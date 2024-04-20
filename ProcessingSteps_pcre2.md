# Over-arching processing script for the PCRE2 Changelog file

## Getting started
Start with ChangeLog_pcre2.txt in the working directory. This is a download of the changelog file from the [official PCRE2 website](https://www.rexegg.com/pcre-doc/ChangeLog_pcre2).

Verify that the following files are available for running:
- parse_log.py
- truth_csv_to_jsonl.py
- aiCategorizer_chatgpt.py
- aiWriteCsv.py

Verify that the following packages are installed and ready to use by Python
- enum
- re
- csv
- openai
- json
- tqdm
- dotenv

To run OpenAI model queries for ChatGPT, you will need to make an account with OpenAI and download a copy of your personal API access key. Create a file named `.env` and paste the following code snippet followed by your API key without quotes or brackets.
```
# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=
```

## Pre-Processing Steps
To train a custom model, or test the accuracy of a given model, you will need to manually label several changes as either "Maintenance" or "Evolution". To assist with this task, `parse_log.py` will convert the original changelog text to an Excel file with a row for each text block in the change log. This will result in multiple change entries for a single revision number, but will be easier to label and process. This is also closer to how each commit is graded for changes in Git repositories.

1. Run `parse_log.py` to convert `ChangeLog_pcre2.txt` to `ChangeLog_pcre2.csv`
    >Note: The script expects all input files to be in the `data/` directory, and will put all output files there as well.
2. Open `ChangeLog_pcre2.csv` in Excel and add columns for "Evolution?", "New Features", and "Comments"
3. Label several changes as either "Y" or "N" in the "Evolution?" column
4. Save file as a CSV named `ChangeLog_pcre2_all.txt`
    
    >Note: This file will contain a mix of labeled and unlabeled changes

## Training a Fine-Tuned Model
Once you have labeled some data, you can use this data to train a custom fine-tuned model. The advantages of this are to improve accuracy of the AI output, as well as consistency of the response text for easier post-processing. Here, we will select half of the labeled changes for training and the rest for testing.

1. Run `truth_csv_to_jsonl.py` to create the training and test JSONL files
2. Using the OpenAI web portal, start a Fine-Tuning job of the ChatGPT-3.5-0125 model using `pcre2_train.jsonl` for the training set and `pcre2_test.jsonl` for the test/validation set.
3. When the Fine-Tuning job is complete, copy the name of the new fine-tuned model and paste it into `aiCategorizer_chatgpt.py` on line 11, replacing any existing fine-tuned model name.

## Using the models
Next, use OpenAI API to get responses from the base and fine-tuned models in Python.

1. Run `aiCategorizer_chatgpt.py` to query model responses for all data sets (train, test, and all JSONL files) from both the base and fine-tuned models. Model responses are saved in new JSONL files named `[engine]_[train/test/all]_output_[base/ft].jsonl`.
2. Run `aiWriteCsv.py` to append the responses from the model, e.g. `pcre2_all_output_ft.jsonl`, to the original csv file, e.g. `ChangeLog_pcre2.csv`, and save as a new csv file, e.g. `pcre2_all_output_ft.csv`.

## Evaluating each model
The accuracy of the AI responses should be evaulated against the test data set only. Evaluation against the training set is useful only to inspect for overfitting concerns. In general, accuracy of the fine-tuned model should be better than the base model, and have a more consistent output. Because of possible unexpected responses from the model, individual responses and the automated matching to "Maintenance" or "Evolution" should be inspected as well.

1. Run `aiEvaluator.py` to produce accuracy statistics from the test and train output files for each model.

    > Note: Only report on the accuracy of the test datasets! "Accuracy" of the training data set is provided only for awareness and inspection, and is not a valid measure of model accuracy.

2. Copy the command line output to a new file, `pcre2_trinaing_results.txt`, for later reference.
3. Inspect the matches for correctness and update code as needed to capture unexpected outputs.
4. Consider the accuracy of the fine-tuned model to determine if this model is suitable for use.


