import re
from csv import DictReader, DictWriter

with open(r"Python\IssueRefactoringDocCalculator\refactoring_motivations.csv", 'r', encoding='utf-8-sig') as motivations_csv:
    motivations_reader = DictReader(motivations_csv)
    motivations = {field_name: [] for field_name in motivations_reader.fieldnames}
    for row in motivations_reader:
        for key in row:
            if row[key]:
                motivations[key].append(row[key])
          
motivations_dict = {category: {keyword: 0 for keyword in motivations[category]} for category in motivations}

issue_IDs = set()
issue_IDs.add('5b45f71c56677a15366cc80d')
issue_IDs.add('5b45fc0e56677a15366cfacf')
issue_IDs.add('5c57f0cdcf244d7545c80d62')
issue_IDs.add('5c57f3d5cf244d7545c82c29')
issue_IDs.add('5c57f48ecf244d7545c834b7')
issue_ID_reg_exp = r"Issue ID: (?P<Issue_ID>.*)"
with open(r"Java\consoleOutput", 'r') as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break
        line = line.strip()
        matches = re.match(issue_ID_reg_exp, line, re.I | re.M | re.DOTALL)
        if matches:
            issue_IDs.add(matches.groupdict()['Issue_ID'][2:])

current_issue_ID = ""
areIssueTitlesOnlySingleLine = False
with open(r"Python\mongo_db_extract_refactoring_doc.txt", encoding='utf-8') as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break
        if areIssueTitlesOnlySingleLine is True and not ("Issue Id:" in line or "Issue Description" in line):
            print('Issue Titles can be multiline in the data.')
            exit(1)
        if "Issue Description:" in line:
            areIssueTitlesOnlySingleLine = False
            if current_issue_ID in issue_IDs:
                issue_IDs.remove(current_issue_ID)
                issue_desc = line[19:]
                while True:
                    line = input_file.readline()
                    if "Linked Commit Revision Hash" in line:
                        break
                    else:
                        issue_desc += line
                for category in motivations:
                    for reg_exp in motivations[category]:
                        matches = re.search(reg_exp, issue_desc, re.I | re.M | re.DOTALL)
                        if matches:
                            motivations_dict[category][reg_exp] += 1
        line = line.strip()
        if "Issue Title:" in line:
           issue_title = line[13:]
           areIssueTitlesOnlySingleLine = True
        elif "Issue Id:" in line:
            current_issue_ID = line[10:]
            if line[10:] in issue_IDs:
                for category in motivations:
                    for reg_exp in motivations[category]:
                        matches = re.search(reg_exp, issue_title, re.I | re.M | re.DOTALL)
                        if matches:
                            motivations_dict[category][reg_exp] += 1

internal_QAs = motivations_dict['Internal']
external_QAs = motivations_dict['External']
code_smells = motivations_dict['Code Smell']
print(motivations_dict)
print({category: {keyword: (100 * motivations_dict[category][keyword] / 5932) for keyword in motivations_dict[category] if motivations_dict[category][keyword] != 0} for category in motivations_dict})
