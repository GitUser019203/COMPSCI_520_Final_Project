import re
import csv

# Contains the total number of issues that document refactoring in their titles and that developers have affirmed
# be linked to commits involving refactoring which contain refactoring operations according to RefactoringMiner.
total_num_issues = 0
issue_IDs = set()
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
            total_num_issues += 1

percent_5932_issues_with_refactoring = 100 * (len(issue_IDs) / 5932.00)
percent_detected_refactoring_in_issue_titles_with_refactoring_doc = 100 * (len(issue_IDs) / 11158.00)

with open(r"Python\IssueRefactoringDocCalculator\data.txt", 'w') as out_file:
    print("The total number of issues is 45323.", file = out_file)
    print("The total number of issues with refactoring documentation in their titles is 11194.", file = out_file)
    print(f"RefactoringMiner calculates that {len(issue_IDs)} or {percent_detected_refactoring_in_issue_titles_with_refactoring_doc}% of issues with refactoring documentation in their titles contained refactoring operations.", file = out_file)
    print("However, only 5932 of the issues have linked commits that developers have labelled as involving refactoring.", file = out_file)        
    print(f"Out of the 5932 issues, RefactoringMiner detects refactoring operations in only {len(issue_IDs)}.", file = out_file)
    print(f"Thus, according to RefactoringMiner only {percent_5932_issues_with_refactoring}% of the 5932 issues contained refactoring operations.", file = out_file)

issue_title_phrases_terms = ['REFACTOR','RECODE', 'REENGINEER', 
                             'REWRIT', 'EDIT', 'ADD', 'CHANG', 'CREAT', 
                             'EXTEND', 'EXTRACT', 'FIX', 'IMPROV', 'INLIN', 
                             'INTRODUC', 'MERG', 'MOV', 'REPACKAG', 'REDESIGN', 
                             'REDUC', 'REFIN', 'REMOV', 'RENAM', 'REORGANIZ', 
                             'REPLAC', 'RESTRUCTUR', 'SPLIT', 'CHANGTHENAME',
                             'CLEANUPCODE', 'CLEANUP', 'CODECLEAN', 
                             'CODEOPTIMIZATION',
                             'FIXCODESTYLE', 'IMPROVCODEQUALITY', 'PULLUP', 
                             'PUSHDOWN',
                             'SIMPLIFYCODE']
issue_title_phrases_terms_dict = {}
for phrase_term in issue_title_phrases_terms:
    issue_title_phrases_terms_dict[phrase_term] = 0

issue_title_reg_exps = {}
with open(r"Python\IssueRefactoringDocCalculator\reg_exp_grouped.txt", 'r') as input_file:
    for phrase_term in issue_title_phrases_terms:
        issue_title_reg_exps[phrase_term] = input_file.readline().strip()

current_issue_ID = ""
with open(r"Python\mongo_db_extract_refactoring_doc.txt", encoding='utf-8') as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break
        if "Issue Description:" in line:
            if current_issue_ID in issue_IDs:
                issue_IDs.remove(current_issue_ID)
                issue_desc = line[19:]
                while True:
                    line = input_file.readline()
                    if "Linked Commit Revision Hash" in line:
                        break
                    else:
                        issue_desc += line
                for phrase_term in issue_title_reg_exps:
                    matches = re.search(issue_title_reg_exps[phrase_term], issue_desc, re.I | re.M | re.DOTALL)
                    if matches:
                        issue_title_phrases_terms_dict[phrase_term] += 1
        line = line.strip()
        if "Issue Title:" in line:
           issue_title = line[13:]
        elif "Issue Id:" in line:
            current_issue_ID = line[10:]
            if line[10:] in issue_IDs:
                for phrase_term in issue_title_reg_exps:
                    matches = re.search(issue_title_reg_exps[phrase_term], issue_title, re.I | re.M | re.DOTALL)
                    if matches:
                        issue_title_phrases_terms_dict[phrase_term] += 1

with open(r"Python\IssueRefactoringDocCalculator\issue_title_refactoring_doc_text_patterns.csv", 'w', newline='') as output_csv:
    csv_writer = csv.DictWriter(output_csv, fieldnames = issue_title_phrases_terms)
    csv_writer.writeheader()
    percentages_dict = {pattern: ((100.0 * issue_title_phrases_terms_dict[pattern]) / sum([issue_title_phrases_terms_dict[pattern] for pattern in issue_title_phrases_terms_dict])) for pattern in issue_title_phrases_terms_dict}
    csv_writer.writerow(percentages_dict)
    csv_writer.writerow(issue_title_phrases_terms_dict)