import re
from logging import debug, warning, error
from os import path, listdir
from copy import deepcopy
from csv import DictReader, DictWriter
from sys import argv
from multiprocessing import cpu_count
from threading import Thread
from json import dumps
from queue import Queue
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, File, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string
from Python.stopwatch import StopWatch
from Python.NLTK.issueTitlesModel import IssueTitlesModel
from Python.NLTK.issueDescriptionsModel import IssueDescriptionsModel
from Python.NLTK.issueLinkedCommitsModel import IssueLinkedCommitsModel

def escape(regular_expression):
    chars_to_escape = ["-", "[", "]", ".", "~", "#", "$", "^", "&", "*", "(", ")", "+", "|", "}", "{", "?"]
    regular_expression = regular_expression.replace("\\", "\\\\")
    for character in chars_to_escape:
        regular_expression = regular_expression.replace(character, f"\\{character}")
    return regular_expression


refactoring_types_regular_expressions = ['(?P<Change>^Change[_ ]Variable[_ ]Type|^Change[_ ]Parameter[_ ]Type|^Change[_ ]Return[_ ]Type|^Change[_ ]Attribute[_ ]Type|^Change[_ ]Thrown[_ ]Exception[_ ]Type|^Change[_ ]Type[_ ]Declaration[_ ]Type)', 
                         '(?P<Move>^Move[_ ]|^Pull[_ ]Up|^Push[_ ]Down|and[_ ]Move[_ ]Method)', 
                         '(?P<Inline>^Inline[_ ]|^Merge[_ ]|and[_ ]Inline[_ ]Method)', 
                         '(?P<Rename>^Rename[_ ]|and[_ ]Rename[_ ]Class|and[_ ]Rename[_ ]Method|and[_ ]Rename[_ ]Attribute)', 
                         '(?P<Extract>^Extract[_ ]Method|^Extract[_ ]Superclass|^Extract[_ ]Subclass|^Extract[_ ]Class|^Extract[_ ]and|^Extract[_ ]Interface)']
html_refactorings_regular_expressions = ['(?P<Change><b>Change Variable Type|<b>Change Parameter Type|<b>Change Return Type|<b>Change Attribute Type|<b>Change Thrown Exception Type|<b>Change Type Declaration Type)', 
                         '(?P<Move><b>Move |<b>Pull Up|<b>Push Down|and Move Method</b>)', 
                         '(?P<Inline><b>Inline |<b>Merge |and Inline Method</b>)', 
                         '(?P<Rename><b>Rename |and Rename Class</b>|and Rename Method</b>|and Rename Attribute</b>)', 
                         '(?P<Extract><b>Extract Method|<b>Extract Superclass|<b>Extract Subclass|<b>Extract Class|<b>Extract and|<b>Extract Interface)']
