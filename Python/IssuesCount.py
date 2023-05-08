

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

if __name__ == "__main__":
    main()