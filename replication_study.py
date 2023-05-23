from sys import argv
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit,Refactoring, Issue
from pycoshark.utils import create_mongodb_uri_string
from Python.stopwatch import StopWatch

# Assign db_user and db_password depending on cmd arguments.
if argv[0] == '':
    db_user = ''
    db_password = ''
else:
    db_user = ''
    db_password = ''

# You may have to update this dict to match your DB credentials
credentials = {'db_user': db_user,
               'db_password': db_password,
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

print('Connecting to the MongoDB server.')
uri = create_mongodb_uri_string(**credentials)
mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

print('Starting to mine the 68 projects with the SmartSHARK database information.')
projectCollection = Project.objects()
stopwatch = StopWatch()
stopwatch.start()

refactoring_commits_with_issues = set()
issues_having_kwrd_refactor_in_title = set()
refactoring_commits_with_issues_having_kwrd_refactor_in_title = set()
refactoring_operations_associated_with_issues = set()
for j, project in enumerate(projectCollection):
    print(f"Starting mining project #{j} named {project.name}")
    # We now select the version control system of the project
    vcs_system = VCSSystem.objects(project_id=project.id).get()
        
    # We can now grab the commits in the VCS system
    commits = Commit.objects(vcs_system_id=vcs_system.id)
    
    for commit in commits:
        refactorings = Refactoring.objects(commit_id=commit.id)
        if refactorings.count() > 0:
            if commit.linked_issue_ids and len(commit.linked_issue_ids) > 0:
                any_list = []
                for linked_issue_id in commit.linked_issue_ids:
                    for issue in Issue.objects(id=linked_issue_id):
                        if issue.title is not None and "refactor" in issue.title.casefold():
                            any_list.append(True)
                if any(any_list):
                    refactoring_commits_with_issues_having_kwrd_refactor_in_title.add(commit.id)
                refactoring_commits_with_issues.add(commit.id)
                for refactoring_operation in refactorings:
                    refactoring_operations_associated_with_issues.add(refactoring_operation.id)
    print(f'Completed mining {project.name}')

print("Starting issue mining.")
issues = Issue.objects()
for i, issue in enumerate(issues):
    if issue.title is not None and "refactor" in issue.title.casefold():
        issues_having_kwrd_refactor_in_title.add(issue.id)
    if i % 1000 == 0:
        print(f"Finished mining {i} issues.")
print("Completed issue mining.")

stopwatch.stop()
stopwatch.get_elapsed_time()

print(f"Refactoring commits with issues: {len(refactoring_commits_with_issues)}")
print(f"Refactoring commits with issues having keyword 'refactor' in title: {len(refactoring_commits_with_issues_having_kwrd_refactor_in_title)}")
print(f"Refactoring operations associated with issues: {len(refactoring_operations_associated_with_issues)}")
print(f"Issues that reported developers' intention about the application of refactoring (i.e., having the keyword 'refactor'): {len(issues_having_kwrd_refactor_in_title)}")