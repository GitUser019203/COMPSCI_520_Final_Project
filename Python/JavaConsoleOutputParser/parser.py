from inspect import trace
import re

reg_pattern = re.compile('	at .*\(.*\)|Caused by:', re.I)
error_info_pattern = re.compile('.*Exception')
parsed_line_pattern = re.compile('Currently parsing line')
revison_hash_pattern = re.compile('Ignored revision|Processing')

error_list = []

with open("Python/JavaConsoleOutputParser/extracted_errors", 'w') as out_file:
    with open("Java/consoleOutput", 'r') as console_output:
        lines = console_output.readlines()
        trace_dict = {}
        for i in range(1, len(lines) + 1):
            if re.search(reg_pattern, lines[i - 1]):
                trace_dict[i] = lines[i - 1]
            else:
                error_list.append(trace_dict)
                trace_dict = {}
        for trace_dict in error_list:
            if trace_dict:
                found_error_info = False
                print('\n', file=out_file)
                for key in trace_dict:
                    print(f"{key}: {trace_dict[key].strip()}", file=out_file)
                for key in trace_dict:
                    line_number = int(key)
                    i = 1
                    while(not found_error_info):
                        if re.search(error_info_pattern, lines[line_number - i]):
                            print(f"Line about exception that occurred: {lines[line_number - i].strip()}", file=out_file)
                        if re.search(parsed_line_pattern, lines[line_number - i]):
                            print(f"Line that was being parsed: {lines[line_number - i].strip().replace('Currently', 'Was')}", file=out_file)
                            found_error_info = True
                        if re.search(revison_hash_pattern, lines[line_number - i]):
                            print(f"Line about revision hash that wasn't mined': {lines[line_number - i].strip()}", file=out_file)
                        i += 1
                        if line_number - i <= 1:
                            break
                print('\n', file=out_file)