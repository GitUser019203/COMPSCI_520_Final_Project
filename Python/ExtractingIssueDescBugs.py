import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string
import matplotlib.pyplot as plt
import numpy as np

# You may have to update this dict to match your DB credentials
credentials = {'db_user': '',
               'db_password': '',
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

uri = create_mongodb_uri_string(**credentials)

mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

projectCollection = [Project.objects()]
totalBugs = 0
totalValidatedBugs = 0
totalIssues = 0
totalCommits = 0
detectedBugList = []

with open(r"Python\extractedIssueDescBugs.txt", 'w', encoding="utf-8") as out_file:
    for projects in projectCollection:
        for i, project in enumerate(projects):
            print(f"{i}. {project.name}")
            # We now select the version control system of the project
            vcs_system = VCSSystem.objects(project_id=project.id).get()
            # We can now fetch the commits and analyze them
            num_commits = Commit.objects(vcs_system_id=vcs_system.id).count()
            totalCommits+=num_commits
            # We now select the issue tracking system of the project
            # Please note that some projects have multiple issue trackers
            # In this case get() would fail and you would need to loop over them
            issue_tracker = IssueSystem.objects(project_id=project.id).get()
            # we can now work with the issues
            num_issues = Issue.objects(issue_system_id=issue_tracker.id).count()

            totalIssues+=num_issues
            count_comments = 0
            count_referenced_by_commits = 0
            count_bugs_dev_label = 0
            count_bugs_validated = 0
            detectedBug = 0
            commitBugsDetected = []
            bugSynonymList = ['bug','bugs','error','failure','defect','fault']
            bug_pattern = re.compile("[ \.;'\"\?!]bug|^bug|[ \.;'\"\?!]bugs|^bugs|[ \.;'\"\?!]error|^error|[ \.;'\"\?!]fault|[ \.;'\"\?!]faults|[ \.;'\"\?!]defect|[ \.;'\"\?!]bugs|^bugged|^bug|[ \.;'\"\?!]problem|^problems", re.I | re.M)

            for issue in Issue.objects(issue_system_id=issue_tracker.id):
                if issue.issue_type is not None and issue.issue_type.lower() in bugSynonymList:
                    count_bugs_dev_label += 1
                if issue.issue_type_verified is not None and issue.issue_type_verified.lower() in bugSynonymList:
                    description = issue.desc
                    print("Issue Description: ",description,file=out_file)
                    count_bugs_validated += 1
                if Commit.objects(linked_issue_ids=issue.id).count()>0:
                    count_referenced_by_commits += 1
                for commits in Commit.objects(linked_issue_ids=issue.id):
                    if commits.message is not None and re.search(bug_pattern, commits.message):
                        commitBugsDetected.append(commits.message)
                if issue.title is not None and re.search(bug_pattern, issue.title):
                    detectedBugList.append(issue.title)
                    linked_commits = Commit.objects(linked_issue_ids=issue.id)
                    revision_hashes = [commit.revision_hash for commit in linked_commits]
                    commit_ids = [commit.id for commit in linked_commits]

            totalBugs+=count_bugs_dev_label
            totalValidatedBugs+=count_bugs_validated
