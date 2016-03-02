from __future__ import print_function, division

__author__ = 'amrit'

import re
from time import time
from demos import atom
from demos import cmd
import sys
import numpy as np
from sklearn import svm
from sklearn.feature_extraction import FeatureHasher
from random import randint, random, seed, shuffle
from time import time
from ABCD import ABCD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pickle


def get_top_words(model, feature_names, n_top_words):
    a=[]
    for topic_idx, topic in enumerate(model.components_):
        #print("Topic #%d:" % topic_idx)
        a.append([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]])
    return a

def token_freqs(doc):
    return Counter(doc[1:])

"tf"

def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat

"tf-idf"

def tf_idf(mat):
    docs = len(mat)
    word = {}
    doc = {}
    words = 0
    for row in mat:
        for key in row.keys():
            words += row[key]
            try:
                word[key] += row[key]
            except:
                word[key] = row[key]
            try:
                doc[key] += 1
            except:
                doc[key] = 1
    tfidf = {}
    for key in doc.keys():
        tfidf[key] = word[key] / words * np.log(docs / doc[key])
    return tfidf

"L2 normalization"


def l2normalize(mat):
    for row in mat:
        n = 0
        for key in row:
            n += row[key] ** 2
        n = n ** 0.5
        for key in row:
            row[key] = row[key] / n
    return mat


"hashing trick"


def hash(mat, n_features=1000):
    hasher = FeatureHasher(n_features=n_features)
    X = hasher.transform(mat)
    X = X.toarray()
    return X


tfidf_temp = {}
filename_global = ""
lastfile = ""

"make feature matrix"


