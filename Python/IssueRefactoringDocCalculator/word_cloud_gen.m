cd 'C:\SmartSHARK\GitSmartSHARKfilePathconflict\SmartSHARKRepo\Python\IssueRefactoringDocCalculator\'
refactoring_tbl = readtable("issue_title_refactoring_doc_text_patterns - MATLAB.csv")
figure
wordcloud(refactoring_tbl, 'RefactoringType', 'Percentage')
title('Issue Refactoring Documentation Word Cloud')