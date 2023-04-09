import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string


# You may have to update this dict to match your DB credentials
credentials = {'db_user': '',
               'db_password': '',
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

uri = create_mongodb_uri_string(**credentials)

mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

# We first need the the project from the database
project = Project.objects(name='giraph').get()
activemqProject = Project.objects(name='activemq').get()

# We now select the version control system of the project
vcs_system = VCSSystem.objects(project_id=project.id).get()

print('VCS System:', vcs_system.url)

# We can now fetch the commits and analyze them
num_commits = Commit.objects(vcs_system_id=vcs_system.id).count()

print('Number of commits:', num_commits)

# We now select the issue tracking system of the project
# Please note that some projects have multiple issue trackers
# In this case get() would fail and you would need to loop over them
issue_tracker = IssueSystem.objects(project_id=project.id).get()

print('Issue Tracker:', issue_tracker.url)

# we can now work with the issues
num_issues = Issue.objects(issue_system_id=issue_tracker.id).count()

print('Number of issues:', num_issues)

###
count_comments = 0
count_referenced_by_commits = 0
count_bugs_dev_label = 0
count_bugs_validated = 0
refactor_pattern = re.compile("[ \.;'\"\?!]refactor|^refactor|[ \.;'\"\?!]restructure|^restructure|[ \.;'\"\?!]recode|^recode|[ \.;'\"\?!]reengineer|^reengineer|[ \.;'\"\?!]rewrite|[ \.;'\"\?!]rewrote|[ \.;'\"\?!]rewritten|[ \.;'\"\?!]rewrites|^rewrite|^rewrote|^rewrites|^rewritten|[ \.;'\"\?!]edit|^edit", re.I | re.M)

for issue in Issue.objects(issue_system_id=issue_tracker.id):
    count_comments += IssueComment.objects(issue_id=issue.id).count()
    if issue.issue_type is not None and issue.issue_type.lower()=='bug':
        count_bugs_dev_label += 1
    if issue.issue_type_verified is not None and issue.issue_type_verified.lower()=='bug':
        count_bugs_validated += 1
    if Commit.objects(linked_issue_ids=issue.id).count()>0:
        count_referenced_by_commits += 1
    if issue.title is not None and re.search(refactor_pattern, issue.title) :
        print(issue.title)
        
print('Number of comments in discussions:', count_comments)
print('Number of issues referenced by commits:', count_referenced_by_commits)
print('Number of issues labeled as bugs by developers:', count_bugs_dev_label)
print('Number of issues labeled validated as bug by researchers:', count_bugs_validated)

exit(0)
###


count_bugfix = 0
count_linked_issue = 0
count_hunks = 0
count_refactorings_refdiff = 0
count_refactorings_refactoringminer = 0

# Only limits the fields we are reading to the required fields. This is important for the performance.
for commit in Commit.objects(vcs_system_id=vcs_system.id).only('labels', 'linked_issue_ids'):
    if commit.labels is not None and 'validated_bugfix' in commit.labels and commit.labels['validated_bugfix']==True:
        count_bugfix += 1
    if commit.linked_issue_ids is not None and len(commit.linked_issue_ids)>0:
        count_linked_issue += 1
        
    # File actions group all changed hunks in a commit of the same file
    for fa in FileAction.objects(commit_id=commit.id):
        count_hunks += Hunk.objects(file_action_id=fa.id).count()
        
    count_refactorings_refdiff += Refactoring.objects(commit_id=commit.id, detection_tool='"refDiff"').count()
    count_refactorings_refactoringminer += Refactoring.objects(commit_id=commit.id, detection_tool='rMiner').count()
    print(commit.title)

print('Number of bug fixing commits:', count_bugfix)
print('Number of commits that link to a Jira issue:', count_linked_issue)
print('Number of hunks for all commits:', count_hunks)
print('Number of refactorings detected by refDiff:', count_refactorings_refdiff)
print('Number of refactorings detected by RefactoringMiner:', count_refactorings_refactoringminer)

# We now select the issue tracking system of the project
# Please note that some projects have multiple issue trackers
# In this case get() would fail and you would need to loop over them
issue_tracker = IssueSystem.objects(project_id=project.id).get()

print('Issue Tracker:', issue_tracker.url)

# we can now work with the issues
num_issues = Issue.objects(issue_system_id=issue_tracker.id).count()

print('Number of issues:', num_issues)

count_comments = 0
count_referenced_by_commits = 0
count_bugs_dev_label = 0
count_bugs_validated = 0

for issue in Issue.objects(issue_system_id=issue_tracker.id):
    count_comments += IssueComment.objects(issue_id=issue.id).count()
    if issue.issue_type is not None and issue.issue_type.lower()=='bug':
        count_bugs_dev_label += 1
    if issue.issue_type_verified is not None and issue.issue_type_verified.lower()=='bug':
        count_bugs_validated += 1
    if Commit.objects(linked_issue_ids=issue.id).count()>0:
        count_referenced_by_commits += 1
        
print('Number of comments in discussions:', count_comments)
print('Number of issues referenced by commits:', count_referenced_by_commits)
print('Number of issues labeled as bugs by developers:', count_bugs_dev_label)
print('Number of issues labeled validated as bug by researchers:', count_bugs_validated)

# We now select the mailing list of the project
# Since we have two mailing lists, we need to loop over them
mailing_lists = MailingList.objects(project_id=project.id)
for mailing_list in mailing_lists:
    print('Mailing List:', mailing_list.name)

    # We can now access the messages
    count_emails = Message.objects(mailing_list_id=mailing_list.id).count()

    print('Number of Emails:', count_emails)

    count_references_jira = 0
    
    jira_id = re.compile('GIRAPH-[0-9]+', re.I | re.M)
    for message in Message.objects(mailing_list_id=mailing_list.id):
        if message.body is not None and jira_id.search(message.body):
            count_references_jira += 1
            
    print('Number of emails that reference a Jira issue:', count_references_jira)