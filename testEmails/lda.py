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
    a = []
    for topic_idx, topic in enumerate(model.components_):
        # print("Topic #%d:" % topic_idx)
        a.append([feature_names[i]
                  for i in topic.argsort()[:-n_top_words - 1:-1]])
    return a


def token_freqs(doc):
    return Counter(doc[1:])


"tf"


def tf(corpus):
    mat = [token_freqs(doc) for doc in corpus]
    return mat


def make_feature(corpus, n_features=1000):
    label = list(zip(*corpus)[0])
    mat = tf(corpus)
    matt = hash(mat, n_features=n_features)
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


def readfile1(filename='', thres=[0.0, 0.1]):
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
                targetlabel.append(label)
                break
        if targetlabel:
            break
        thres[1] = 2 * thres[1]
        thres[0] = 0.5 * thres[0]
    targetlabel = [item for sublist in targetlabel for item in sublist]
    #targetlabel=list(set(np.array(targetlabel)))
    return targetlabel, dict


def _test_LDA(file='cs'):
    n_topics = 100
    n_top_words = 20
    n_samples = 2000
    n_features = 4000

    fileB = [
        'beck-s.txt', 'farmer-d.txt', 'kaminski-v.txt', 'kitchen-l.txt', 'lokay-m.txt', 'sanders-r.txt', 'williams-w3.txt']

    filepath = "../Cleaned_Data/"

    F_final = {}
    for j, file1 in enumerate(fileB):
        with open(filepath + str(file1), 'r') as f:
            file = open(filepath + str(file1) + "1", "w+")
            for doc in f.readlines():
                file.write(re.sub(r'\s+', ' ', doc) + "\n")

        label, data_samples = readfile1(filepath + str(file1) + "1")

        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                        stop_words='english')
        tf = tf_vectorizer.fit_transform(data_samples)

        print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
              % (n_samples, n_features))
        lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                        learning_method='online', learning_offset=50.,
                                        random_state=0)
        t0 = time()
        tf_new = lda.fit_transform(tf)
        print("done in %0.3fs." % (time() - t0))
        tf_feature_names = tf_vectorizer.get_feature_names()
        corpus = get_top_words(lda, tf_feature_names, n_top_words)
        #data, label1 = make_feature(corpus, n_features=1000)
        #print(corpus)
        F_final = {}
        final_label=list(set(label))
        print(final_label[0:5])
        for x in range(5):
            split = split_two(corpus=tf_new, label=label, target_label=final_label[x])
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
            F_final[final_label[x]] = result
        plt.figure(num=j, figsize=(20, 6))
        plt.subplot(121)
        X = range(5)
        Y_median = []
        Y_iqr = []
        for i, filename in enumerate(final_label[0:5]):
            Y = F_final[filename]
            Y_median.append(np.median(Y))
            Y_iqr.append(np.percentile(Y, 75) - np.percentile(Y, 25))

        line, = plt.plot(X, Y_median, label="median")
        plt.plot(X, Y_iqr, "-.", color=line.get_color(), label="iqr")
        plt.xticks(X, (final_label[0:5]), size='xx-small')
        plt.ylabel("F score")
        plt.xlabel(file1)
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0.)
        plt.savefig("../Results/lda_"+file1+".png")
        with open('../Results/lda_dump/' + file1 + '.pickle', 'wb') as handle:
            pickle.dump(F_final, handle)


if __name__ == '__main__':
    eval(cmd())
