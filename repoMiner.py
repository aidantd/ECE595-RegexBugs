from pydriller import Repository
import pandas as pd
from openpyxl import workbook
import matplotlib.pyplot as plt

# Here begins a list of potentially interesting repos to mine
#
# https://github.com/rust-lang/regex (lots of bug fixes for regex related code)
# https://github.com/google/re2


# Notes:
# TODO: update these lists as time goes on, maybe add additional criteria for evolution since a lot are being pulled
# TODO: Maybe use code churn methods to see average commit , or lines count, could also incop dmm params for additional analysis
def plotAllEngine(mode, dataDict):
    plt.figure()
    keylist = []
    for key in dataDict:
        plt.plot(dataDict[key].index, dataDict[key].values, marker="o")
        keylist.append(key)
    plt.xlabel("Year")
    plt.ylabel("Number of Items")
    plt.title(mode + " Items Found Each Year")
    plt.legend(keylist)
    plt.grid(True)
    # plt.show()
    plt.savefig(mode + "_EngTotal_line_graph.png")


def plotSingleEngine(totalItemsPerYear, evoItemsPerYear, maintainItemsPerYear, key):
    plt.figure()
    plt.plot(totalItemsPerYear.index, totalItemsPerYear.values, marker="o")
    plt.plot(evoItemsPerYear.index, evoItemsPerYear.values, marker="s")
    plt.plot(maintainItemsPerYear.index, maintainItemsPerYear.values, marker="^")
    plt.xlabel("Year")
    plt.ylabel("Number of Items")
    plt.title(key.upper() + "- Number of Items Found Each Year")
    plt.legend(["All", "Evolution", "Maintenance"])
    plt.grid(True)
    # plt.show()
    plt.savefig(key + "_line_graph.png")


def mineRepo():
    # Run one repo at a time so it won't take too long
    """repoDict = {
        "rust": "https://github.com/rust-lang/regex.git",
        "re2": "https://github.com/google/re2.git",
        "pcre": "https://github.com/PCRE/pcre2.git",
        "https://github.com/openjdk/jdk": "src/java.base/share/classes/java/util/regex/",
        "https://github.com/v8/v8": "src/regexp/",
        "https://github.com/python/cpython": "Lib/re/"
    }"""
    # Format: {repo url: folder path}
    repoDict = {"https://github.com/unicode-org/icu": "icu4c/source/i18n/unicode/"}
    allEngTotal = {}
    allEngEvo = {}
    allEngMaintain = {}

    # %% set search criteria for code
    # strings to check for in the repo
    evoStrings = ["improve", "support", "feature", "new"]  # removed "add"
    maintainStrings = ["fix", "cleanup", "clean up", "sanity check"]
    keywordMatchCount = {}

    df = pd.DataFrame(
        columns=[
            "Commit Hash",
            "Commit Date",
            "Commit Msg",
            "Categorization",
            "Number of Lines",
        ]
    )

    for word in evoStrings + maintainStrings:
        keywordMatchCount[word] = 0

    for key, value in repoDict.items():
        commitArray = []
        # %% Search through every commit in a given repository and return any commits containing
        # the information we are searching for
        for commit in Repository(key, filepath=value).traverse_commits():
            # initialize flags as false for each commit, make them true
            evoFlag = False
            maintainFlag = False

            # %% check if the message contains any key phrases in
            for s in evoStrings:
                if s in commit.msg.lower():
                    commitArray.append(
                        [
                            commit.hash,
                            str(commit.committer_date),
                            commit.msg,
                            "Evolution",
                            commit.lines,
                        ]
                    )
                    evoFlag = (
                        True  # set flag to true to indicate that is has been matched
                    )
                    keywordMatchCount[s] = keywordMatchCount[s] + 1
                    break  # end early once one is found

            for s in maintainStrings:
                if s in commit.msg.lower():
                    commitArray.append(
                        [
                            commit.hash,
                            str(commit.committer_date),
                            commit.msg,
                            "Maintenance",
                            commit.lines,
                        ]
                    )
                    maintainFlag = (
                        True  # set flag to true to indicate that is has been matched
                    )
                    keywordMatchCount[s] = keywordMatchCount[s] + 1
                    break  # end early once one is found

            if (
                not evoFlag and not maintainFlag
            ):  # if not matched mark the commit as unmatched
                commitArray.append(
                    [
                        commit.hash,
                        str(commit.committer_date),
                        commit.msg,
                        "Unmatched",
                        commit.lines,
                    ]
                )

            # %% Write the originally scraped information
            df = pd.DataFrame(
                data=commitArray,
                columns=[
                    "Commit Hash",
                    "Commit Date",
                    "Commit Msg",
                    "Categorization",
                    "Number of Lines",
                ],
                copy=False,
            )
            # TODO: add in progess bar?
            # end commit loop

        df.to_excel("_output.xlsx", index=False)

        # Extract year from the commit date
        df["Year"] = pd.to_datetime(df["Commit Date"], utc=True).dt.year


# Commemted out because sometimes there will be error
"""
        # %% Count the number of items per year

        # todo save these across repos for cross analysis
        totalItemsPerYear = df["Year"].value_counts().sort_index()

        evoDf = df[df["Categorization"] == "Evolution"]
        evoItemsPerYear = evoDf["Year"].value_counts().sort_index()

        maintainDf = df[df["Categorization"] == "Maintenance"]
        maintainItemsPerYear = maintainDf["Year"].value_counts().sort_index()

        allEngTotal[key] = totalItemsPerYear
        allEngEvo[key] = evoItemsPerYear
        allEngMaintain[key] = maintainItemsPerYear

        # get stats for lines
        avgLinesTotal = df["Number of Lines"].mean()
        stdLinesTotal = df["Number of Lines"].std()
        avgLinesEvo = evoDf["Number of Lines"].mean()
        stdLinesEvo = evoDf["Number of Lines"].std()
        avgLinesMaintain = maintainDf["Number of Lines"].mean()
        stdLinesMaintain = maintainDf["Number of Lines"].std()

        x = ["All", "Evolution", "Maintenance"]
        y = [avgLinesTotal, avgLinesEvo, avgLinesMaintain]
        yerr = [stdLinesTotal, stdLinesEvo, stdLinesMaintain]
        fig, ax = plt.subplots()
        ax.errorbar(x, y, yerr, fmt="o", linewidth=2, capsize=6)
        plt.show()
        #        plt.xlabel("Year")
        #        plt.ylabel("Number of Items")
        #        plt.title(key.upper() + "- Number of Items Found Each Year")
        #        plt.legend(["All", "Evolution", "Maintenance"])
        #        plt.grid(True)

        # these may no longer be needed
        #        # Add the count of items per year to the original DataFrame
        #        df = df.merge(totalItemsPerYear.rename("Commits (Bug Fixes?) Found Per Year"), left_on="Year", right_index=True, how="left")
        #
        #        # Save the modified DataFrame to Excel
        #        df.to_excel("output.xlsx", index=False)

        # %% Create a line graph (uncomment if wanted)
        plotSingleEngine(totalItemsPerYear, evoItemsPerYear, maintainItemsPerYear, key)

        print("Done with " + key + " engine\n")
        # end engine loop

    plotAllEngine("All", allEngTotal)
    plotAllEngine("Evolution", allEngEvo)
    plotAllEngine("Maintenance", allEngMaintain)

    for key in keywordMatchCount:
        print(key + ": " + str(keywordMatchCount[key]) + "\n")

"""
if __name__ == "__main__":
    mineRepo()
