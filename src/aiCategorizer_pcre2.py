from openai import OpenAI
import json
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Enter your api key here
client = OpenAI()

models = ["gpt-3.5-turbo", "ft:gpt-3.5-turbo-1106:personal:changelog-pcre2:95whKLu9"]
file_names = ['pcre2_test', 'pcre2_train','pcre2_all']
for file_name in file_names:

    data_path = file_name + ".jsonl"
    output_files = [file_name + "_output_base.jsonl", file_name + "_output_ft.jsonl"]
    for output_file, model in zip(output_files, models):
        print(f'Processing {data_path} using {model}')

        # Load the dataset
        with open(data_path, 'r', encoding='utf-8') as f:
            dataset = [json.loads(line) for line in f]
            f.close()

        print(f'  Querying {len(dataset)} input messages for response')
        # Query model for responses
        completions = []
        for i in tqdm(range(len(dataset))):
            input_messages = dataset[i]['messages'][:2]

            completion = client.chat.completions.create(
                model=model,
                messages=input_messages
            )
            if len(dataset[i]['messages'])>2:
                expected_response = dataset[i]['messages'][2]['content']
            else:
                expected_response = None
            save_data = {'model':completion.model, 
                        'input_messages':input_messages,
                        'expected_response':expected_response,
                        'actual_response':completion.choices[0].message.content,
                        'finish_reason':completion.choices[0].finish_reason,
                        }
            completions.append(save_data)

        # Write results to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for completion in completions:
                json.dump(completion, f)
                f.write('\n')
            f.close()
        print(f'  Saved responses to {output_file}')
        