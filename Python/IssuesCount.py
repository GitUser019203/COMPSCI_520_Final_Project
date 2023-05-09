

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
    total_iss = countTotalIssueTitles(file_path=file_path_test)

    # Calculate total number of issue titles containing key words ("bugs", "refactoring")
    bug_keywords = ["bugs", "bug"]
    total_iss_bugs = countIssueTitlesContaining(file_path=file_path_test, key_word_list=bug_keywords)

    refactor_keywords = ["refactor", "refactoring", "refactors", "refactorings", "refactored"]
    total_iss_refactor = countIssueTitlesContaining(file_path=file_path_test, key_word_list=refactor_keywords)

    # Caculate total number of issue title containing key words or words similar to key word
    bug_keywords_related = ["bug", "bugs", "error", "failure", "defect", "fault"]
    total_related_iss_bugs = countIssueTitlesContaining(file_path=file_path_test, key_word_list=bug_keywords_related)

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
    total_related_iss_refactor = countIssueTitlesContaining(file_path=file_path_test, key_word_list=refactor_keywords_related)
    
    # Calculate percentages
    refactor_percent = (total_iss_refactor / total_related_iss_refactor) * 100
    bug_percent = (total_iss_bugs / total_related_iss_bugs) * 100
    
    print("----- Research Question 2 -----")
    print("Grand Total Issue Titles:", total_iss)
    print()
    print("Total 'bugs' Issue Titles:", total_iss_bugs)
    print("Total 'bug-related' Issue Titles:", total_related_iss_bugs)
    print()
    print("Total 'refactor' Issue Titles:", total_iss_refactor)
    print("Total 'refactor-related' Issue Titles:", total_related_iss_refactor)
    print()
    print("Bug Percentage: ", bug_percent, "%", sep="")
    print("Refactor Percentage: ", refactor_percent, "%", sep="")

if __name__ == "__main__":
    main()