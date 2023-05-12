

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

def main():
    
    return
=======
def countTotalIssueTitles(file_path):
    """
    Counts grand total number of issue titles in .txt file
    @param file_path: file to extract issues titles from
    """
    # IssueTitles Counter
    total_num_issue_titles = 0

    # Access .txt file
    with open(file=file_path, mode='r', encoding="utf-8") as out_file:
        for line in out_file:
            if "Issue Title:" in line:
                total_num_issue_titles += 1

    # Return total number of issue titles
    return total_num_issue_titles


def countIssueTitlesContaining(file_path, key_word_list):
    """
    Counts grand total number of issues containing specific key word(s).
    @param file_path: file path that contains 
    @param key_word: key word to find inside of file_path
    """
    # IssueTitles Counter
    total_num_issue_titles = 0

    # Access .txt file
    with open(file=file_path, mode='r', encoding="utf-8") as out_file:
        for line in out_file:
            if ("Issue Title:" in line) and any(word in line.lower() for word in key_word_list):
                total_num_issue_titles += 1

    # Return total number of issue titles
    return total_num_issue_titles


def main():
    """Main Method"""
    # File path
    file_path_test = "./Python/mongo_db_extract_refactoring_doc.txt"

    # Calculate total number of issue titles
<<<<<<< HEAD
    total_iss = countTotalIssueTitles(file_path="/Users/preston/CS520_Final_Project/COMPSCI_520_Final_Project/Python/mongo_db_extract_refactoring_doc.txt")
    print("TOTAL_ISSUE_TITLES:", total_iss)
>>>>>>> c540d70 (Code cleanup for IssuesCount.py)
=======
    total_iss = countTotalIssueTitles(file_path=file_path_test)
    print("Grand Total Issue Titles:", total_iss)
>>>>>>> 55fbd0d (Added countIssueTitlesContaining() to IssuesCount.py)

    # Later: We calculate total number of issue titles containing key words or related words
    bug_keywords = ["bugs", "bug"]
    total_iss_bugs = countIssueTitlesContaining(file_path=file_path_test, key_word_list=bug_keywords)
    print("Total 'bugs' Issue Titles:", total_iss_bugs)

    refactor_keywords = ["refactor", "refactoring", "refactors", "refactorings", "refactored"]
    total_iss_refactor = countIssueTitlesContaining(file_path=file_path_test, key_word_list=refactor_keywords)
    print("Total 'refactor' Issue Titles:", total_iss_refactor)
=======
def countTotalIssueTitles(file_path):
=======
def countTotalIssueBodies(file_path):
>>>>>>> cbd89d3... Fixed IssuesCount.py to count Issue Bodies
    """
    Counts grand total number of issue bodies in .txt file
    Note that issue bodies are counted as "Issue Descriptions" in the textfile
    @param file_path: file to extract issues titles from
    """
    # Issue Bodies Counter
    total_num_issue_bodies = 0

    # Access .txt file
    with open(file=file_path, mode='r', encoding="utf-8") as out_file:
        for line in out_file:
            if "Issue Description:" in line:
                total_num_issue_bodies += 1

    # Close file
    out_file.close()

    # Return total number of issue bodies
    return total_num_issue_bodies


