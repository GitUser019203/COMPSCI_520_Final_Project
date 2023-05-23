import PythonApplicationForBugs as bugs
import PythonApplicationForRefactoring as refactor
import random
import numpy as np
import matplotlib.pyplot as plt

def checkRefactoringTitles():
    print(random.choices(refactor.refactoringIssueTitles, k=20))

def checkBugsTitles():
    print(random.choices(bugs.detectedBugList, k=20))

def checkRefactoringBodies():
    lines = []
    with open(file='extractedIssueDescRefactoring.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)
    print(random.choices(lines, k=20))

def checkBugsBodies():
    lines2 = []
    with open(file='extractedIssueDescBugs.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines2.append(line)
    print(random.choices(lines2, k=20))

    
checkRefactoringTitles()
print("+++++++=")
checkBugsTitles()
print("+++++++=")
checkRefactoringBodies()
print("+++++++=")
checkBugsBodies()
print("+++++++=")


d = np.array([1, 20])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Incorrect Refactor Issue Title Classification","Correct Classification"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([2, 20])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Incorrect Bug Issue Title Classification","Correct Classification"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([2, 20])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Total incorrect classification for Refactoring Issue Bodies","Correct Classification"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([3, 20])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Total incorrect classification for Bugs Issue Bodies","Correct Classification"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()