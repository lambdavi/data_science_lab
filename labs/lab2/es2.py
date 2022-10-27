from math import log10
import string
from collections import Counter
import csv

# Functions section
def tokenize(docs):
    """
    Compute the tokens for each document.
    Input: a list of strings. Each item is a document to tokenize.
    Output: a list of lists. Each item is a list containing the tokens of the
    relative document.
    """
    tokens = []
    for doc in docs:
        for punct in string.punctuation:
            doc = doc.replace(punct, " ")
        split_doc = [ token.lower() for token in doc.split(" ") if token ]
        tokens.append(split_doc)
    return tokens

def load_dataset(path)->tuple:
    """
    Import the dataset as list of lists.
    Input: path to the file
    Output: dataset, header
    """
    dataset = []

    with open(path) as f:
        header = f.readline()
        cr = csv.reader(f)
        for r,_ in cr:
            dataset.append(r)
    return header, dataset


# Main section
header, dataset = load_dataset('reviews.txt')
tokenized_docs = tokenize(dataset)

tf = []
for doc in tokenized_docs:
    tf.append(dict(Counter(doc)))
print(tf[0])

dfs={}
for row in tokenized_docs:
    local=[]
    for w in row:
        if dfs.get(w) != None:
            if w not in local:
                dfs[w]+=1
                local.append(w)
        else:
            dfs[w]=1
            local.append(w)


dfs={k: v for k, v in sorted(dfs.items(), key=lambda item: item[1], reverse=True)}
idfs = {k:log10(len(dataset)/v) for k,v in dfs.items()}

words_top = [(k,v) for k,v in idfs.items()]
print(words_top[:100])
tfidf = []
for doc in tf:
    tfidf_elem = {}
    for k,v in doc.items():
        tfidf_elem[k] = v*idfs[k]
    tfidf.append(tfidf_elem)

