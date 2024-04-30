import pandas as pd
import json

# Read from xlsx file
excel_file = "re2_output.xlsx"
df = pd.read_excel(
    excel_file, usecols="A:C", skiprows=0, names=["hash", "date", "message"]
)

repository_name = "re2"
df["repository"] = repository_name

df = df[["repository", "hash", "date", "message"]]
data = df.to_dict(orient="records")

# Write to JSONL file
jsonl_file = repository_name + "_commits.jsonl"
with open(jsonl_file, "w") as f:
    for record in data:
        f.write(json.dumps(record) + "\n")
