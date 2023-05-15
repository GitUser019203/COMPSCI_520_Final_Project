
# Count Issue Bodies related to Bugs

# Calculate total number of issue bodies containing key words or words similar to key word
bug_keywords = ["bugs", "bug"]

bug_keywords_related = [
    " bug ", 
    " bugs ", 
    " error ", 
    " failure ", 
    " defect ", 
    " fault "
]



lines = []
with open(file='./Python/extractedIssueDescBugs.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)

list1 =["Add","add","append","addition","creation","create","apply","clean",
    "code optimization","extend","introduce"]
list2=["clean","modify","repair","fix","simplify","split","redesign","refactor","rewrite","repackage","refactor", "refactoring", "refactors", "refactorings", "refactored"]
list3=["reduce","reduction","delete","subtract","remove","dump","rid","push down","redundant"]

counterAdd =0
counterModify=0
totalIssues = 0
counterDelete = 0

for i in lines:
  totalIssues+=1
  j = i.split()
  for m in j:
    if any(word in m.lower() for word in list1):
      counterAdd+=1
    elif any(word in m.lower() for word in list2):
        counterModify+=1
    elif any(word in m.lower() for word in list3):
        counterDelete+=1
#print("total",totalIssues)
#print(counterAdd,counterModify,counterDelete)

print("Evaluation Criteria")
print("Issues that talked about Code Addition: ",(counterAdd/totalIssues)*100,"%")
print("Issues that talked about Code Modification: ",(counterModify/totalIssues)*100,"%")
print("Issues that talked about Code Deletion: ",(counterDelete/totalIssues)*100,"%")