r_miner_finished_regular_expression = r"Developers have reported that \d+ commits involve refactoring but only \d+ involve refactoring operations"
refactoring_types_cluster_names = ['Change', 'Move', 'Inline', 'Rename', 'Extract']
issue_refactoring_documenting_expression_keys = ['REFACTOR','RESTRUCTUR', 'RECODE', 'REENGINEER', 
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

# Load the issue titles model, descriptions model and linked commits model from JSON files.
issue_titles_model = IssueTitlesModel()
issue_titles_model.load()
linked_commit_messages_model = IssueLinkedCommitsModel(issue_titles_model=issue_titles_model)
linked_commit_messages_model.load()
issue_descriptions_model = IssueDescriptionsModel(issue_titles_model=issue_titles_model, issue_linked_commits_model=linked_commit_messages_model)
issue_descriptions_model.load()

# Initialize the dictionary containing the number of refactoring operations per refactoring operation cluster
refactorings_operations_dict = {name: 0 for name in refactoring_types_cluster_names}

# Initialize the dictionary storing the numbers of occurrences of different expressions in issue refactoring documentation
issue_refactoring_phrases_terms_dict = {}
for phrase_term in issue_refactoring_documenting_expression_keys:
    issue_refactoring_phrases_terms_dict[phrase_term] = 0
issue_refactoring_phrases_terms_dict_all_match = deepcopy(issue_refactoring_phrases_terms_dict)
issue_refactoring_phrases_terms_dict_any_match = deepcopy(issue_refactoring_phrases_terms_dict)

print('Initializing the dictionary containing the number of times each regular expression group was matches in issue refactoring documentation')
# Initialize the dictionary containing the number of times each regular expression group was matched in issue refactoring documentation
issue_title_refactoring_documentation_regular_expression_groups = {}
issue_desc_refactoring_documentation_regular_expression_groups = {}
linked_commit_msgs_refactoring_documentation_regular_expression_groups = {}

with open(r"Python\NLTK\reg_exp_grouped.txt", 'r') as input_file:
    for phrase_term in issue_refactoring_documenting_expression_keys:
        if phrase_term.casefold() in issue_titles_model.keywords:
            titles_phrases_list = ["[^0-9^a-z^A-Z]" + escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "[^0-9^a-z^A-Z]" + escape(phrase) + "$" + "|" +  "^" + escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "^" + escape(phrase) + "$" for phrase in issue_titles_model.refactoring_documentation_patterns_phrases[phrase_term.casefold()]]
            issue_title_refactoring_documentation_regular_expression_groups[phrase_term] =  f"(?P<{phrase_term}>" + "|".join(titles_phrases_list) + ")"
            desc_phrases_list = ["[^0-9^a-z^A-Z]" + escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "[^0-9^a-z^A-Z]" + escape(phrase) + "$" + "|" +  "^" + escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "^" + escape(phrase)+ "$" for phrase in issue_descriptions_model.refactoring_documentation_patterns_phrases[phrase_term.casefold()]]
            issue_desc_refactoring_documentation_regular_expression_groups[phrase_term] =  f"(?P<{phrase_term}>" + "|".join(desc_phrases_list) + ")"
            linked_commit_msgs_phrases_list = ["[^0-9^a-z^A-Z]" +escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "[^0-9^a-z^A-Z]" + escape(phrase) + "$" + "|" +  "^" + escape(phrase) + "[^0-9^a-z^A-Z]" + "|" + "^" + escape(phrase) + "$" for phrase in linked_commit_messages_model.refactoring_documentation_patterns_phrases[phrase_term.casefold()]]
            linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term] =  f"(?P<{phrase_term}>" + "|".join(linked_commit_msgs_phrases_list) + ")"
            input_file.readline().strip()
        else:
            line = input_file.readline().strip()
            issue_title_refactoring_documentation_regular_expression_groups[phrase_term] = line
            issue_desc_refactoring_documentation_regular_expression_groups[phrase_term] = line
            linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term] = line

print('Initializing the dictionary containing the number of times a refactoring purpose regular expression was matches in issue refactoring documentation')

# Initialize the dictionary containing the number of times a refactoring purpose regular expression was matches in issue refactoring documentation
with open(r"Python\NLTK\refactoring_motivations.csv", 'r', encoding = 'utf-8-sig') as motivations_csv:
    motivations_reader = DictReader(motivations_csv)
    refactoring_motivations = {field_name: [] for field_name in motivations_reader.fieldnames}
    for row in motivations_reader:
        [refactoring_motivations[key].append(row[key]) for key in row if row[key]]
refactoring_motivations_dict = {category: {keyword: 0 for keyword in refactoring_motivations[category]} for category in refactoring_motivations}

# Assign db_user and db_password depending on cmd arguments.
if argv[0] == '':
    db_user = ''
    db_password = ''
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

print('Connecting to the MongoDB server.')
uri = create_mongodb_uri_string(**credentials)
mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

