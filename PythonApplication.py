import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string

with open("issue_tracked_projects.txt",'r') as file:
    for line in file:
        project_data = line.strip().split(',')
    
with open("regexp.txt",'r') as file:
    for line in file:
        reg_exp = line.strip()

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
        
        refactor_pattern = re.compile(reg_exp, re.I | re.M | re.DOTALL)

        for issue in Issue.objects(issue_system_id=issue_tracker.id):
            if issue.title is not None and re.search(refactor_pattern, issue.title):
                print("Issue Title: " + issue.title + "\nIssue Id: " + str(issue.id))
                linked_commits = Commit.objects(linked_issue_ids=issue.id)
                revision_hashes = [commit.revision_hash for commit in linked_commits]
                commit_ids = [commit.id for commit in linked_commits]
                
                for revision_hash in revision_hashes:
                    print("Linked Commit Revision Hash: " + str(revision_hashes))
                    print("Linked Commit Github URL: " + vcs_system.url.replace(".git", "") + "/commit/" + revision_hash)
 