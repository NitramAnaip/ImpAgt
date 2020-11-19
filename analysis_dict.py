# Check out here for preprocessing: https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/


import json
import numpy as np

#import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter


# Plotting tools
import matplotlib.pyplot as plt
import seaborn as sns

import heapq



parsed_sites = 'abs_dict.json'


print("Started Reading JSON file")
with open(parsed_sites, "r") as read_file:
    developer = json.load(read_file)
    print("Decoded JSON Data From File")

corpus = developer['abstracts']

# Preprocessing

def convert_lower_case(data):
    return np.char.lower(data)

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer= PorterStemmer()
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def lemming(data):
    lemmatizer = WordNetLemmatizer() 
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + lemmatizer.lemmatize(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text



def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = lemming(data)
    return data


# # Preprocessing
print("Preprocessing {} abstracts...".format(len(corpus)))
preprocessed_abstracts = []
for abstract in corpus:
    preprocessed_abstracts.append(preprocess(abstract))
print("Preprocessing DONE...")


# # Word Counts

# words = word_tokenize(str(preprocess_abstract[3]))
# fd = FreqDist(words)
# print(fd.most_common(3))
# fd.plot(20)

print("Word Counts")
wordfreq = {}
for abstract in preprocessed_abstracts:
    tokens = word_tokenize(abstract)
    for token in tokens:
        if token not in wordfreq.keys():
            wordfreq[token] = 1
        else:
            wordfreq[token] += 1

most_wordfreq = sorted(wordfreq.items(), key=lambda x: x[1], reverse=True)[:200]
# print(list(sort_wordfreq)[:20])

# IDF values for the most frequently occurring words in the corpus
print("IDF Values")
word_idf_values = {}
for token in most_wordfreq:
    doc_containing_word = 0
    for abstract in preprocessed_abstracts:
        if token[0] in word_tokenize(abstract):
            doc_containing_word += 1
    word_idf_values[token] = np.log(len(preprocessed_abstracts)/(1 + doc_containing_word))


# TF values
print("TF Values")
word_tf_values = {}
for token in most_wordfreq:
    sent_tf_vector = []
    for abstract in preprocessed_abstracts:
        doc_freq = 0
        for word in word_tokenize(abstract):
            if token[0] == word:
                  doc_freq += 1
        word_tf = doc_freq/len(word_tokenize(abstract))
        sent_tf_vector.append(word_tf)
    word_tf_values[token] = sent_tf_vector

# TF-IDF values
print("TF-IDF Values")
tfidf_values = []
for token in word_tf_values.keys():
    tfidf_sentences = []
    for tf_sentence in word_tf_values[token]:
        tf_idf_score = tf_sentence * word_idf_values[token]
        tfidf_sentences.append(tf_idf_score)
    tfidf_values.append(tfidf_sentences)

print(tfidf_values)
