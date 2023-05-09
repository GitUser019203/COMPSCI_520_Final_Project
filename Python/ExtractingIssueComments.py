import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string

with open(r"issue_tracked_projects.txt",'r') as file:
    for line in file:
        project_data = line.strip().split(',')
    
with open(r"regexp.txt",'r') as file:
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
total_num_commits_linked_to_issues_documenting_refactoring = 0;
total_num_commits_reporting_refactoring_linked_to_issues_documenting_refactoring = 0
unique_commit_hashes = set()
unique_commit_hashes_with_refactoring_reported = set()

with open("Python\\extractedIssueComments.txt", 'w', encoding="utf-8") as out_file:
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
                if issue_trackers.count() > 1:
                    print(f"The VCS system {vcs_system} has more than one issue tracker.", file=out_file)
                    [print(f"Issue Tracker URL: {issue_tracker.url}", file=out_file) for issue_tracker in issue_trackers]

                for issue_tracker in issue_trackers:
                    issue_tracker_reported_refactoring = False
                    # we can now work with the issues
                    num_issues = Issue.objects(issue_system_id=issue_tracker.id).count()
                    total_num_issues += num_issues        

                    refactor_pattern = re.compile(reg_exp, re.I | re.M | re.DOTALL)

                    for issue in Issue.objects(issue_system_id=issue_tracker.id):
                        if issue.title is not None and re.search(refactor_pattern, issue.title):                            
                            total_num_issues_documenting_refactoring += 1 # There could be False positives!
                            com = IssueComment.objects(issue_id=issue.id).values_list('comment')
                            print("Comment: ",com,file=out_file)
                            linked_commits = Commit.objects(linked_issue_ids=issue.id)
                            for commit in linked_commits:
                                # Although distinct commits can have identical commit hashes it is rare
                                unique_commit_hashes.add(commit.revision_hash)
                            total_num_commits_linked_to_issues_documenting_refactoring += linked_commits.count()
                            if linked_commits.count() > 0:
                                linked_commit_msgs = [commit.message for commit in linked_commits]
                                refactorings_reported = [(msg is not None and re.search(refactor_pattern, msg)) for msg in linked_commit_msgs]
                                if any(refactorings_reported):
                                    total_num_issues_documenting_refactoring_with_linked_commits_reporting_refactoring += 1
                                    if vcs_system_reported_refactoring:
                                        if not issue_tracker_reported_refactoring:
                                            #print("Issue Title: " + issue.title + "\nIssue Id: " \
                                            #+ str(issue.id), file=out_file)
                                        #else:
                                            #print('Issue Tracker:', issue_tracker.url + "\nIssue Title: " + issue.title + "\nIssue Id: " \
                                            #+ str(issue.id), file=out_file)
                                            issue_tracker_reported_refactoring = True
                                    else:
                                        #print('VCS System:' + vcs_system.url + "\n" + 'Issue Tracker:', issue_tracker.url \
                                        #+ "\nIssue Title: " + issue.title + "\nIssue Id: " + str(issue.id), file=out_file)
                                        vcs_system_reported_refactoring = True
                                        issue_tracker_reported_refactoring = True
                                        
                                for commit in linked_commits:
                                    if commit.message is not None and re.search(refactor_pattern, commit.message):
                                        revision_hash = commit.revision_hash
                                        total_num_commits_reporting_refactoring_linked_to_issues_documenting_refactoring += 1
                                        # Although distinct commits can have identical commit hashes it is rare
                                        unique_commit_hashes_with_refactoring_reported.add(revision_hash)
                                        #print("Linked Commit Revision Hash: " + str(revision_hash), file=out_file)
                                        #print("Linked Commit Github URL: " + vcs_system.url.replace(".git", "") + "/commit/" + revision_hash, file=out_file)

    print("\n", file=out_file)
    print("RESULTS", file=out_file)
    print("=" * 100, file=out_file)
    print("The total number of issues is " + str(total_num_issues) + ".", file=out_file)
    print("The total number of issues with refactoring documentation in their titles is " + str(total_num_issues_documenting_refactoring) + ".", file=out_file)
    print("However, only " + str(total_num_issues_documenting_refactoring_with_linked_commits_reporting_refactoring) + " of the issues have linked commits that developers have labelled as involving refactoring.", file=out_file)
    print("The total number of unique commits linked to issues documenting refactoring is " + str(len(unique_commit_hashes)) + ".", file=out_file)    
    print("However, developers have reported that only " + str(len(unique_commit_hashes_with_refactoring_reported)) + " of them involve refactoring.", file=out_file)
    print(f"There are {total_num_commits_linked_to_issues_documenting_refactoring - len(unique_commit_hashes)} duplicate commits linked to issues documenting refactoring.", file=out_file)
    print(f"Developers have affirmed that {total_num_commits_reporting_refactoring_linked_to_issues_documenting_refactoring - len(unique_commit_hashes_with_refactoring_reported)} of the duplicate linked commits do refactoring.", file=out_file)