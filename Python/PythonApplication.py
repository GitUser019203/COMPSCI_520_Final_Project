import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string

with open("Python\\issue_tracked_projects.txt",'r') as file:
    for line in file:
        project_data = line.strip().split(',')
    
with open("Python\\regexp.txt",'r') as file:
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

total_num_issues = 0
total_num_issues_documenting_refactoring = 0;
total_num_issues_documenting_refactoring_with_linked_commits_reporting_refactoring = 0
total_num_linked_commits = 0
total_num_linked_commits_with_refactoring_reported = 0;

with open("Python\\mongo_db_extract_refactoring_doc.txt", 'w', encoding="utf-8") as out_file:
    for projects in projectCollection:
        for project in projects:
            vcs_system_reported_refactoring = False

            # We now select the version control system of the project
            vcs_system = VCSSystem.objects(project_id=project.id).get()

            # We can now fetch the commits and analyze them
            num_commits = Commit.objects(vcs_system_id=vcs_system.id).count()

            # We now select the issue tracking system of the project
            # Please note that some projects have multiple issue trackers
            # In this case get() would fail and you would need to loop over them
            issue_trackers = IssueSystem.objects(project_id=project.id)

            if issue_trackers.count() > 0:
                for issue_tracker in issue_trackers:
                    issue_tracker_reported_refactoring = False
                    # we can now work with the issues
                    num_issues = Issue.objects(issue_system_id=issue_tracker.id).count()
                    total_num_issues += num_issues        

                    refactor_pattern = re.compile(reg_exp, re.I | re.M | re.DOTALL)

                    for issue in Issue.objects(issue_system_id=issue_tracker.id):
                        if issue.title is not None and re.search(refactor_pattern, issue.title):                            
                            total_num_issues_documenting_refactoring += 1 # There could be False positives!
                            linked_commits = Commit.objects(linked_issue_ids=issue.id)

                            if linked_commits.count() > 0:
                                total_num_linked_commits += linked_commits.count()
                                linked_commit_msgs = [commit.message for commit in linked_commits]
                                refactorings_reported = [(msg is not None and re.search(refactor_pattern, msg)) for msg in linked_commit_msgs]
                                if any(refactorings_reported):
                                    total_num_issues_documenting_refactoring_with_linked_commits_reporting_refactoring += 1
                                    if vcs_system_reported_refactoring:
                                        if issue_tracker_reported_refactoring:
                                            print("Issue Title: " + issue.title + "\nIssue Id: " \
                                            + str(issue.id), file=out_file)
                                        else:
                                            print('Issue Tracker:', issue_tracker.url + "Issue Title: " + issue.title + "\nIssue Id: " \
                                            + str(issue.id), file=out_file)
                                            issue_tracker_reported_refactoring = True
                                    else:
                                        print('VCS System:' + vcs_system.url + "\n" + 'Issue Tracker:', issue_tracker.url \
                                        + "Issue Title: " + issue.title + "\nIssue Id: " + str(issue.id), file=out_file)
                                        vcs_system_reported_refactoring = True
                                        issue_tracker_reported_refactoring = True
                                        
                                for commit in linked_commits:
                                    if commit.message is not None and re.search(refactor_pattern, commit.message):
                                        revision_hash = commit.revision_hash
                                        total_num_linked_commits_with_refactoring_reported += 1
                                        print("Linked Commit Revision Hash: " + str(revision_hash), file=out_file)
                                        print("Linked Commit Github URL: " + vcs_system.url.replace(".git", "") + "/commit/" + revision_hash, file=out_file)

    print("The total number of issues is " + str(total_num_issues), file=out_file)
    print("The total number of issues with refactoring documentation in their titles is " + str(total_num_issues_documenting_refactoring), file=out_file)
    print("The total number of issues with refactoring documentation in their titles and that have linked commits reported to involve refactoring is " + str(total_num_issues_documenting_refactoring_with_linked_commits_reporting_refactoring), file=out_file)
    print("The total number of linked commits is " + str(total_num_linked_commits), file=out_file)
    print("The total number of linked commits reported to involve refactoring is " + str(total_num_linked_commits_with_refactoring_reported), file=out_file)