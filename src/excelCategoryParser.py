import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = "/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/RegexBugsData/categorizedData/excel"

evolution_counts = {}
maintenance_counts = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file_name)
        
        df = pd.read_excel(file_path)
        
        evolution_count = df[df['Category'] == 'Evolution']['Commit Msg'].count()
        maintenance_count = df[df['Category'] == 'Maintenance']['Commit Msg'].count()
        
        evolution_counts[file_name] = evolution_count
        maintenance_counts[file_name] = maintenance_count

counts_df = pd.DataFrame({'File': list(evolution_counts.keys()),
                          'Evolution': list(evolution_counts.values()),
                          'Maintenance': list(maintenance_counts.values())})

counts_excel_path = "message_category_counts.xlsx"
counts_df.to_excel(counts_excel_path, index=False)

file_names = list(evolution_counts.keys())
evolution_values = list(evolution_counts.values())
maintenance_values = list(maintenance_counts.values())

plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(file_names))
plt.bar(index, evolution_values, bar_width, label='Evolution')
plt.bar([i + bar_width for i in index], maintenance_values, bar_width, label='Maintenance')
plt.xlabel('File Name')
plt.ylabel('Message Count')
plt.title('Message Category Counts for Each File')
plt.xticks([i + bar_width / 2 for i in index], file_names, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

plt.savefig('message_category_counts.png')

plt.show()
