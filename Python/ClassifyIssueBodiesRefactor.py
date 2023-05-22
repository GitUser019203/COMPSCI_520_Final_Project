import re
import numpy as np
import matplotlib.pyplot as plt
lines = []
with open(file='extractedIssueDescRefactoring.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)
add_verbs = [
    "add",
    "append",
    "creat",
    "introduc",
    "nice to hav",
    "creat",
    "helpful"
]

modify_verbs = [
    "clean",
    "modify",
    "chang",
    "mov",
    "repair",
    "fix",
    "simplif",
    "split",
    "refactor",
    "rewrit",
    "reorganiz",
    "shift",
    "migrat",
    "extend",
    "improve",
    "restructur",
    "consolidat",
    "decompos",
    "merg",
    "extract",
    "moderniz",
    "renam",
    "reorder",
    "updat",
    "format",
    "combin",
    "optimiz",
    "optimis"
]

delete_verbs = [
    "delet",
    "reduc",
    "remov",
    "rid",
    "dump",
    "scratch",
    "redundan",
    "eliminat",
    "drop",
    "discard",
    "exclud",
    "prun",
    "trim"
]

nouns = [
    "feat",
    "func",
    "class",
    "component",
    "method",
    "property",
    "parameter",
    "arg",
    "interface",
    "dependenc",
    "lib",
    "plugin",
    "test",
    "coverage",
    "example",
    "demo",
    "doc",
    "trace",
    "error.*message",
    "error.*msg",
    "warning",
    "order",
    "performance",
    "style",
    "versioning",
    "format",
    "readability",
    "comment"
]

add_list = [f"{verb}.*{noun}" for verb in add_verbs for noun in nouns] + [f"{noun}.*{verb}" for verb in add_verbs for noun in nouns]

modify_list = [f"{verb}.*{noun}" for verb in modify_verbs for noun in nouns] + [f"{noun}.*{verb}" for verb in modify_verbs for noun in nouns]

delete_list = [f"{verb}.*{noun}" for verb in delete_verbs for noun in nouns] + [f"{noun}.*{verb}" for verb in delete_verbs for noun in nouns]

#add_list =[
#    "add",
#    "append",
#    "creat",
#    "apply",
#    "extend",
#    "introduce"
#]
#modify_list=["clean","modify","repair","fix","simplify","split","redesign","refactor","rewrite","repackage","refactor", "refactoring", "refactors", "refactorings", "refactored","cleaned","simplified"]
#delete_list=["reduce","reduction","delete","subtract","remove","dump","rid","push down","redundant"]
counterAdd =0
counterModify=0
totalIssues = 0
counterDelete = 0

for i in lines:
    totalIssues+=1
    if any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in delete_list):
        counterDelete += 1
    elif any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in modify_list):
        counterModify += 1
    elif any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in add_list):
        counterAdd += 1

print("total",totalIssues)
print(f"Issues about additions: {counterAdd}")
print(f"Issues about modifications: {counterModify}")
print(f"Issues about deletions: {counterDelete}")

print("Evaluation Criteria")
print("Issues that talked about Code Addition: ",(counterAdd/totalIssues)*100,"%")
print("Issues that talked about Code Modification: ",(counterModify/totalIssues)*100,"%")
print("Issues that talked about Code Deletion: ",(counterDelete/totalIssues)*100,"%")

d = np.array([counterAdd, counterModify, counterDelete, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Code Addition", "Issues About Code Modification", "Issues About Code Deletion", "Other Issues"]
plt.pie(d, labels=plotLabel,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterAdd, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Code Addition","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterModify, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Code Modification","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterDelete, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Code Deletion","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()