unique_issues = set()
commit_queue = Queue()
def commitMiningWorker():
    while True:
        commit = commit_queue.get()
        refactorings = Refactoring.objects(commit_id=commit.id)
        if refactorings.count() > 0:
            #if "git-svn-id" in commit.message and not commit.linked_issue_ids:
            #    print(commit)
            # This commit emailed 
            for linked_issue_id in commit.linked_issue_ids:
                for issue in Issue.objects(id=linked_issue_id):
                    if issue.title is not None and issue.desc is not None and commit.message is not None :
                        title_match_list = []
                        msg_match_list = []
                        desc_match_list = []
                        if issue.id not in unique_issues:
                            for phrase_term in issue_refactoring_documenting_expression_keys:
                                 if phrase_term in ["REPACKAG", "REDESIGN"]:
                                     continue

                                 title_match_list.append(re.search(issue_title_refactoring_documentation_regular_expression_groups[phrase_term], issue.title, re.I | re.M | re.DOTALL))
                                 msg_match_list.append(re.search(linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term], commit.message, re.I | re.M | re.DOTALL))
                                 desc_match_list.append(re.search(issue_desc_refactoring_documentation_regular_expression_groups[phrase_term], issue.desc, re.I | re.M | re.DOTALL))
                                
                                
                                 if any(title_match_list) and any(msg_match_list):
                                    # Save the issue selected to a json file with the UTF-8 encoding instead of using the cp1252 encoding.
                                    #with open("Python\\NLTK\\SelectedIssues\\" + str(commit.id) + ".json", 'w', encoding='utf-8') as out_json:
                                    #    out_json.write(dumps({'Linked Issue ID': str(issue.id), 
                                    #                          'Linked Issue Title': issue.title, 
                                    #                          "Linked Issue Description": issue.desc,                                                               
                                    #                          "Commit Revision Hash": str(commit.revision_hash),
                                    #                          "Commit Message": commit.message}, indent = '\t'))

                                    for match in title_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for match in desc_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for category in refactoring_motivations:
                                        for reg_exp in refactoring_motivations[category]:
                                            mot_title_matches = re.search(reg_exp, issue.title, re.I | re.M | re.DOTALL)
                                            mot_desc_matches = re.search(reg_exp, issue.desc, re.I | re.M | re.DOTALL)
                                            mot_msg_matches = re.search(reg_exp, commit.message, re.I | re.M | re.DOTALL)
                                            if any([mot_title_matches, mot_desc_matches, mot_msg_matches]):
                                                refactoring_motivations_dict[category][reg_exp] += 1
                                    for refactoring in refactorings:
                                        for refactoring_reg_exp in refactoring_types_regular_expressions:
                                            r_matches = re.search(refactoring_reg_exp, refactoring.type, re.I)
                                            if r_matches:
                                                refactorings_operations_dict[list(r_matches.groupdict().keys())[0]] += 1
                                    unique_issues.add(issue.id)

                        for phrase_term in issue_refactoring_documenting_expression_keys:
                            
                            title_matches = re.search(issue_title_refactoring_documentation_regular_expression_groups[phrase_term], issue.title, re.I | re.M | re.DOTALL)
                            msg_matches = re.search(linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term], commit.message, re.I | re.M | re.DOTALL)
                            desc_matches = re.search(issue_desc_refactoring_documentation_regular_expression_groups[phrase_term], issue.desc, re.I | re.M | re.DOTALL)
                                
                            if title_matches and desc_matches and msg_matches:
                                issue_refactoring_phrases_terms_dict_all_match[phrase_term] += 1
                            if any([title_matches, desc_matches, msg_matches]):
                                issue_refactoring_phrases_terms_dict_any_match[phrase_term] += 1
                                
        commit_queue.task_done()

