from transformers import AutoTokenizer, AutoModel
import json
import torch
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def getEmbedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    
    outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def calculateCentroid(embeddings):
    return np.mean(embeddings, axis=0)

evolutionCommits = ["{\"repository\": \"re2\", \"hash\": \"0a38cba1d9dcfbd713141095582597af700f22e9\", \"date\": \"2010-03-02 17:17:51-08:00\", \"message\": \"initial release\"}", 
                    "{\"repository\": \"re2\", \"hash\": \"e414fec4f7fe30f08baaf2d1f9ddf7e88963a2f7\", \"date\": \"2011-03-02 15:59:46-05:00\", \"message\": \"re2: add endpos to RE2::Match, fix bugs\n\nAdding endpos to RE2::Match allows callers to limit the ending\nposition of matches to points before the end of the text.\n\nFound and fixed a few bugs involving startpos and endpos not\nbeing handled properly.  These would only affect callers using\nMatch directly.  They cannot affect callers using FullMatch,\nPartialMatch, and DoMatch, because those always use startpos == 0.\n\nR=r, rsc_swtch\nCC=re2-dev\nhttp://codereview.appspot.com/4237051\"}",
                    "{\"repository\": \"re2\", \"hash\": \"c98af90b23ed1345f08bac91f4c2914a6ed61f39\", \"date\": \"2012-07-17 16:44:09-04:00\", \"message\": \"make RE2::Rewrite and RE2::MaxSubmatch public, so that\nclients can implement their own Replace loops\n\n[Exported from internal Google RE2 repository.]\n\nR=rsc\nCC=re2-dev\nhttp://codereview.appspot.com/6410044\"}"]

maintenanceCommits = ["{\"repository\": \"re2\", \"hash\": \"db46d1e11eee1ad501e8e08411747468d1d6a87e\", \"date\": \"2024-03-17 10:04:57+00:00\", \"message\": \"Bump versions of actions to latest releases.\n\nNote that this isn't the same as pinning to commits as in specifying\ntheir hashes. Note also that this isn't as ugly either. It's a minor\nimprovement over \"floating\" (i.e. major version only) tags/branches.\n\nChange-Id: Id88fe81281885aff41f2625b3b71f945266c8677\nReviewed-on: https://code-review.googlesource.com/c/re2/+/62871\nReviewed-by: Alex Chernyakhovsky <achernya@google.com>\nReviewed-by: Paul Wankadia <junyer@google.com>\"} ",
                      "{\"repository\": \"re2\", \"hash\": \"ddb3414a8f65ff03e63bbd1932fb2164cec69bf1\", \"date\": \"2024-03-11 11:18:05+00:00\", \"message\": \"Add Clang 18 to the build matrix.\n\n... and remove Clang 15 so that we continue to\ntest with only the three most recent releases.\n\nChange-Id: Ib1eaa20b2c988bb53027dd3e01551d5d95058e24\nReviewed-on: https://code-review.googlesource.com/c/re2/+/62830\nReviewed-by: Perry Lorier <perryl@google.com>\nReviewed-by: Paul Wankadia <junyer@google.com>\"}",
                      "{\"repository\": \"re2\", \"hash\": \"f9550c3f7207f946a45bbccd1814b12b136aae72\", \"date\": \"2024-02-19 16:37:14+00:00\", \"message\": \"Fix more ancient bugs around Latin-1 handling.\n\nIt turned out that case folding assumed UTF-8 mode, so\nwe would fold, say, 0xD1 to 0xF1 even in Latin-1 mode.\n\nFixes #477.\n\nChange-Id: I73aa5c8e33ee0c6041c54e3a7268635915960f64\nReviewed-on: https://code-review.googlesource.com/c/re2/+/62714\nReviewed-by: Alex Chernyakhovsky <achernya@google.com>\nReviewed-by: Paul Wankadia <junyer@google.com>\"}"]


evolutionEmbeddings = [getEmbedding(sentence) for sentence in evolutionCommits]
maintenanceEmbeddings = [getEmbedding(sentence) for sentence in maintenanceCommits]

evolutionCentroid = calculateCentroid(evolutionEmbeddings)
maintenanceCentroid = calculateCentroid(maintenanceEmbeddings)

with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/categorizations.txt", 'w') as output_file:
    output_file.write("Categorization\n")
    output_file.write("-----------------------\n")

    with open("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/re2_commits.jsonl", 'r') as file:
        commitsToCheck = [line.strip() for line in file.readlines()]

    for commit in commitsToCheck:
        embedding = getEmbedding(commit)
        centroid = calculateCentroid(embedding)

        evolution_distance = np.linalg.norm(evolutionCentroid - centroid)
        maintenance_distance = np.linalg.norm(maintenanceCentroid - centroid)

        if evolution_distance < maintenance_distance:
            category = "Evolution"
        else:
            category = "Maintenance"

        output_file.write(category + "\n")
        print("We wrote something")