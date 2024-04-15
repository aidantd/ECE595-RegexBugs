import torch
import json
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from tqdm import tqdm


dataTypeEvolution = 0
dataTypeMaintenance = 1

def parseTrainingData(dataType):
    parsedData = []
    label_map = {'0': dataTypeEvolution, '1': dataTypeMaintenance}
    if dataType == dataTypeEvolution:
        # with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingData/trainingDataEvolution.jsonl', 'r') as file:
        with open('/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/trainingData/trainingDataEvolution.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                message = data["message"]
                label = label_map[data["label"]]
                parsedData.append((message, label))

    elif dataType == dataTypeMaintenance:
        # with open('/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/trainingData/trainingDataMaintenance.jsonl', 'r') as file:
        with open('/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/trainingData/trainingDataMaintenance.jsonl', 'r') as file:
            for commit in file:
                data = json.loads(commit)
                message = data["message"]
                label = label_map[data["label"]]
                parsedData.append((message, label))
    
    return parsedData


class CommitTrainingDataset(Dataset):
    def __init__(self, sentences, labels, tokenizer, max_length):
        self.sentences = sentences
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        sentence = self.sentences[idx]
        label = self.labels[idx]
        
        encoding = self.tokenizer(sentence, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        
        return {'input_ids': input_ids, 'attention_mask': attention_mask, 'label': label}
    
def main():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
    
    evolutionData = parseTrainingData(dataTypeEvolution)
    maintenanceData = parseTrainingData(dataTypeMaintenance)
    
    allData = evolutionData + maintenanceData

    sentences = [data[0] for data in allData]
    labels = [data[1] for data in allData]

    train_dataset = CommitTrainingDataset(sentences, labels, tokenizer, max_length=128)
    train_loader = DataLoader(train_dataset, batch_size=1)

    optimizer = AdamW(model.parameters(), lr=5e-5)
    criterion = torch.nn.CrossEntropyLoss()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()

    trainingIterations = 3
    for iteration in range(trainingIterations):
        total_loss = 0
        for batch in tqdm(train_loader, desc=f'Iteration {iteration + 1}/{trainingIterations}'):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        average_loss = total_loss / len(train_loader)
        print(f"Iteration {iteration + 1}/{trainingIterations}, Average Loss: {average_loss:.4f}")

    # Aidan Mac
    # model.save_pretrained("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/models")
    # tokenizer.save_pretrained("/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/models")
    
    # Aidan Linux
    model.save_pretrained("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/models")
    tokenizer.save_pretrained("/home/aidan/Documents/School/ECE595/ECE595-RegexBugs/models")

if __name__ == "__main__":
    main()
