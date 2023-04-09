import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string

with open("issue_tracked_projects.txt",'r') as file:
    for line in file:
        project_data = line.strip().split(',')
    

# You may have to update this dict to match your DB credentials
credentials = {'db_user': '',
               'db_password': '',
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

uri = create_mongodb_uri_string(**credentials)

mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

projectCollection = [Project.objects(name=project_name) for project_name in project_data]

for projects in projectCollection:
    for project in projects:

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

        count_comments = 0
        count_referenced_by_commits = 0
        count_bugs_dev_label = 0
        count_bugs_validated = 0
        refactor_pattern = re.compile("[ \.;'\"\?!]restructure|^restructure|[ \.;'\"\?!]recode|^recode|[ \.;'\"\?!]reengineer|^reengineer|[ \.;'\"\?!]rewrite|[ \.;'\"\?!]rewrote|[ \.;'\"\?!]rewritten|[ \.;'\"\?!]rewrites|^rewrite|^rewrote|^rewrites|^rewritten|[ \.;'\"\?!]edit|^edit", re.I | re.M)

        for issue in Issue.objects(issue_system_id=issue_tracker.id):
            count_comments += IssueComment.objects(issue_id=issue.id).count()
            if issue.issue_type is not None and issue.issue_type.lower()=='bug':
                count_bugs_dev_label += 1
            if issue.issue_type_verified is not None and issue.issue_type_verified.lower()=='bug':
                count_bugs_validated += 1
            if Commit.objects(linked_issue_ids=issue.id).count()>0:
                count_referenced_by_commits += 1
            if issue.title is not None and re.search(refactor_pattern, issue.title):
                print("Issue Title: " + issue.title + "\nIssue Id: " + str(issue.id))
                linked_commits = Commit.objects(linked_issue_ids=issue.id)
                revision_hashes = [commit.revision_hash for commit in linked_commits]
                commit_ids = [commit.id for commit in linked_commits]
                print("Linked Commit Revision Hashes: " + str(revision_hashes))
                print("Linked Commit Ids: " + str(commit_ids))
        
        print('Number of comments in discussions:', count_comments)
        print('Number of issues referenced by commits:', count_referenced_by_commits)
        print('Number of issues labeled as bugs by developers:', count_bugs_dev_label)
        print('Number of issues labeled validated as bug by researchers:', count_bugs_validated)
