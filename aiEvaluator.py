from openai import OpenAI
import json
from dotenv import load_dotenv


def load_dataset_from_file(data_path):
    print(f'\n\nLoading {data_path}')

    # Load the dataset
    with open(data_path, 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
        f.close()
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

def grade_responses(dataset):
    # Grade responses
    ind_correct = [0] * len(dataset)
    for i in range(len(dataset)):
        expected_response = (dataset[i]['expected_response'])
        model_response = dataset[i]['actual_response']
        finish_reason = dataset[i]['finish_reason']

        is_exact = exact_match(expected_response, model_response)
        is_similar = is_exact or similar_match(expected_response, model_response)

        if is_exact:
            ind_correct[i] = 1
        
        elif is_similar:
            ind_correct[i] = 2
            # print(f'    [SIMILAR] Expected: {expected_response}, but recieved: {model_response}')

        else:
            # Print incorrect responses
            # print(f'  [INCORRECT] Expected: {expected_response}, but recieved: {model_response}')
            # print(f'  {dataset[i]['input_messages'][-1]['content']}')
            # print(f'  Finish Reason: {finish_reason}')
            pass

    return ind_correct

def eval_file(data_path):

    dataset = load_dataset_from_file(data_path)

    ind_correct = grade_responses(dataset)

    # Evaluate results
    num_correct = sum([x>0 for x in ind_correct])
    num_trials = len(ind_correct)
    print(f'Model accuracy = {num_correct/num_trials*100:.1f}% [{data_path}]')


if __name__ == '__main__':
    file_names = ['pcre2_chlog_test', 
                  'pcre_chlog_test',
                  'v8_test',
                  'rust_test',
                  'pcre2_test',
                  'java_test',
                  'ICU_test',
                  ]
    data_dir = 'data/'
    for file_name in file_names:

        file_name = data_dir + file_name # append data directory to base file name
        data_paths = [file_name + "_output_base.jsonl", file_name + "_output_ft.jsonl"]
        for data_path in data_paths:
            eval_file(data_path)




