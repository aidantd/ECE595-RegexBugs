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
        with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingData/trainingDataEvolution.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                parsedData.append(data["message"])

    elif(dataType == dataTypeMaintenance):
        with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingData/trainingDataMaintenance.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                parsedData.append(data["message"])
    
    return parsedData



def main():
    evolutionJson = parseTrainingData(dataTypeEvolution)
    maintenanceJson = parseTrainingData(dataTypeMaintenance)

    evolutionEmbeddings = [getEmbedding(data) for data in evolutionJson]
    maintenanceEmbeddings = [getEmbedding(data) for data in maintenanceJson]

    evolutionCentroid = calculateCentroid(evolutionEmbeddings)
    maintenanceCentroid = calculateCentroid(maintenanceEmbeddings)
    
    print("Evolution Centroid: " + str(evolutionCentroid) + "\n")
    print("Maintenance Centroid: " + str(maintenanceCentroid) + "\n")

    # # Aidan Mac: /Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/
    # # Aidan Linux: /home/aidan/Documents/School/ECE595/ECE595-RegexBugs/
    with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/categorizationsRE2.txt", 'w') as output_file:

        with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/uncategorizedData/re2_commits copy_sorted.jsonl", 'r') as file:
            commitsToCheck = []
            for commit in file:
                data = json.loads(commit)
                commitsToCheck.append(data["message"])

        currentCommit = 1
        totalCommits = len(commitsToCheck)

        for commitMessage in commitsToCheck:
            embedding = getEmbedding(commitMessage)
            # print(embedding + "\n")
            centroid = calculateCentroid(embedding)

            # evolution_distance = np.linalg.norm(evolutionCentroid - centroid)
            # maintenance_distance = np.linalg.norm(maintenanceCentroid - centroid)

            # if evolution_distance < maintenance_distance:
            #     category = "Evolution"
            # else:
            #     category = "Maintenance"
            
            # Calculate cosine similarity
            evolution_similarity = np.dot(evolutionCentroid, centroid) / (np.linalg.norm(evolutionCentroid) * np.linalg.norm(centroid))
            maintenance_similarity = np.dot(maintenanceCentroid, centroid) / (np.linalg.norm(maintenanceCentroid) * np.linalg.norm(centroid))

            # Determine category based on cosine similarity
            if evolution_similarity < maintenance_similarity:
                category = "Evolution"
            else:
                category = "Maintenance"


            output_file.write("----------------------------------------------------------------------" + "\n")
            output_file.write("Category: " + category + "\n")
            output_file.write("Evolution Distance: " + str(evolution_similarity) + "\n")
            output_file.write("Maintenance Distance: " + str(maintenance_similarity) + "\n")
            output_file.write("Commit Msg: " + commitMessage + "\n")
            output_file.write("----------------------------------------------------------------------" + "\n")

            print("Have categorized commit " + str(currentCommit) + " out of " + str(totalCommits))
            currentCommit += 1

if __name__ == "__main__":
    main()