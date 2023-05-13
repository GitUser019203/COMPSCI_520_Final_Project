lines = []
with open(file='extractedIssueDescRefactoring.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)

list1 =["Add","add","append","addition","creation","create","apply","clean",
    "code optimization","extend","introduce"]
list2=["clean","modify","repair","fix","simplify","split","redesign","refactor","rewrite","repackage"]
counterAdd =0
counterModify=0
totalIssues = 0
for i in lines:
  totalIssues+=1
  
  j = i.split()
  for m in j:
    if m.lower() in list1:
      counterAdd+=1
    if m.lower() in list2:
        counterModify+=1
print("total",totalIssues)
print(counterAdd,counterModify)

