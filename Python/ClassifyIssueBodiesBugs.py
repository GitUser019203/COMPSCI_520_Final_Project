import re
from matplotlib import pyplot as plt

import numpy as np


def extractIssueDesc(filepath: str) -> list:
    """
    Extract Issue Descriptions as format of 
    :param: filepath: path to txt file
    Returns list of extracted issue bodies
    """
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


def bugCounter(issue_body_list: list, 
                   bug_id_keys: list, 
                   bug_class_keys: list, 
                   bug_fix_keys: list,
                   bug_report_keys: list) -> list:
    """
    Count number of Issue Bodies that exist, plus Issue Bodies that are 
    in one of the types or groups:
    - Bug Identification
    - Bug Classification
    - Bug Fixes
    - Bug Reports
    :param: issue_body_list: list of issue bodies extracted
    :param: bug_id_keys: list of bug identification keys
    :param: bug_class_keys: list of bug classification keys
    :param: bug_fix_keys: list of bug fix keys
    :param: bug_report_keys: list of bug report keys
    Returns list of extracted issue bodies
    """        
    # Set counters
    total_issues = 0
    counter_found = 0
    counter_bug_classify = 0
    counter_bug_fix = 0
    counter_bug_report = 0

    # Loop through each line and count all occurences
    for i in issue_body_list:
        total_issues += 1
        if any(word in i.lower() for word in bug_id_keys):
            counter_found += 1
        elif any(word in i.lower() for word in bug_class_keys) or re.findall(r"bug#\d+", i) or re.findall(r"bug\d+", i):
            counter_bug_classify += 1
        elif any(word in i.lower() for word in bug_fix_keys) or re.findall(r"^fix *bug$", i):
            counter_bug_fix += 1
        elif any(word in i.lower() for word in bug_report_keys):
            counter_bug_report += 1
    
    # Return list of all counters
    return [total_issues, counter_found, counter_bug_classify, counter_bug_fix, counter_bug_report]
    

# Get list of lines from filepath
lines = extractIssueDesc(filepath='./Python/extractedIssueDescBugs.txt')

# Identify list of keywords for specific 
bug_identify_list = [
     "found a bug", 
     "there is a bug", 
     "bug has been found", 
     "it is a bug", 
     "this is a bug", 
     "this bug", 
     "catch this bug", 
     "catch a bug", 
     "catched this bug", 
     "catched a bug"
     ]
bug_classify_list = [" bug#"]
bug_fix_list = [
     "fixed a bug", 
     "fix a bug", 
     "bug fix", 
     "fixes bug", 
     "fix bug"
     ]
bug_report_list = [
     "bug reported", 
     "report a bug",
     "bug report "]

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

bug_counters = bugCounter(issue_body_list=lines, 
                          bug_id_keys=bug_identify_list, 
                          bug_class_keys=bug_classify_list, 
                          bug_fix_keys=bug_fix_list,
                          bug_report_keys=bug_report_list)

totalIssues = bug_counters[0]
counterFound = bug_counters[1]
counterBugClassify = bug_counters[2]
counterBugFix = bug_counters[3]
counterBugReport = bug_counters[4]

print("total issues:", totalIssues)
print("total bugs identify:", counterFound)
print("total bugs classify:", counterBugClassify)
print("total bugs fixes:", counterBugFix)
print("total bugs reports:", counterBugReport)

print("Evaluation Criteria")
print("Issues that talked about Bug Found: ",(counterFound/totalIssues)*100,"%")
print("Issues that talked about Bug Classification: ",(counterBugClassify/totalIssues)*100,"%")
print("Issues that talked about Bug Fix: ",(counterBugFix/totalIssues)*100,"%")
print("Issues that talked about Bug Report: ",(counterBugReport/totalIssues)*100,"%")

# d = np.array([counterFound, totalIssues])
# myexplode = [0.2,0]
# fig1, ax1 = plt.subplots()
# plotLabel = ["Issues about Bug Found","Other Issues"]
# plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
# plt.axis('equal')
# plt.show()

# d = np.array([counterBugClassify, totalIssues])
# myexplode = [0.2,0]
# fig1, ax1 = plt.subplots()
# plotLabel = ["Issues about Bug Classification","Other Issues"]
# plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
# plt.axis('equal')
# plt.show()

# d = np.array([counterBugFix, totalIssues])
# myexplode = [0.2,0]
# fig1, ax1 = plt.subplots()
# plotLabel = ["Issues about Bug Fixes","Other Issues"]
# plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
# plt.axis('equal')
# plt.show()

# d = np.array([counterBugReport, totalIssues])
# myexplode = [0.2,0]
# fig1, ax1 = plt.subplots()
# plotLabel = ["Issues about Bug Report","Other Issues"]
# plt.pie(d, labels=plotLabel,explode = myexplode,autopct='%1.1f%%', startangle=90)
# plt.axis('equal')
# plt.show()