def countIssueBodiesContaining(file_path, key_word_list):
    """
    Counts grand total number of issues bodies containing specific key word(s).
    @param file_path: file path that contains all issue bodies to extract/count
    @param key_word: key word to find inside of file_path
    """
    # Issue bodies Counter
    total_num_issue_bodies = 0

    # Flag for identifying if keyword(s) is/are found in line of text for a given issue body
    keyword_found = False

    # Access .txt file
    with open(file=file_path, mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                keyword_found = False

            # If key word(s) is found, and flag wasn't set to True, increment number of issue bodies count
            if (not keyword_found) and any(word in line.lower() for word in key_word_list):
                total_num_issue_bodies += 1
                keyword_found = True

    # Close file
    out_file.close()

    # Return total number of issue titles
    return total_num_issue_bodies


def main():
    """Main Method"""
    # File path
<<<<<<< HEAD
    # file_path_test = "mongo_db_extract_refactoring_doc.txt"
    file_path_test = "extractedIssueDescRefactoring.txt"

<<<<<<< HEAD
    # Calculate total number of issue titles
<<<<<<< HEAD
    total_iss = countTotalIssueTitles(file_path="/Users/preston/CS520_Final_Project/COMPSCI_520_Final_Project/Python/mongo_db_extract_refactoring_doc.txt")
    print("TOTAL_ISSUE_TITLES:", total_iss)
>>>>>>> 1ec81ef... Added countTotalIssueTitles() of IssuesCount.py
=======
    total_iss = countTotalIssueTitles(file_path=file_path_test)
<<<<<<< HEAD
    print("Grand Total Issue Titles:", total_iss)
>>>>>>> 55fbd0d... Added countIssueTitlesContaining() to IssuesCount.py
=======
>>>>>>> 3441dd5... Added related-key words and calculated RQ2 percentage
=======
    # Calculate total number of issue bodies
    total_iss = countTotalIssueBodies(file_path=file_path_test)
>>>>>>> cbd89d3... Fixed IssuesCount.py to count Issue Bodies
=======
    file_path_test_refactor = "./Python/extractedIssueDescRefactoring.txt"
    file_path_test_bugs = "./Python/extractedIssueDescBugs.txt"

    # Calculate total number of issue bodies
    # total_iss = countTotalIssueBodies(file_path=file_path_test)
>>>>>>> 3bc195f... Added IssueBodiesCountBugs.py and IssueBodiesCountRefactor.py for RQ2

    # Calculate total number of issue bodies containing key words ("bugs", "refactoring")
    bug_keywords = ["bugs", "bug"]
    total_iss_bugs = countIssueBodiesContaining(file_path=file_path_test_bugs, key_word_list=bug_keywords)

    refactor_keywords = ["refactor", "refactoring", "refactors", "refactorings", "refactored"]
    total_iss_refactor = countIssueBodiesContaining(file_path=file_path_test_refactor, key_word_list=refactor_keywords)

    # Caculate total number of issue bodies containing key words or words similar to key word
    bug_keywords_related = [
        " bug ", 
        " bugs ", 
        " error ", 
        " failure ", 
        " defect ", 
        " fault "
    ]
    total_related_iss_bugs = countIssueBodiesContaining(file_path=file_path_test_bugs, key_word_list=bug_keywords_related)

    refactor_keywords_related = [
        "add", 
        "chang" , 
        "clean",
        "code optimization",
        "creat",
        "extend",
        "extract",
        "fix",
        "improv",
        "inlin",
        "introduc",
        "merg",
        "mov",
        "pull up", 
        "pulls up",
        "pulling up", 
        "pulled up",
        "push down", 
        "pushes down", 
        "pushed down", 
        "pushing down",
        "repackag",
        "redesign", 
        "reduc", 
        "refactor", 
        "refin", 
        "remov", 
        "renam", 
        "reorganiz", 
        "replac", 
        "restructur",
        "rewrit",
        "simplify",
        "simplifi",
        "split"
    ]
    total_related_iss_refactor = countIssueBodiesContaining(file_path=file_path_test_refactor, key_word_list=refactor_keywords_related)
    
    # Calculate percentages
    refactor_percent = (total_iss_refactor / total_related_iss_refactor) * 100
    bug_percent = (total_iss_bugs / total_related_iss_bugs) * 100
    
    print("----- Research Question 2 -----")
    # print("Grand Total Issue Bodies:", total_iss)
    # print()
    print("Total 'bugs' Issue Bodies:", total_iss_bugs)
    print("Total 'bug-related' Issue Bodies:", total_related_iss_bugs)
    print()
    print("Total 'refactor' Issue Bodies:", total_iss_refactor)
    print("Total 'refactor-related' Issue Bodies:", total_related_iss_refactor)
    print()
    print("Bug Percentage: ", bug_percent, "%", sep="")
    print("Refactor Percentage: ", refactor_percent, "%", sep="")

if __name__ == "__main__":
    main()