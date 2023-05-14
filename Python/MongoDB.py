import re
from copy import deepcopy
from csv import DictReader, DictWriter
from sys import argv
from multiprocessing import cpu_count
from threading import Thread
from queue import Queue
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string
from Python.stopwatch import StopWatch

refactorings_reg_exps = ['(?P<Change>^Change_Variable_Type|^Change_Parameter_Type|^Change_Return_Type|^Change_Attribute_Type|^Change_Thrown_Exception_Type|^Change_Type_Declaration_Type)', 
                         '(?P<Move>^Move_|^Pull_Up|^Push_Down|and_Move_Method)', 
                         '(?P<Inline>^Inline_|^Merge_|and_Inline_Method)', 
                         '(?P<Rename>^Rename_|and_Rename_Class|and_Rename_Method|and_Rename_Attribute)', 
                         '(?P<Extract>^Extract_Method|^Extract_Superclass|^Extract_Subclass|^Extract_Class|^Extract_and|^Extract_Interface)']
refactorings_cluster_names = ['Change', 'Move', 'Inline', 'Rename', 'Extract']
refactorings_operations_dict = {name: 0 for name in refactorings_cluster_names}


issue_refactoring_phrases_terms = ['REFACTOR','RESTRUCTUR', 'RECODE', 'REENGINEER', 
                             'REWRIT', 'EDIT', 'ADD', 'CHANG', 'CREAT', 
                             'EXTEND', 'EXTRACT', 'FIX', 'IMPROV', 'INLIN', 
                             'INTRODUC', 'MERG', 'MOV', 'REPACKAG', 'REDESIGN', 
                             'REDUC', 'REFIN', 'REMOV', 'RENAM', 'REORGANIZ', 
                             'REPLAC', 'SPLIT', 'CHANGTHENAME',
                             'CLEANUPCODE', 'CLEANUP', 'CODECLEAN', 
                             'CODEOPTIMIZATION',
                             'FIXCODESTYLE', 'IMPROVCODEQUALITY', 'PULLUP', 
                             'PUSHDOWN',
                             'SIMPLIFYCODE']
issue_refactoring_phrases_terms_dict = {}
for phrase_term in issue_refactoring_phrases_terms:
    issue_refactoring_phrases_terms_dict[phrase_term] = 0

issue_refactoring_phrases_terms_dict_all_match = deepcopy(issue_refactoring_phrases_terms_dict)
issue_refactoring_phrases_terms_dict_any_match = deepcopy(issue_refactoring_phrases_terms_dict)

with open(r"Python\issue_tracked_projects.txt",'r') as file:
    for line in file:
        project_data = line.strip().split(',')

issue_refactoring_reg_exps = {}
with open(r"Python\IssueRefactoringDocCalculator\reg_exp_grouped.txt", 'r') as input_file:
    for phrase_term in issue_refactoring_phrases_terms:
        issue_refactoring_reg_exps[phrase_term] = input_file.readline().strip()

with open(r"Python\IssueRefactoringDocCalculator\refactoring_motivations.csv", 'r', encoding = 'utf-8-sig') as motivations_csv:
    motivations_reader = DictReader(motivations_csv)
    motivations = {field_name: [] for field_name in motivations_reader.fieldnames}
    for row in motivations_reader:
        [motivations[key].append(row[key]) for key in row if row[key]]

motivations_dict = {category: {keyword: 0 for keyword in motivations[category]} for category in motivations}

if argv[0] == 'Preston':
    db_user = 'root'
    db_password = 'mongoElise2024'
else:
    db_user = ''
    db_password = ''

