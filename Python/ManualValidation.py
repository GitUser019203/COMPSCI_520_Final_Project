import PythonApplicationForBugs as bugs
import PythonApplicationForRefactoring as refactor
import random

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
checkBugsTitles()
checkRefactoringBodies()
checkBugsBodies()

