"""
Convert XLSX output files from PyDriller, with manually added labels for some rows, to CSV files

Prepartory step before using truth_csv_to_jsonl.py
"""

"""
ECE 59500 AI Class, Spring 2024 - Regex Bugs project team
"""

import pandas as pd
import json

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
        df.loc[i,'message'] = msg

    # Write needed columns to CSV file
    df = df[["hash", "date", "message","Evolution?"]]
    df.to_csv(repository_name + "_all.csv", index=False)

repository_name = "data/rust"
convert_xlsx_to_csv(repository_name)