def make_feature(corpus, method="tfidf", n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    if method == "tfidf":
        tfidf = tf_idf(mat)
        keys = np.array(tfidf.keys())[np.argsort(tfidf.values())][-n_features:]
        matt = []
        for row in mat:
            matt.append([row[key] for key in keys])
        matt = np.array(matt)
        # matt=norm(matt)


        "Store tfidf_temp for drawing"
        global tfidf_temp
        if filename_global not in tfidf_temp.keys():
            tfidf_temp[filename_global] = np.sort(tfidf.values())


    else:
        matt = hash(mat, n_features=n_features)
       # matt = norm(matt)
    return matt, label

def cmd(com="demo('-h')"):
    "Convert command line to a function call."
    if len(sys.argv) < 2: return com

    def strp(x): return isinstance(x, basestring)

    def wrap(x): return "'%s'" % x if strp(x) else str(x)

    words = map(wrap, map(atom, sys.argv[2:]))
    return sys.argv[1] + '(' + ','.join(words) + ')'


"split data according to target label"


def split_two(corpus, label, target_label):
    pos = []
    neg = []
    for i, lab in enumerate(label):
        if lab == target_label:
            pos.append(i)
        else:
            neg.append(i)
    positive = corpus[pos]
    negative = corpus[neg]
    return {'pos': positive, 'neg': negative}


def do_SVM(train_data, test_data, train_label, test_label):
    clf = svm.LinearSVC(dual=False)
    clf.fit(train_data, train_label)
    prediction = clf.predict(test_data)
    abcd = ABCD(before=test_label, after=prediction)
    F = np.array([k.stats()[-2] for k in abcd()])
    labeltwo = list(set(test_label))
    if labeltwo[0] == 'positive':
        labelone = 0
    else:
        labelone = 1
    try:
        return F[labelone]
    except:
        pass


def readfile(filename='', thres=[0.02, 0.05]):
    dict = []
    label = []
    targetlabel = []
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                row = doc.lower().split(' ::::::>>>>>> ')[1]
                label.append(doc.lower().split(' ::::::>>>>>> ')[0].split()[0])
                dict.append(row)
            except:
                pass
    labellst = Counter(label)
    n = sum(labellst.values())
    while True:
        for l in labellst:
            if labellst[l] > n * thres[0] and labellst[l] < n * thres[1]:
                targetlabel = l
                break
        if targetlabel:
            break
        thres[1] = 2 * thres[1]
        thres[0] = 0.5 * thres[0]
    print(targetlabel)
    for i, l in enumerate(label):
        if l == targetlabel:
            label[i] = 'pos'
        else:
            label[i] = 'neg'
    label = np.array(label)
    return label, dict


def _test_LDA(file='cs'):
    n_topics = 100
    n_top_words = 20
    n_samples = 2000
    n_features = 4000

    fileB = [
        'beck-s.txt' , 'farmer-d.txt', 'kaminski-v.txt', 'kitchen-l.txt', 'lokay-m.txt', 'sanders-r.txt', 'williams-w3.txt']

    filename = "../Cleaned_Data/"
    Score = []

    def cross_split(corpus, folds, index):
        i_major = []
        i_minor = []
        l = len(corpus)
        for i in range(0, folds):
            if i == index:
                i_minor.extend(range(int(i * l / folds), int((i + 1) * l / folds)))
            else:
                i_major.extend(range(int(i * l / folds), int((i + 1) * l / folds)))
        return corpus[i_minor], corpus[i_major]

    "generate training set and testing set"

    def train_test(pos, neg, folds, index):
        pos_train, pos_test = cross_split(pos, folds=folds, index=index)
        neg_train, neg_test = cross_split(neg, folds=folds, index=index)
        data_train = np.vstack((pos_train, neg_train))
        data_test = np.vstack((pos_test, neg_test))
        label_train = ['pos'] * len(pos_train) + ['neg'] * len(neg_train)
        label_test = ['pos'] * len(pos_test) + ['neg'] * len(neg_test)

        "Shuffle"
        tmp = range(0, len(label_train))
        shuffle(tmp)
        data_train = data_train[tmp]
        label_train = np.array(label_train)[tmp]

        tmp = range(0, len(label_test))
        shuffle(tmp)
        data_test = data_test[tmp]
        label_test = np.array(label_test)[tmp]

        return data_train, data_test, label_train, label_test

    F_final = {}
    for file1 in fileB:
        with open(filename + str(file1), 'r') as f:
            file = open(filename + str(file1) + "1", "w+")
            for doc in f.readlines():
                file.write(re.sub(r'\s+', ' ', doc) + "\n")
                # file.close()
        # targetlist and corpus
        label, data_samples = readfile(filename + str(file1) + "1")
        target_label = 'pos'
        ra = Counter(label)["pos"] / len(label)


        # Use tf (raw term count) features for LDA.
        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                        stop_words='english')
        t0 = time()
        tf = tf_vectorizer.fit_transform(data_samples)
        print("done in %0.3fs." % (time() - t0))

        # print(tf)
        print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
              % (n_samples, n_features))
        lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                        learning_method='online', learning_offset=50.,
                                        random_state=0)
        t0 = time()
        tf_new = lda.fit_transform(tf)
        print("done in %0.3fs." % (time() - t0))
        #topic_tf = [np.argmax(x) for x in tf_new]
        tf_feature_names = tf_vectorizer.get_feature_names()
        corpus= get_top_words(lda, tf_feature_names, n_top_words)
        #data, label1 = make_feature(corpus, method='tf', n_features=1000)
        split = split_two(corpus=tf_new, label=label, target_label=target_label)
        pos = split['pos']
        neg = split['neg']
        result = []
        folds = 5
        for i in range(folds):
            tmp = range(0, len(pos))
            shuffle(tmp)
            pos = pos[tmp]
            tmp = range(0, len(neg))
            shuffle(tmp)
            neg = neg[tmp]
            for index in range(folds):
                data_train, data_test, label_train, label_test = \
                    train_test(pos, neg, folds=folds, index=index)
                "SVM"
                result.append(do_SVM(data_train, data_test, label_train, label_test))
        F_final[file1] = result
    with open('../Results/lda/dump/'+'r'+'.pickle', 'wb') as handle:
        pickle.dump(F_final, handle)

if __name__ == '__main__':
    eval(cmd())
