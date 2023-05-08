

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
    """
    Counts grand total number of Issue Titles in .txt file
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

def countIssueTitlesContaining():
    """
    Counts grand total number of issues
    """
    return 0



def main():
    """Main Method"""
    total_iss = countTotalIssueTitles(file_path="/Users/preston/CS520_Final_Project/COMPSCI_520_Final_Project/Python/mongo_db_extract_refactoring_doc.txt")
    print("TOTAL_ISSUE_TITLES:", total_iss)
>>>>>>> 1ec81ef... Added countTotalIssueTitles() of IssuesCount.py

if __name__ == "__main__":
    main()