import matplotlib.pyplot as plt
from wordcloud import WordCloud
from csv import DictReader
from multidict import MultiDict

with open(r"Python\NLTK\issue_refactoring_doc_text_patterns.csv", 'r', encoding='utf-8-sig') as in_csv:
    dict_reader = DictReader(in_csv)
    multi_dict = MultiDict()

    for row in dict_reader:
        for key in row:
            multi_dict[key] = float(row[key])
        break

word_cloud = WordCloud(background_color="white",width=1000,height=1000, relative_scaling=0.5)
word_cloud.generate_from_frequencies(multi_dict)
plt.imshow(word_cloud)
plt.axis("off")
plt.show()
plt.savefig(r"Python\NLTK\word_cloud.png")


with open(r"Python\NLTK\refactoring_motivations_code_smells.csv", 'r', encoding="utf-8-sig" ) as in_csv:
    dict_reader = DictReader(in_csv)
    refactoring_code_smells_dict = {}
    for row in dict_reader:
        for key in row:
            refactoring_code_smells_dict[key] = float(row[key])
        break
    names = list(refactoring_code_smells_dict.keys())
    values = list(refactoring_code_smells_dict.values())
    
    fig = plt.figure(figsize =(10, 7))
    plt.bar(range(len(refactoring_code_smells_dict)),values,tick_label=names)
    plt.ylabel("Issue Percentage")
    plt.title("Issue Documentation of Refactoring Done To Mitigate Code Smells")
    plt.savefig(r"Python\NLTK\code_smells.png")
    plt.show()

with open(r"Python\NLTK\refactoring_motivations_internal_qas.csv", 'r', encoding="utf-8-sig" ) as in_csv:
    dict_reader = DictReader(in_csv)
    refactoring_internal_qas_dict = {}
    for row in dict_reader:
        for key in row:
            refactoring_internal_qas_dict[key] = float(row[key])
        break
    names = list(refactoring_internal_qas_dict.keys())
    values = list(refactoring_internal_qas_dict.values())

    #tick_label does the some work as plt.xticks()
    fig = plt.figure(figsize =(14, 7))
    plt.bar(range(len(refactoring_internal_qas_dict)),values,tick_label=names)
    plt.ylabel("Issue Percentage")
    plt.title("Issue Documentation of Refactoring Done To Improve Internal QAs")
    plt.savefig(r"Python\NLTK\internal_qas.png")
    plt.show()

with open(r"Python\NLTK\refactoring_motivations_external_qas.csv", 'r', encoding="utf-8-sig" ) as in_csv:
    dict_reader = DictReader(in_csv)
    refactoring_external_qas_dict = {}
    for row in dict_reader:
        for key in row:
            refactoring_external_qas_dict[key] = float(row[key])
        break
    names = list(refactoring_external_qas_dict.keys())
    values = list(refactoring_external_qas_dict.values())

    #tick_label does the some work as plt.xticks()
    fig = plt.figure(figsize =(16, 7))
    plt.bar(range(len(refactoring_external_qas_dict)),values,tick_label=names)    
    plt.ylabel("Issue Percentage")
    plt.xticks(fontsize=5)
    plt.title("Issue Documentation of Refactoring Done To Improve External QAs")
    plt.savefig(r"Python\NLTK\external_qas.png")
    plt.show()
    plt.tight_layout()

with open(r"Python\NLTK\refactoring_operations_clustered_by_class.csv", 'r', encoding="utf-8-sig" ) as in_csv:
    dict_reader = DictReader(in_csv)
    refactoring_operations_dict = {}
    for row in dict_reader:
        for key in row:
            refactoring_operations_dict[key] = float(row[key])
        break
    names = list(refactoring_operations_dict.keys())
    values = list(refactoring_operations_dict.values())

    #tick_label does the some work as plt.xticks()
    plt.pie(values,labels=names)
    plt.title("Refactoring Operation Types in Issue Associated Refactoring")
    plt.savefig(r"Python\NLTK\refactoring_operations.png")
    plt.show()