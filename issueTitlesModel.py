import re
from copy import deepcopy
from csv import DictReader, DictWriter
from json import dumps, loads
from sys import argv
from multiprocessing import cpu_count
from this import s
from threading import Thread
from queue import Queue
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit, FileAction, Hunk, Refactoring, IssueSystem, Issue, IssueComment, MailingList, Message
from pycoshark.utils import create_mongodb_uri_string
from Python.stopwatch import StopWatch
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download, pos_tag, RegexpParser
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree

class IssueTitlesModel:
    def __init__(self):
        self.stopwatch = StopWatch()
        self.stopwatch.start()
        # Download stopwords to filter them out, and punkt and averaged_perceptron_tagger
        download("stopwords")
        download("punkt")
        download("averaged_perceptron_tagger")
        download("wordnet")

        # Issue with running NLP in multithreaded mode
        self.commit_queue = Queue()

        # Initialize lemmatizer
        self.lemmatizer = WordNetLemmatizer()

        # Verb phrase grammar
        self.verb_phrase_grammar = "VP: {<VB|VBD|VBG|VBN|VBP|VBZ><RP>*<JJ>*<NN|NNP|NNPS|NNS>}"
        self.chunk_parser = RegexpParser(self.verb_phrase_grammar)

        # Any other phrases desired can be placed below

        # Initialize a set of stop words
        self.stop_words = set(stopwords.words("english"))


        self.refactoring_documentation_patterns_words = {}
        self.refactoring_documentation_patterns_lemmas = {}
        self.refactoring_documentation_patterns_phrases = {}
        
        # Initialize a set of words to search for using NLP
        self.keywords = ['add', 'chang', 'creat', 'extend', 'extract', 'fix', 
            'improv', 'inlin', 'introduc', 'merg', 'mov', 'repackag', 
            'redesign', 'reduc', 'refin', 'remov', 'renam', 'reorganiz', 
            'replac', 'split']

        # Initialize the dictionary of refactoring documentation phrases going to be found using keyword based classification
        for keyword in self.keywords:
            self.refactoring_documentation_patterns_phrases[keyword] = []
    def load(self):
        # Loads the refactoring documentation phrases from a json file with the UTF-8 encoding instead of using the cp1252 encoding.
        with open(r"Python\NLTK\commit_msg_refactoring_documentation_phrases.json", 'r', encoding='utf-8') as in_json:
            self.refactoring_documentation_patterns_phrases = loads(in_json.read())       
    def save(self):
        # Save the refactoring documentation words to a csv file with no newlines between rows and with the UTF-8 encoding.
        with open("refactoring_documentation_words.csv", 'w', newline = '', encoding='utf-8') as out_csv:
            csv_writer = DictWriter(out_csv, fieldnames = ['Word', 'Number of occurrences'])
            csv_writer.writeheader()
            for word in self.refactoring_documentation_patterns_words:
                csv_writer.writerow({'Word': word, 'Number of occurrences': self.refactoring_documentation_patterns_words[word]})

        # Save the refactoring documentation lemmas to a csv file with no newlines between rows and with the UTF-8 encoding.
        with open("refactoring_documentation_lemmas.csv", 'w', newline = '', encoding='utf-8') as out_csv:
            csv_writer = DictWriter(out_csv, fieldnames = ['Lemma', 'Number of occurrences'])
            csv_writer.writeheader()
            for word in self.refactoring_documentation_patterns_words:
                csv_writer.writerow({'Lemma': word, 'Number of occurrences': self.refactoring_documentation_patterns_words[word]})
        # Save the refactoring documentation phrases to a json file with no newlines between rows and with the UTF-8 encoding instead of using the cp1252 encoding.
        with open("refactoring_documentation_phrases.json", 'w', encoding='utf-8') as out_json:
            out_json.write(dumps(self.refactoring_documentation_patterns_phrases, indent = '\t'))
        
        self.stopwatch.stop()
        self.stopwatch.get_elapsed_time()
    def mine_commit(self, commit):
        #commit_queue.put(commit)
        refactorings = Refactoring.objects(commit_id=commit.id)
        if refactorings.count() > 0:
            for linked_issue_id in commit.linked_issue_ids:
                for issue in Issue.objects(id=linked_issue_id):
                    if issue.title is not None and issue.desc is not None and commit.message is not None :
                        words_in_issue_title = word_tokenize(issue.title)
                        for word in words_in_issue_title:
                            if word.casefold() not in self.stop_words and len(word) > 2:
                                lemma = self.lemmatizer.lemmatize(word)
                                if word in self.refactoring_documentation_patterns_words:
                                    self.refactoring_documentation_patterns_words[word] += 1
                                else:
                                    self.refactoring_documentation_patterns_words[word] = 0

                                if lemma in self.refactoring_documentation_patterns_lemmas:
                                    self.refactoring_documentation_patterns_lemmas[lemma] += 1
                                else:
                                    self.refactoring_documentation_patterns_lemmas[lemma] = 0
                        issue_title_pos_tags = pos_tag(words_in_issue_title)
                        verb_phrase_trees = [node for node in self.chunk_parser.parse(issue_title_pos_tags) if type(node) is Tree]
                        for nlp_tree in verb_phrase_trees:
                            if nlp_tree.label() == "VP":
                                tree_string_representation = str(nlp_tree).casefold()
                                for keyword in self.keywords:
                                   # Filter out the verb phrases that don't use the keyword as a verb
                                   if keyword in tree_string_representation:
                                       phrase = " ".join([node[0] for node in nlp_tree])
                                       if re.match(keyword, nlp_tree[0][0], re.I):
                                           if phrase not in self.refactoring_documentation_patterns_phrases[keyword]:
                                               self.refactoring_documentation_patterns_phrases[keyword].append(phrase)
    def commit_mining_worker():
        while True:
            commit = self.commit_queue.get()
            refactorings = Refactoring.objects(commit_id=commit.id)
            if refactorings.count() > 0:
                for linked_issue_id in commit.linked_issue_ids:
                    for issue in Issue.objects(id=linked_issue_id):
                        if issue.title is not None and issue.desc is not None and commit.message is not None :
                            words_in_issue_title = word_tokenize(issue.title)
                            for word in words_in_issue_title:
                                if word.casefold() not in stop_words and len(word) > 2:
                                    lemma = self.lemmatizer.lemmatize(word)
                                    if word in self.refactoring_documentation_patterns_words:
                                        self.refactoring_documentation_patterns_words[word] += 1
                                    else:
                                        self.refactoring_documentation_patterns_words[word] = 0

                                    if lemma in self.refactoring_documentation_patterns_lemmas:
                                        self.refactoring_documentation_patterns_lemmas[lemma] += 1
                                    else:
                                        self.refactoring_documentation_patterns_lemmas[lemma] = 0
                            issue_title_pos_tags = pos_tag(words_in_issue_title)
                            print(self.chunk_parser.parse(issue_title_pos_tags))
            self.commit_queue.task_done()