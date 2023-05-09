import re
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string
import matplotlib.pyplot as plt
import numpy as np

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
totalBugs = 0
totalValidatedBugs = 0
totalIssues = 0
totalCommits = 0
detectedBugList = []

for projects in projectCollection:
    for project in projects:
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
        bug_pattern = re.compile("[ \.;'\"\?!]restructure[ \.;'\"\?!]|[ \.;'\"\?!]restructured[ \.;'\"\?!]|[ \.;'\"\?!]restructuring[ \.;'\"\?!]|[ \.;'\"\?!]restructures[ \.;'\"\?!]|^restructure[ \.;'\"\?!]|^restructured[ \.;'\"\?!]|^restructures[ \.;'\"\?!]|^restructuring[ \.;'\"\?!]|[ \.;'\"\?!]restructure$|[ \.;'\"\?!]restructured$|[ \.;'\"\?!]restructuring$|[ \.;'\"\?!]restructures$|[ \.;'\"\?!]recode[ \.;'\"\?!]|[ \.;'\"\?!]recoded[ \.;'\"\?!]|[ \.;'\"\?!]recoding[ \.;'\"\?!]|[ \.;'\"\?!]recodes[ \.;'\"\?!]|[ \.;'\"\?!]recode$|[ \.;'\"\?!]recoded$|[ \.;'\"\?!]recoding$|[ \.;'\"\?!]recodes$|^recode[ \.;'\"\?!]|^recodes[ \.;'\"\?!]|^recoding[ \.;'\"\?!]|^recoded[ \.;'\"\?!]|[ \.;'\"\?!]reengineer[ \.;'\"\?!]|[ \.;'\"\?!]reengineered[ \.;'\"\?!]|[ \.;'\"\?!]reengineers[ \.;'\"\?!]|[ \.;'\"\?!]reengineer$|[ \.;'\"\?!]reengineered$|[ \.;'\"\?!]reengineers$|^reengineer[ \.;'\"\?!]|^reengineers[ \.;'\"\?!]|^reengineered[ \.;'\"\?!]|[ \.;'\"\?!]rewrite[ \.;'\"\?!]|[ \.;'\"\?!]rewrote[ \.;'\"\?!]|[ \.;'\"\?!]rewritten[ \.;'\"\?!]|[ \.;'\"\?!]rewrites[ \.;'\"\?!]|[ \.;'\"\?!]rewrite$|[ \.;'\"\?!]rewrote$|[ \.;'\"\?!]rewritten$|[ \.;'\"\?!]rewrites$|^rewrite[ \.;'\"\?!]|^rewrote[ \.;'\"\?!]|^rewrites[ \.;'\"\?!]|^rewritten[ \.;'\"\?!]|[ \.;'\"\?!]edit[ \.;'\"\?!]|[ \.;'\"\?!]edits[ \.;'\"\?!]|[ \.;'\"\?!]edited[ \.;'\"\?!]|[ \.;'\"\?!]edit$|[ \.;'\"\?!]edits$|[ \.;'\"\?!]edited$|^edit[ \.;'\"\?!]|^edited[ \.;'\"\?!]|^edits[ \.;'\"\?!]|[ \.;'\"\?!]add.*|^add.*|[ \.;'\"\?!]Add.*|^Add.*|[ \.;'\"\?!]chang.*|^chang.*|[ \.;'\"\?!]Chang.*|^Chang.*|[ \.;'\"\?!]creat.*|^creat.*|[ \.;'\"\?!]Creat.*|^Creat.*|[ \.;'\"\?!]extend.*|^extend.*|[ \.;'\"\?!]Extend.*|^Extend.*|[ \.;'\"\?!]extract.*|^extract.*|[ \.;'\"\?!]Extract.*|^Extract.*|[ \.;'\"\?!]fix.*|^fix.*|[ \.;'\"\?!]Fix.*|^Fix.*|[ \.;'\"\?!]improv.*|^improv.*|[ \.;'\"\?!]Improv.*|^Improv.*|[ \.;'\"\?!]inlin.*|^inlin.*|[ \.;'\"\?!]Inlin.*|^Inlin.*|[ \.;'\"\?!]introduc.*|^introduc.*|[ \.;'\"\?!]Introduc.*|^Introduc.*|[ \.;'\"\?!]merg.*|^merg.*|[ \.;'\"\?!]Merg.*|^Merg.*|[ \.;'\"\?!]mov.*|^mov.*|[ \.;'\"\?!]Mov.*|^Mov.*|[ \.;'\"\?!]repackag.*|^repackag.*|[ \.;'\"\?!]Repackag.*|^Repackag.*|[ \.;'\"\?!]redesign.*|^redesign.*|[ \.;'\"\?!]Redesign.*|^Redesign.*|[ \.;'\"\?!]reduc.*|^reduc.*|[ \.;'\"\?!]Reduc.*|^Reduc.*|[ \.;'\"\?!]refin.*|^refin.*|[ \.;'\"\?!]Refin.*|^Refin.*|[ \.;'\"\?!]remov.*|^remov.*|[ \.;'\"\?!]Remov.*|^Remov.*|[ \.;'\"\?!]renam.*|^renam.*|[ \.;'\"\?!]Renam.*|^Renam.*|[ \.;'\"\?!]reorganiz.*|^reorganiz.*|[ \.;'\"\?!]Reorganiz.*|^Reorganiz.*|[ \.;'\"\?!]replac.*|^replac.*|[ \.;'\"\?!]Replac.*|^Replac.*|[ \.;'\"\?!]restructur.*|^restructur.*|[ \.;'\"\?!]Restructur.*|^Restructur.*|[ \.;'\"\?!]rewrit.*|^rewrit.*|[ \.;'\"\?!]Rewrit.*|^Rewrit.*|[ \.;'\"\?!]split.*|^split.*|[ \.;'\"\?!]Split.*|^Split.*|[ \.;'\"\?!]chang.* the name[ \.;'\"\?!]|[ \.;'\"\?!]chang.* the name$|^chang.* the name[ \.;'\"\?!]|^chang.* the name$|[ \.;'\"\?!]clean.* up code[ \.;'\"\?!]|[ \.;'\"\?!]clean.* up code$|^clean.* up code[ \.;'\"\?!]|^clean.* up code$|[ \.;'\"\?!]cleanup[ \.;'\"\?!]|[ \.;'\"\?!]cleanup$|^cleanup[ \.;'\"\?!]|^cleanup$|[ \.;'\"\?!]code clean.*[ \.;'\"\?!]|[ \.;'\"\?!]code clean.*$|^code clean.*[ \.;'\"\?!]|^code clean.*$|[ \.;'\"\?!]code optimization[ \.;'\"\?!]|[ \.;'\"\?!]code optimization$|^code optimization[ \.;'\"\?!]|^code optimization$|[ \.;'\"\?!]fix.* code style[ \.;'\"\?!]|[ \.;'\"\?!]fix.* code style$|^fix.* code style[ \.;'\"\?!]|^fix.* code style$|[ \.;'\"\?!]improv.* code quality[ \.;'\"\?!]|[ \.;'\"\?!]improv.* code quality$|^improv.* code quality[ \.;'\"\?!]|^improv.* code quality$|[ \.;'\"\?!]pull.* up[ \.;'\"\?!]|[ \.;'\"\?!]pull.* up$|^pull.* up[ \.;'\"\?!]|^pull.* up$|[ \.;'\"\?!]push.* down[ \.;'\"\?!]|[ \.;'\"\?!]push.* down$|^push.* down[ \.;'\"\?!]|^push.* down$|[ \.;'\"\?!]simplify.* code[ \.;'\"\?!]|[ \.;'\"\?!]simplify.* code$|^simplify.* code[ \.;'\"\?!]|^simplify.* code$", re.I | re.M)

        
        for issue in Issue.objects(issue_system_id=issue_tracker.id):
            count_comments += IssueComment.objects(issue_id=issue.id).count()
            if issue.issue_type is not None and issue.issue_type.lower()=='refactor':
                count_bugs_dev_label += 1
            if issue.issue_type_verified is not None and issue.issue_type_verified.lower() in bugSynonymList:
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

print("Total Issues reported: ",totalIssues)
print("Total bugs reported: ",totalBugs)
print("Total bugs validated: ",totalValidatedBugs)
print("Detected bugs",len(detectedBugList))
print("Commited bugs detected",len(commitBugsDetected))
print(" The number of issues that talk about bugst are (Evaluation Criteria) : ", ((totalValidatedBugs+len(detectedBugList))/totalIssues)*100 )

"""
x = (totalValidatedBugs/totalIssues)*100
y = np.array([x, 100 - x])
myexplode = [0.2,0]
ax1 = plt.subplot()
plotLabel = ["Validated Issue titles containing 'bug'","Other Issues"]
ax1.pie(y, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
plt.show()

ax2 = plt.subplot()
a = (len(detectedBugList)/totalIssues)*100
b = np.array([a, 100 - a])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Validated Issue titles containing 'bug'synonyms","Other Issues"]
ax2.pie(b, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
plt.show()
"""
Allbugs = ((totalValidatedBugs+len(detectedBugList))/totalIssues)*100 
chartArr = np.array([Allbugs, 100 - Allbugs])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Bug related Issues","Other Issues"]
plt.pie(chartArr, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()