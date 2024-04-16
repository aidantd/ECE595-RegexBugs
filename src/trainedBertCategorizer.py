from transformers import BertTokenizer, BertForSequenceClassification
import json
import torch

dataTypeEvolution = 0
dataTypeMaintenance = 1

# # Aidan Mac: /Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/
# # Aidan Linux: /home/aidan/Documents/School/ECE595/ECE595-RegexBugs/

def main():
    # Load pre-trained tokenizer and model
    tokenizer = BertTokenizer.from_pretrained("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/models")
    model = BertForSequenceClassification.from_pretrained("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/models", num_labels=2)

    model.eval()

    with open("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/categorizationsRE2_sorted_2.txt", 'w') as output_file:
        with open("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/uncategorizedData/re2_commits copy_sorted.jsonl", 'r') as file:
            commitsToCheck = []
            for commit in file:
                data = json.loads(commit)
                commitsToCheck.append(data["message"])

        currentCommit = 1
        totalCommits = len(commitsToCheck)

        for commitMessage in commitsToCheck:
            inputs = tokenizer(commitMessage, padding='max_length', truncation=True, max_length=128, return_tensors="pt")

            with torch.no_grad():
                outputs = model(**inputs)

            prediction = torch.argmax(outputs.logits, dim=1).item()
            if prediction == dataTypeEvolution:
                category = "Evolution"
            else:
                category = "Maintenance"

            output_file.write("----------------------------------------------------------------------" + "\n")
            output_file.write("Category: " + category + "\n")
            output_file.write("Commit Msg: " + commitMessage + "\n")
            output_file.write("----------------------------------------------------------------------" + "\n")

            print("Have categorized commit " + str(currentCommit) + " out of " + str(totalCommits))
            currentCommit += 1

if __name__ == "__main__":
    main()
