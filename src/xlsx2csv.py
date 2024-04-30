"""
Convert XLSX output files from PyDriller, with manually added labels for some rows, to CSV files

Prepartory step before using truth_csv_to_jsonl.py
"""

"""
ECE 59500 AI Class, Spring 2024 - Regex Bugs project team
"""

import pandas as pd
import unicodedata

def convert_xlsx_to_csv(repository_name):
    # Read from xlsx file to Pandas DataFrame
    excel_file = repository_name + "_output.xlsx"
    df = pd.read_excel(
        excel_file, usecols="A:F", skiprows=0, names=["hash", "date", "message","category","lines","Evolution?"]
    )

    # Clean up commit text for CSV output
    for i in range(len(df["message"])):
        msg = df.loc[i,'message']
        msg = msg.replace('"',"'").replace('\\','')
        msg = msg.replace('\n'," ").replace('\r'," ")       
        msg = "".join(ch for ch in msg if unicodedata.category(ch)[0]!="C")
        df.loc[i,'message'] = msg

    # Write needed columns to CSV file
    df = df[["hash", "date", "message","Evolution?"]]
    df.to_csv(repository_name + "_all.csv", index=False)

repo_names = ['v8','rust','pcre2','java','ICU','re2','python_re']
for name in repo_names:
    repository_name = "data/" + name
    convert_xlsx_to_csv(repository_name)
