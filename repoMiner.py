from pydriller import Repository
import pandas as pd
from openpyxl import workbook
import matplotlib.pyplot as plt

# Here begins a list of potentially interesting repos to mine
#
# https://github.com/rust-lang/regex (lots of bug fixes for regex related code)
# https://github.com/google/re2 

def mineRepo():
    commitArray = []

    # Search through every commit in a given repository and return any commits containing
    # the information we are searching for 
    for commit in Repository("https://github.com/rust-lang/regex").traverse_commits():
        if ("regex " in commit.msg) and (("bug" in commit.msg) or ("fix" in commit.msg)):
            commitArray.append([commit.hash, str(commit.committer_date), commit.msg])

    # Write the originally scraped information 
    df = pd.DataFrame(data=commitArray, columns=["Commit Hash", "Commit Date", "Commit Msg"], copy=False)
    df.to_excel('output.xlsx', index=False)

    # Extract year from the commit date
    df['Year'] = pd.to_datetime(df['Commit Date'], utc=True).dt.year

    # Count the number of items per year
    items_per_year = df['Year'].value_counts().sort_index()

    # Add the count of items per year to the original DataFrame
    df = df.merge(items_per_year.rename("Commits (Bug Fixes?) Found Per Year"), left_on='Year', right_index=True, how='left')

    # Save the modified DataFrame to Excel
    df.to_excel('output.xlsx', index=False)

    # Create a line graph (uncomment if wanted)
    # plt.plot(items_per_year.index, items_per_year.values, marker='o')
    # plt.xlabel('Year')
    # plt.ylabel('Number of Items')
    # plt.title('Number of Items Found Each Year')
    # plt.grid(True)
    # plt.savefig('line_graph.png')

if __name__ == "__main__":
    mineRepo()

