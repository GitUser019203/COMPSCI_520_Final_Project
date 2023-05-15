import re
lines = []
with open(file='extractedIssueDescBugs.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)

list1 =["found a bug", "there is a bug", "a bug has been found", "it is a bug", "this is a bug", "this bug", "catch(ed) this/a bug"]
list2=["bug#"]
list3=["fixed a bug", "bug fix(es)", "fixes bug", "fix bug"]
list4=["bug report(ed)", "report a bug","bug report"]
counterFound =0
counterBugClassify=0
totalIssues = 0
counterBugFix = 0
counterBugReport = 0
for i in lines:
  totalIssues+=1
  if any(word in i.lower() for word in list1):
      counterFound+=1
      print("printing",counterFound)
  elif any(word in i.lower() for word in list2) or re.findall(r"bug#\d+", i):
        counterBugClassify+=1
  elif any(word in i.lower() for word in list3):
        counterBugFix+=1
  elif any(word in i.lower() for word in list4):
        counterBugReport+=1
"""
  #j = i.split()
  
  #for m in j:
    if any(word in m.lower() for word in list1):
      counterFound+=1
      print("printing",counterFound)
    elif any(word in m.lower() for word in list2) or re.findall(r"bug#\d+", m):
        counterBugClassify+=1
    elif any(word in m.lower() for word in list3):
        counterBugFix+=1
    elif any(word in m.lower() for word in list4):
        counterBugReport+=1
    """
#print("total",totalIssues)
#print(counterAdd,counterBugClassify,counterBugFix)


print("Evaluation Criteria")
print("Issues that talked about Bug Found: ",(counterFound/totalIssues)*100,"%")
print("Issues that talked about Bug Classification: ",(counterBugClassify/totalIssues)*100,"%")
print("Issues that talked about Bug Fix: ",(counterBugFix/totalIssues)*100,"%")
print("Issues that talked about Bug Report: ",(counterBugReport/totalIssues)*100,"%")

