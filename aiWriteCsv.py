"""
Convert a JSONL file with OpenAI responses from aiCategorizer to a CSV file
"""

import json
import csv

def load_responses_from_file(data_path):
    print(f'\n\nLoading {data_path}')

    # Load the dataset
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
        f.close()

    print(f'  Read {len(dataset)} lines')
    # dataset objects include the following fields:
    #  - model
    #  - input_messages
    #  - expected_response
    #  - actual_response
    #  - finish_reason

    return dataset

def exact_match(expected_response, model_response):
    result = expected_response == model_response
    return result

def similar_match(expected_response, model_response):
    import re

    e = expected_response.lower()
    a = model_response.lower()
    match = re.search(e, a)
    if match:
        return True
    else:
        return False

def prepare_csv_output(dataset, csv_data, headers):
    lines = [headers]
    ind_evolution = headers.index('Evolution?')
    print(f'{len(dataset)} Repsonses, {len(csv_data)} Rows')
    assert len(dataset)==len(csv_data)

    for d,row in zip(dataset, csv_data):
        # change_description = d['input_messages'][1]['content']
        response = d['actual_response']
        if exact_match('Evolution',response) or similar_match('Evolution',response):
            evolution = "Y"
        else:
            evolution = "N"
        row[ind_evolution] = evolution
        lines.append(row)
    return lines

def write_csv_file(data, name):
    with open(name,'w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        print(f'\nWriting {len(data)} rows of CSV output to {name}')
        csvwriter.writerows(data)
        csvfile.close()
    print('  Complete!\n')

def load_orig_data_from_csv(file):
    with open(file,'r',newline='') as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel')
    
        headers = next(csvreader)
        
        all_data = []
        for row in csvreader:
            all_data.append(row)

    return all_data, headers
    

def convert_jsonl_to_csv(name, csv_file):
    orig_data, headers = load_orig_data_from_csv(csv_file)
    
    jsonl_file = name + ".jsonl"    
    responses = load_responses_from_file(jsonl_file)

    csv_data = prepare_csv_output(responses, orig_data, headers)

    csv_file = name + ".csv"
    write_csv_file(csv_data, csv_file)


if __name__ == "__main__":
    # PCRE2 Changelog
    csv_file = 'data/ChangeLog_pcre2_all.csv'
    jsonl_file_name = 'data/pcre2_chlog_all_output_ft'
    convert_jsonl_to_csv(jsonl_file_name, csv_file)

    # PCRE Changelog
    csv_file = 'data/ChangeLog_pcre_all.csv'
    jsonl_file_name = 'data/pcre_chlog_all_output_ft'
    convert_jsonl_to_csv(jsonl_file_name, csv_file)

    # PyDriller Commits
    data_path = 'data/'
    repositories = ['v8','rust','pcre2','java','ICU']

    for repo_name in repositories:
        csv_file = data_path + repo_name + '_all.csv'
        jsonl_file_name = data_path + repo_name + '_all_output_ft'
        convert_jsonl_to_csv(jsonl_file_name, csv_file)
