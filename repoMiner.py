from pydriller import Repository
from datetime import timedelta
import pandas as pd
import openpyxl 

# Here begins a list of potentially interesting repos to mine
#
# https://github.com/rust-lang/regex (lots of bug fixes for regex related code)
# https://github.com/google/re2 

def main():
    commitArray = []
    for commit in Repository("https://github.com/rust-lang/regex").traverse_commits():
        if ("regex " in commit.msg) and (("bug" in commit.msg) or ("fix" in commit.msg)):
            commitArray.append([commit.hash, str(commit.committer_date), commit.msg])

    df = pd.DataFrame(data=commitArray, columns=["Commit Hash", "Commit Date", "Commit Msg"], copy=False)
    df.to_excel('output.xlsx')

if __name__ == "__main__":
    main()