print('Starting to mine the 68 projects with the SmartSHARK database information.')
projectCollection = Project.objects()
stopwatch = StopWatch()
stopwatch.start()
for j, project in enumerate(projectCollection):
    print(f"Starting mining project #{j} named {project.name}")
    # We now select the version control system of the project
    vcs_system = VCSSystem.objects(project_id=project.id).get()
        
    # We can now grab the commits in the VCS system
    commits = Commit.objects(vcs_system_id=vcs_system.id)
    
    for commit in commits:
        #commit_queue.put(commit)
        refactorings = Refactoring.objects(commit_id=commit.id)
        if refactorings.count() > 0:
            #if "git-svn-id" in commit.message and not commit.linked_issue_ids:
            #    print(commit)
            # This commit emailed 
            for linked_issue_id in commit.linked_issue_ids:
                for issue in Issue.objects(id=linked_issue_id):
                    if issue.title is not None and issue.desc is not None and commit.message is not None :
                        title_match_list = []
                        msg_match_list = []
                        desc_match_list = []
                        if issue.id not in unique_issues:
                            for phrase_term in issue_refactoring_documenting_expression_keys:
                                 if phrase_term in ["REPACKAG", "REDESIGN"]:
                                     continue

                                 title_match_list.append(re.search(issue_title_refactoring_documentation_regular_expression_groups[phrase_term], issue.title, re.I | re.M | re.DOTALL))
                                 msg_match_list.append(re.search(linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term], commit.message, re.I | re.M | re.DOTALL))
                                 desc_match_list.append(re.search(issue_desc_refactoring_documentation_regular_expression_groups[phrase_term], issue.desc, re.I | re.M | re.DOTALL))
                                
                                
                                 if any(title_match_list) and any(msg_match_list):
                                    # Save the issue selected to a json file with the UTF-8 encoding instead of using the cp1252 encoding.
                                    #with open("Python\\NLTK\\SelectedIssues\\" + str(commit.id) + ".json", 'w', encoding='utf-8') as out_json:
                                    #    out_json.write(dumps({'Linked Issue ID': str(issue.id), 
                                    #                          'Linked Issue Title': issue.title, 
                                    #                          "Linked Issue Description": issue.desc,                                                               
                                    #                          "Commit Revision Hash": str(commit.revision_hash),
                                    #                          "Commit Message": commit.message}, indent = '\t'))

                                    for match in title_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for match in desc_match_list:
                                        if match:
                                            keyword = list(match.groupdict().keys())[0]
                                            issue_refactoring_phrases_terms_dict[keyword] += 1
                                    for category in refactoring_motivations:
                                        for reg_exp in refactoring_motivations[category]:
                                            mot_title_matches = re.search(reg_exp, issue.title, re.I | re.M | re.DOTALL)
                                            mot_desc_matches = re.search(reg_exp, issue.desc, re.I | re.M | re.DOTALL)
                                            mot_msg_matches = re.search(reg_exp, commit.message, re.I | re.M | re.DOTALL)
                                            if any([mot_title_matches, mot_desc_matches, mot_msg_matches]):
                                                refactoring_motivations_dict[category][reg_exp] += 1
                                    for refactoring in refactorings:
                                        for refactoring_reg_exp in refactoring_types_regular_expressions:
                                            r_matches = re.search(refactoring_reg_exp, refactoring.type, re.I)
                                            if r_matches:
                                                refactorings_operations_dict[list(r_matches.groupdict().keys())[0]] += 1
                                    unique_issues.add(issue.id)

                        for phrase_term in issue_refactoring_documenting_expression_keys:
                            
                            title_matches = re.search(issue_title_refactoring_documentation_regular_expression_groups[phrase_term], issue.title, re.I | re.M | re.DOTALL)
                            msg_matches = re.search(linked_commit_msgs_refactoring_documentation_regular_expression_groups[phrase_term], commit.message, re.I | re.M | re.DOTALL)
                            desc_matches = re.search(issue_desc_refactoring_documentation_regular_expression_groups[phrase_term], issue.desc, re.I | re.M | re.DOTALL)
                                
                            if title_matches and desc_matches and msg_matches:
                                issue_refactoring_phrases_terms_dict_all_match[phrase_term] += 1
                            if any([title_matches, desc_matches, msg_matches]):
                                issue_refactoring_phrases_terms_dict_any_match[phrase_term] += 1

    #for i in range(0, 2):
    #    Thread(target = commitMiningWorker, daemon = True).start()
    #commit_queue.join()
    print(f'Completed mining {project.name}')
