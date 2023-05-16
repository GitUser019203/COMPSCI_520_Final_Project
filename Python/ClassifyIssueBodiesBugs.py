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


def issueTitleBugCounter(issue_body_list: list, 
                   bug_id_keys: list, 
                   bug_class_keys: list, 
                   bug_fix_keys: list,
                   bug_report_keys: list) -> list:
    """
    Count number of Issue Bodies that exist, 
    plus number of Issue Bodies that are in one of the folowing bug types:
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
#        if any(word in i.lower() for word in bug_id_keys) or \
#                re.findall(r"^there.*(bug|problem)$", i) or \
#                re.findall(r"^cause.*(bug|problem)$", i):
#            counter_found += 1
#        elif any(word in i.lower() for word in bug_class_keys) or \
#                re.findall(r"bug#[0-9]+", i) or \
#                re.findall(r"bug #[0-9]+", i) or \
#                re.findall(r"bug[0-9]+", i) or \
#                re.findall(r"bug [0-9]+", i):
#            counter_bug_classify += 1
#        elif any(word in i.lower() for word in bug_fix_keys) or re.findall(r"^fix.*bug$", i):
#            counter_bug_fix += 1
#        elif any(word in i.lower() for word in bug_report_keys) or re.findall(r"^report.*bug$", i):
#            counter_bug_report += 1

        if any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in bug_class_keys):
            counter_bug_classify += 1
        elif any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in bug_fix_keys):
           counter_bug_fix += 1
        elif any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in bug_report_keys):
            counter_bug_report += 1
        elif any(re.search(r"\b{}\b".format(word), i, re.IGNORECASE) for word in bug_id_keys):
            counter_found += 1
    
    # Return list of all counters
    return [total_issues, counter_found, counter_bug_classify, counter_bug_fix, counter_bug_report]
    

# Get list of lines from filepath
lines = extractIssueDesc(filepath='./Python/extractedIssueDescBugs.txt')

# Identify list of keywords for specific 
#bug_identify_list = [
#     "exception",
#     "found.*bug", 
#     "found.*problem", 
#     "there.*bug", 
#     "there.* problem", 
#     "bug.*found", 
#     "problem.*found", 
#     "[Ii]t is.*bug", 
#     "[Ii]t is.*problem", 
#     "this is a bug",
#     "this is a problem", 
#     "this bug", 
#     "this problem", 
#     "catch this bug", 
#     "catch this problem", 
#     "catch.*bug", 
#     "catch.*problem", 
#     "caught.*bug",
#     "caught.*problem",
#     "these bug",
#     "these problem",
#     "other bug",
#     "other problem",
#     "following bug",
#     "following problem",
#     " of bug",
#     " of problem"
#     ]
bug_identify_list = [
    "find.*bug",
    "find.*problem",
    "there.*bug",
    "there.*problem",
    "bug.*found",
    "problem.*found",
    "it.*bug",
    "it.*problem",
    "this.*bug",
    "this.*problem",
    "catch.*bug",
    "catch.*problem",
    "caught.*bug",
    "caught.*problem",
    "these.*bug",
    "these.*problem",
    "other.*bug",
    "other.*problem",
    "follow.*bug",
    "follow.*problem",
    "find.*problem",
    "find.*unexpect.*behavior",
    "there.*issue",
    "there.*unexpect.*behavior",
    "issue.*found",
    "unexpect.*behavior*found",
    "it.*issue",
    "it.*unexpect.*behavior",
    "this.*issue",
    "this.*unexpect.*behavior",
    "catch.*issue",
    "catch.*unexpect.*behavior",
    "caught.*issue",
    "caught.*unexpect.*behavior",
    "these.*issue",
    "these.*unexpect.*behavior",
    "other.*issue",
    "other.*unexpect.*behavior",
    "follow.*issue",
    "follow.*unexpect.*behavior",
    "bug",
    "problem",
    "unexpected.*behavior"
]

bug_classify_list = [
    " bug#", 
    "bug is a",
    " error ",
    "defect",
    "crash",
    "infinite loop",
    "corruption",
    "inconsistent.*behavior",
    "performance.*issue",
    "deadlock",
    "memory.*leak"
    ]

bug_fix_list = [
     "bug.*fix",
     "fix.*bug",
     "patch.*bug",
     "patch.*issue",
     "patch.*problem",
     "resolv.*issue",
     "issue.*resol",
     "hotfix.*issue",
     "issue.*hotfix",
     "hotfix.*problem",
     "hotfix.*problem",
     "workaround.*bug",
     "bug.*workaround",
     "workaround.*problem",
     "problem.*workaround",
     "troubleshoot.*issue",
     "troubleshoot.*problem",
     ]
bug_report_list = [
     "bug.*report", 
     "report.*bug",
     "issue.*report", 
     "report.*issue",
     "problem.*report", 
     "report.*problem",
     "error.*report", 
     "report.*error",
     "unexpected.*behavior.*report", 
     "report.*unexpected.*behavior",
     ]

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

# Count number of issue titles and bug types
bug_counters = issueTitleBugCounter(issue_body_list=lines, 
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


# Create charts
def createPieChart(bug_type_counter: int, 
                   total_issues_count: int, 
                   bug_type_label: str,
                   total_issues_label: str):
    """
    Creates Pie Chart of the total number of bug_type out of total_issues
    :param: bug_type_counter: total number of bugs of a certain type (identify, classify, fixes, reports)
    :param: total_issues_count: total number of body issues
    :param: bug_type_label: Chart label for bug_type
    :param: total_issues_label: Chart label for total_issues
    """
    d = np.array([bug_type_counter, total_issues_count])
    myexplode = [0.2,0]
    fig1, ax1 = plt.subplots()
    plotLabel = [bug_type_label, total_issues_label]
    plt.pie(d, labels=plotLabel, explode=myexplode, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.show()


# Chart for Bug Identifications
createPieChart(bug_type_counter=counterFound,
               total_issues_count=totalIssues,
               bug_type_label="Issues about Bug Found",
               total_issues_label="Other Issues")

# Chart for Bug Classifications
createPieChart(bug_type_counter=counterBugClassify,
               total_issues_count=totalIssues,
               bug_type_label="Issues about Bug Classification",
               total_issues_label="Other Issues")

# Chart for Bug Fixes
createPieChart(bug_type_counter=counterBugFix,
               total_issues_count=totalIssues,
               bug_type_label="Issues about Bug Fixes",
               total_issues_label="Other Issues")

# Chart for Bug Reports
createPieChart(bug_type_counter=counterBugReport,
               total_issues_count=totalIssues,
               bug_type_label="Issues about Bug Reports",
               total_issues_label="Other Issues")
