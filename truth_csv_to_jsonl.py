"""
truth_csv_to_jsonl.py - Convert Truth CSV Files to JSONL for fine-tuning OpenAI models
---------------------------------------------
To run, call from command line. 

Script will read the input files and create new JSONL files, or
overwrite existing files, that contain fine-tuning training
messages for OpenAI models.

Truth files currently supported:
- ChangeLog_pcre2_truth.csv
"""

"""
Created 03/21/2024
Michael Heinz
ECE59500 - Advanced Software Engineering, Purdue Univ.
Regex Bugs group project
"""

SYSTEM_ROLE = 'You will be provided a code change description. Indicate if this change is evolution or maintenance.'

from enum import Enum
class LogType(Enum):
    PCRE = 1
    PCRE2 = 2

class ChangeData:
    def __init__(self, ver, date, desc, is_evo) -> None:
        self.change_number = ver
        self.change_date = date
        self.description = desc
        self.is_evolution = is_evo


def read_truth_file_from_csv(truth_file):
    """
    Read truth data structure from a comma-separated values (CSV) file
    """
    counter = 0
    import csv
    with open(truth_file,'r',newline='') as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel')
    
        header = next(csvreader)
        print(f'File has the following headers:\n\t{', '.join(header)}')
        all_data = []
        for row in csvreader:
            version = row[0]
            change_date = row[1]
            change_description = row[2]
            if row[3] == '':
                # change not yet graded, skip
                is_evolution = None
            else:
                is_evolution = row[3].lower()=='y'
            all_data.append(ChangeData(version, change_date, change_description, is_evolution))
            counter += 1
    
        csvfile.close()    
    print(f'Read {counter} rows from {truth_file}')

    truth_data = []
    for change in all_data:
        if not change.is_evolution == None:
            truth_data.append(change)
    print(f'  {len(truth_data)} of {len(all_data)} included manual truth data\n')


    return truth_data, all_data

class OpenAIModelInputData:
    def __init__(self, system_role, user_input) -> None:
        self.system_role = system_role
        self.user_input = user_input.replace('"',"'").replace('\\','')

class TrainingData:
    def __init__(self, system_role, user_input, expected_output) -> None:
        self.system_role = system_role
        self.user_input = user_input.replace('"',"'").replace('\\','')
        self.expected_output = expected_output

def construct_truth_message_data(change_data, system_role=SYSTEM_ROLE):
    message_data = []

    for change in change_data:
        if change.is_evolution == None:
            continue
        elif change.is_evolution:
            expected_output = 'Evolution'
        else:
            expected_output = 'Maintenance'

        x = TrainingData(system_role, change.description, expected_output)
        message_data.append(x)

    return message_data

def construct_input_message_data(change_data, system_role=SYSTEM_ROLE):
    message_data = []

    for change in change_data:
        x = OpenAIModelInputData(system_role, change.description)
        message_data.append(x)

    return message_data

def convert_to_jsonl(message_data):
    output_text = []
    for message in message_data:
        system = '{"role": "system", "content": "' + message.system_role + '"}'
        user = '{"role": "user", "content": "' + message.user_input + '"}'
        if hasattr(message, 'expected_output'):
            expected = '{"role": "assistant", "content": "' + message.expected_output + '"}'
            line = '{"messages": [' + system + ', ' + user + ', ' + expected + ']}\n'
        else:
            line = '{"messages": [' + system + ', ' + user + ']}\n'
        output_text.append(line)
    return output_text

def write_jsonl(output_text, output_file):
    with open(output_file,'w',newline='\n') as f:
        f.writelines(output_text)
        f.close()
    print(f'Wrote {len(output_text)} lines to {output_file}')

def main(truth_file, output_file_prefix, log_type=LogType.PCRE):
    # Read truth file
    truth_data, all_data = read_truth_file_from_csv(truth_file)

    # Create output data structure
    message_data_train = construct_truth_message_data(truth_data[::2])
    message_data_test = construct_truth_message_data(truth_data[1::2])
    message_data_all = construct_input_message_data(all_data)

    # Create output text
    output_text_train = convert_to_jsonl(message_data_train)
    output_text_test = convert_to_jsonl(message_data_test)
    output_text_all = convert_to_jsonl(message_data_all)
    
    # Write Training data split to output file (_train.jsonl)
    write_jsonl(output_text_train, output_file_prefix + '_train.jsonl')
    write_jsonl(output_text_test, output_file_prefix + '_test.jsonl')
    write_jsonl(output_text_all, output_file_prefix + '_all.jsonl')


if __name__ == "__main__":
    main('data/ChangeLog_pcre2_all.csv', 'data/pcre2', LogType.PCRE)