# You may have to update this dict to match your DB credentials
credentials = {'db_user': db_user,
               'db_password': db_password,
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

uri = create_mongodb_uri_string(**credentials)

mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

commit_queue = Queue()
def commitMiningWorker():
    while True:
        commit = commit_queue.get()
        refactorings = Refactoring.objects(commit_id=commit.id)
        if refactorings.count() > 0:
            for linked_issue_id in commit.linked_issue_ids:
                for issue in Issue.objects(id=linked_issue_id):
                    if issue.title is not None and issue.desc is not None and commit.message is not None :
                        title_match_list = []
                        msg_match_list = []
                        desc_match_list = []
                        if issue.id not in unique_issues:
                            for phrase_term in issue_refactoring_phrases_terms:
                                title_match_list.append(re.search(issue_refactoring_reg_exps[phrase_term], issue.title, re.I | re.M | re.DOTALL))
                                msg_match_list.append(re.search(issue_refactoring_reg_exps[phrase_term], commit.message, re.I | re.M | re.DOTALL))
                                desc_match_list.append(re.search(issue_refactoring_reg_exps[phrase_term], issue.desc, re.I | re.M | re.DOTALL))
                                
                                if any(title_match_list) and any(msg_match_list):
                                    for match in title_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for match in desc_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for category in motivations:
                                        for reg_exp in motivations[category]:
                                            mot_title_matches = re.search(reg_exp, issue.title, re.I | re.M | re.DOTALL)
                                            mot_desc_matches = re.search(reg_exp, issue.desc, re.I | re.M | re.DOTALL)
                                            mot_msg_matches = re.search(reg_exp, commit.message, re.I | re.M | re.DOTALL)
                                            if any([mot_title_matches, mot_desc_matches, mot_msg_matches]):
                                                motivations_dict[category][reg_exp] += 1
                                    for refactoring in refactorings:
                                        for refactoring_reg_exp in refactorings_reg_exps:
                                            r_matches = re.search(refactoring_reg_exp, refactoring.type, re.I)
                                            if r_matches:
                                                refactorings_operations_dict[list(r_matches.groupdict().keys())[0]] += 1
                                    unique_issues.add(issue.id)
                                    

                        for phrase_term in issue_refactoring_phrases_terms:
                            title_matches = re.search(issue_refactoring_reg_exps[phrase_term], issue.title, re.I | re.M | re.DOTALL)
                            desc_matches = re.search(issue_refactoring_reg_exps[phrase_term], issue.desc, re.I | re.M | re.DOTALL)
                            msg_matches = re.search(issue_refactoring_reg_exps[phrase_term], commit.message, re.I | re.M | re.DOTALL)
                                
                            if title_matches and desc_matches and msg_matches:
                                issue_refactoring_phrases_terms_dict_all_match[phrase_term] += 1
                            if any([title_matches, desc_matches, msg_matches]):
                                issue_refactoring_phrases_terms_dict_any_match[phrase_term] += 1
                                
        commit_queue.task_done()

projectCollection = [Project.objects(name=project_name) for project_name in project_data]
unique_issues = set()
stopwatch = StopWatch()
stopwatch.start()
for projects in projectCollection:
    for project in projects:
        vcs_system_reported_refactoring = False

        # We now select the version control system of the project
        vcs_system = VCSSystem.objects(project_id=project.id).get()

        # We can now grab the commits in the VCS system
        commits = Commit.objects(vcs_system_id=vcs_system.id)

        for commit in commits:
            commit_queue.put(commit)

        for i in range(0, 2):
            Thread(target = commitMiningWorker, daemon = True).start()
        commit_queue.join()
        print('All work completed')
stopwatch.stop()
stopwatch.get_elapsed_time()

with open(r"Python\IssueRefactoringDocCalculator\issue_refactoring_doc_text_patterns.csv", 'w', newline='') as output_csv:
    csv_writer = DictWriter(output_csv, fieldnames = issue_refactoring_phrases_terms)
    csv_writer.writeheader()
    percentages_dict = {pattern: ((100.0 * issue_refactoring_phrases_terms_dict[pattern]) / sum([issue_refactoring_phrases_terms_dict[pattern] for pattern in issue_refactoring_phrases_terms_dict])) for pattern in issue_refactoring_phrases_terms_dict}
    csv_writer.writerow(percentages_dict)
    csv_writer.writerow(issue_refactoring_phrases_terms_dict)

with open(r"Python\IssueRefactoringDocCalculator\refactoring_operations_clustered_by_class.csv", 'w', newline = '') as output_csv:
    csv_writer = DictWriter(output_csv, fieldnames = list(refactorings_operations_dict.keys()))
    csv_writer.writeheader()
    csv_writer.writerow(refactorings_operations_dict)

total_motivations = sum([sum([motivations_dict[category][keyword] for keyword in motivations_dict[category]]) for category in motivations_dict])
motivations_percentages_dict = {category: {keyword: (100 * motivations_dict[category][keyword] / total_motivations) for keyword in motivations_dict[category] if motivations_dict[category][keyword] != 0} for category in motivations_dict}
internal_qas = {keyword: motivations_dict['Internal'][keyword] for keyword in motivations_dict['Internal'] if motivations_dict['Internal'][keyword] != 0}
with open(r"Python\IssueRefactoringDocCalculator\refactoring_motivations_internal_qas.csv", 'w', newline = '') as internal_qas_csv:
    internal_qas_writer = DictWriter(internal_qas_csv, fieldnames = list(internal_qas.keys()))
    internal_qas_writer.writeheader()
    internal_qas_writer.writerow(motivations_percentages_dict['Internal'])
    internal_qas_writer.writerow(internal_qas)

external_qas = {keyword: motivations_dict['External'][keyword] for keyword in motivations_dict['External'] if motivations_dict['External'][keyword] != 0}
with open(r"Python\IssueRefactoringDocCalculator\refactoring_motivations_external_qas.csv", 'w', newline = '') as external_qas_csv:
    external_qas_writer = DictWriter(external_qas_csv, fieldnames = list(external_qas.keys()))
    external_qas_writer.writeheader()
    external_qas_writer.writerow(motivations_percentages_dict['External'])
    external_qas_writer.writerow(external_qas)

code_smells = {keyword: motivations_dict['Code Smell'][keyword] for keyword in motivations_dict['Code Smell'] if motivations_dict['Code Smell'][keyword] != 0}
with open(r"Python\IssueRefactoringDocCalculator\refactoring_motivations_code_smells.csv", 'w', newline = '') as code_smells_csv:
    code_smells_writer = DictWriter(code_smells_csv, fieldnames = list(code_smells.keys()))
    code_smells_writer.writeheader()
    code_smells_writer.writerow(motivations_percentages_dict['Code Smell'])
    code_smells_writer.writerow(code_smells)

print(f"There are a total of {len(unique_issues)} issues documenting refactoring in their titles and in the messages of linked commits.")