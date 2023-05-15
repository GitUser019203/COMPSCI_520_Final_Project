import re


def extractIssueDesc(filepath: str) -> list:
    '''
    Extract Issue Descriptions as format of 
    :param filepath: path to txt file
    Returns:
    '''
    lines = []
    
    # Open file
    with open(file=filepath, mode='r') as out_file:
            # Have empty string for issue description
            iss_desc_entry = ""

            # Go through every line in file
            for line in out_file:
                # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
                if "Issue Description:" in line:
                    if len(iss_desc_entry) == 0:
                        # Add first line to entry
                        iss_desc_entry += line
                    else:
                        # Remove any newlines \n. End of current entry; add to list
                        lines.append(iss_desc_entry.replace("\n", " "))

                        # Update entry with next entry
                        iss_desc_entry = line
                else:
                    # Keep adding line to entry
                    iss_desc_entry += line

    # Return list
    return lines

lines = extractIssueDesc(filepath='./Python/extractedIssueDescBugs.txt')
print(lines[0:5])
exit()

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
print("total",totalIssues)
print(counterFound,counterBugClassify,counterBugFix,counterBugReport)


print("Evaluation Criteria")
print("Issues that talked about Bug Found: ",(counterFound/totalIssues)*100,"%")
print("Issues that talked about Bug Classification: ",(counterBugClassify/totalIssues)*100,"%")
print("Issues that talked about Bug Fix: ",(counterBugFix/totalIssues)*100,"%")
print("Issues that talked about Bug Report: ",(counterBugReport/totalIssues)*100,"%")

d = np.array([counterFound, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Bug Found","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterBugClassify, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Bug Classification","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterBugFix, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Bug Fixes","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()

d = np.array([counterBugReport, totalIssues])
myexplode = [0.2,0]
fig1, ax1 = plt.subplots()
plotLabel = ["Issues about Bug Report","Other Issues"]
plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()