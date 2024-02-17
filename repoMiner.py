from pydriller import Repository

# Here begins a list of potentially interesting repos to mine
#
# https://github.com/rust-lang/regex (lots of bug fixes for regex related code)
# https://github.com/google/re2 
# 

def main():
    for commit in Repository("https://github.com/rust-lang/regex").traverse_commits():
        if ("regex " in commit.msg) and (("bug" in commit.msg) or ("fix" in commit.msg)):
            print("Found commit " + commit.hash + "\n")
            print(commit.msg + "\n")

if __name__ == "__main__":
    main()