with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingDataEvolution.jsonl', 'r') as file:
    for commit in file:
        data = json.loads(commit)
        print(data["message"])
        parsedData.append(commit["message"])