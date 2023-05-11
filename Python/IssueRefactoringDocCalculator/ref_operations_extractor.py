import re
from csv import DictWriter

refactorings_reg_exps = ['(?P<Change>^Change Variable Type|^Change Parameter Type|^Change Return Type|^Change Attribute Type|^Change Thrown Exception Type|^Change Type Declaration Type)', 
                         '(?P<Move>^Move |^Pull Up|^Push Down|and Move Method)', 
                         '(?P<Inline>^Inline |^Merge |and Inline Method)', 
                         '(?P<Rename>^Rename |and Rename Class|and Rename Method|and Rename Attribute)', 
                         '(?P<Extract>^Extract Method|^Extract Superclass|^Extract Subclass|^Extract Class|^Extract and|^Extract Interface)']
refactorings_end_reg_exp = r"Developers have reported that \d+ commits involve refactoring but only \d+ involve refactoring operations"
refactorings_cluster_names = ['Change', 'Move', 'Inline', 'Rename', 'Extract']
refactorings_operations_dict = {name: 0 for name in refactorings_cluster_names}
with open(r"Java\consoleOutput", 'r') as input_file:
    line = input_file.readline()
    while line:
        if "Refactorings at" in line:
            while True:
                line = input_file.readline()
                if re.search(refactorings_end_reg_exp, line, re.I):
                    break
                for refactorings_reg_exp in refactorings_reg_exps:
                    matches = re.search(refactorings_reg_exp, line, re.I | re.M | re.DOTALL)
                    if matches:
                        groupdict = matches.groupdict()
                        refactorings_operations_dict[list(groupdict.keys())[0]] += 1
        line = input_file.readline()

with open(r"Python\IssueRefactoringDocCalculator\refactoring_operations_clustered_by_class.csv", 'w', newline = '') as output_csv:
    csv_writer = DictWriter(output_csv, fieldnames = refactorings_cluster_names)
    csv_writer.writeheader()
    csv_writer.writerow(refactorings_operations_dict)
    print(refactorings_operations_dict)