stopwatch.stop()
stopwatch.get_elapsed_time()

print('Writing collected information to CSV files.')

with open(r"Python\NLTK\issue_refactoring_doc_text_patterns.csv", 'w', newline='') as output_csv:
    csv_writer = DictWriter(output_csv, fieldnames = issue_refactoring_documenting_expression_keys)
    csv_writer.writeheader()
    percentages_dict = {pattern: ((100.0 * issue_refactoring_phrases_terms_dict[pattern]) / sum([issue_refactoring_phrases_terms_dict[pattern] for pattern in issue_refactoring_phrases_terms_dict])) for pattern in issue_refactoring_phrases_terms_dict}
    csv_writer.writerow(percentages_dict)
    csv_writer.writerow(issue_refactoring_phrases_terms_dict)

with open(r"Python\NLTK\refactoring_operations_clustered_by_class.csv", 'w', newline = '') as output_csv:
    csv_writer = DictWriter(output_csv, fieldnames = list(refactorings_operations_dict.keys()))
    csv_writer.writeheader()
    csv_writer.writerow(refactorings_operations_dict)

total_motivations = sum([sum([refactoring_motivations_dict[category][keyword] for keyword in refactoring_motivations_dict[category]]) for category in refactoring_motivations_dict])
motivations_percentages_dict = {category: {keyword: (100 * refactoring_motivations_dict[category][keyword] / total_motivations) for keyword in refactoring_motivations_dict[category] if refactoring_motivations_dict[category][keyword] != 0} for category in refactoring_motivations_dict}
internal_qas = {keyword: refactoring_motivations_dict['Internal'][keyword] for keyword in refactoring_motivations_dict['Internal'] if refactoring_motivations_dict['Internal'][keyword] != 0}
with open(r"Python\NLTK\refactoring_motivations_internal_qas.csv", 'w', newline = '') as internal_qas_csv:
    internal_qas_writer = DictWriter(internal_qas_csv, fieldnames = list(internal_qas.keys()))
    internal_qas_writer.writeheader()
    internal_qas_writer.writerow(motivations_percentages_dict['Internal'])
    internal_qas_writer.writerow(internal_qas)

external_qas = {keyword: refactoring_motivations_dict['External'][keyword] for keyword in refactoring_motivations_dict['External'] if refactoring_motivations_dict['External'][keyword] != 0}
with open(r"Python\NLTK\refactoring_motivations_external_qas.csv", 'w', newline = '') as external_qas_csv:
    external_qas_writer = DictWriter(external_qas_csv, fieldnames = list(external_qas.keys()))
    external_qas_writer.writeheader()
    external_qas_writer.writerow(motivations_percentages_dict['External'])
    external_qas_writer.writerow(external_qas)

code_smells = {keyword: refactoring_motivations_dict['Code Smell'][keyword] for keyword in refactoring_motivations_dict['Code Smell'] if refactoring_motivations_dict['Code Smell'][keyword] != 0}
with open(r"Python\NLTK\refactoring_motivations_code_smells.csv", 'w', newline = '') as code_smells_csv:
    code_smells_writer = DictWriter(code_smells_csv, fieldnames = list(code_smells.keys()))
    code_smells_writer.writeheader()
    code_smells_writer.writerow(motivations_percentages_dict['Code Smell'])
    code_smells_writer.writerow(code_smells)

print(f"There are a total of {len(unique_issues)} issues documenting refactoring.")