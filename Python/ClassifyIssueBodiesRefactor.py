import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
import en_core_web_sm

lines = []
with open(file='extractedIssueDescRefactoring.txt', mode='r') as out_file:
        # Go through every line in file
        for line in out_file:
            # If line contains "Issue Description:", that is the start of a new issue body; reset flag to false
            if "Issue Description:" in line:
                lines.append(line)

data = pd.read_csv('extractedIssueDescRefactoring.txt', sep='Isse Description:')

nlp = en_core_web_sm.load()
 
for i in lines:
     doc = nlp(i)
     print(doc.ents)
"""
# Step 1: Prepare the unlabeled data
X = data # Issue descriptions

# Step 2: Feature extraction
vectorizer = TfidfVectorizer()  # TF-IDF vectorizer
X = vectorizer.fit_transform(X)

# Step 3: Perform clustering
num_clusters = 3  # Number of desired clusters
model = KMeans(n_clusters=num_clusters)  # K-means clustering
model.fit(X)

# Step 4: Print cluster labels
labels = model.labels_
for i, label in enumerate(labels):
    print("Text:", data['description'][i])
    print("Cluster:", label)
    print("--------")
    """
