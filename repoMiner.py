from pydriller import Repository
import pandas as pd
from openpyxl import workbook
import matplotlib.pyplot as plt

# Here begins a list of potentially interesting repos to mine
#
# https://github.com/rust-lang/regex (lots of bug fixes for regex related code)
# https://github.com/google/re2 

def mineRepo():
    repoDict = {"rust": "https://github.com/rust-lang/regex.git", "re2":"https://github.com/google/re2.git"}

    for key in repoDict:
        commitArray = []
        
        # strings to check for in the repo
        evoStrings = ["improve","add","support"]
        maintainStrings = ["fix", "cleanup", "clean up", "sanity check"]

        # Search through every commit in a given repository and return any commits containing
        # the information we are searching for 
        for commit in Repository(repoDict[key]).traverse_commits():
            
            # check if the message contains any key phrases in 
            for s in evoStrings: 
                if  s in commit.msg.lower():
                    commitArray.append([commit.hash, str(commit.committer_date), commit.msg,'Evolution'])
                    break # end early once one is found
            for s in maintainStrings:
                if  s in commit.msg.lower():
                    commitArray.append([commit.hash, str(commit.committer_date), commit.msg,'Maintainence'])
                    break # end early once one is found
                
                
            # Write the originally scraped information 
            df = pd.DataFrame(data=commitArray, columns=["Commit Hash", "Commit Date", "Commit Msg", "Categorization"], copy=False)
        df.to_excel(key + "_output.xlsx", index=False)
    
        # Extract year from the commit date
        df["Year"] = pd.to_datetime(df["Commit Date"], utc=True).dt.year
    
        # Count the number of items per year
        totalItemsPerYear = df["Year"].value_counts().sort_index()
        evoDf = df[df["Categorization"]=='Evolution']
        evoItemsPerYear = evoDf["Year"].value_counts().sort_index()
        maintainDf = df[df["Categorization"]=='Maintainence']
        maintainItemsPerYear = maintainDf["Year"].value_counts().sort_index()
#        # Add the count of items per year to the original DataFrame
#        df = df.merge(totalItemsPerYear.rename("Commits (Bug Fixes?) Found Per Year"), left_on="Year", right_index=True, how="left")
#    
#        # Save the modified DataFrame to Excel
#        df.to_excel("output.xlsx", index=False)
    
        # Create a line graph (uncomment if wanted)
        plt.figure()
        plt.plot(totalItemsPerYear.index, totalItemsPerYear.values, marker="o")
        plt.plot(evoItemsPerYear.index,evoItemsPerYear.values, marker="s")
        plt.plot(maintainItemsPerYear.index,maintainItemsPerYear.values, marker="^")
        plt.xlabel("Year")
        plt.ylabel("Number of Items")
        plt.title(key.upper() + "- Number of Items Found Each Year")
        plt.legend(["All", "Evolution", "Maintainence"])
        plt.grid(True)
        plt.show()
        plt.savefig(key+"_line_graph.png")

if __name__ == "__main__":
    mineRepo()

