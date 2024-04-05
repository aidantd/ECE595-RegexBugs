from transformers import AutoTokenizer, AutoModel
import json
import torch
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

dataTypeEvolution = 1
dataTypeMaintenance = 2

def getEmbedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def calculateCentroid(embeddings):
    return np.mean(embeddings, axis=0)


def parseTrainingData(dataType):
    parsedData = []
    if(dataType == dataTypeEvolution):
        with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingDataEvolution.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                parsedData.append(data["message"])

    elif(dataType == dataTypeMaintenance):
        with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingDataMaintenance.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                parsedData.append(data["message"])
    
    return parsedData



def main():
    evolutionJson = parseTrainingData(dataTypeEvolution)
    maintenanceJson = parseTrainingData(dataTypeMaintenance)

    # for content in evolutionJson:
    #     print("Contents:", content)

    # for content in maintenanceJson:
    #     print("Contents:", content)

    evolutionEmbeddings = [getEmbedding(data) for data in evolutionJson]
    maintenanceEmbeddings = [getEmbedding(data) for data in maintenanceJson]

    evolutionCentroid = calculateCentroid(evolutionEmbeddings)
    maintenanceCentroid = calculateCentroid(maintenanceEmbeddings)

    # # Aidan Mac: /Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/
    # # Aidan Linux: /home/aidan/Documents/School/ECE595/ECE595-RegexBugs/

    with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/categorizations.txt", 'w') as output_file:
        output_file.write("Categorization\n")
        output_file.write("-----------------------\n")

        with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/pcre_commits.jsonl", 'r') as file:
            commitsToCheck = [line.strip() for line in file.readlines()]

        totalCommits = len(commitsToCheck)
        currentCommit = 1

        for commit in commitsToCheck:
            embedding = getEmbedding(commit)
            # print(embedding + "\n")
            centroid = calculateCentroid(embedding)

            evolution_distance = np.linalg.norm(evolutionCentroid - centroid)
            maintenance_distance = np.linalg.norm(maintenanceCentroid - centroid)

            if evolution_distance < maintenance_distance:
                category = "Evolution"
            else:
                category = "Maintenance"

            output_file.write(category + "\n")

            print("Have categorized commit " + str(currentCommit) + " out of " + str(totalCommits))
            currentCommit += 1

if __name__ == "__main__":
    main()