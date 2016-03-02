__author__ = 'amrit'

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

if __name__ == '__main__':
    # "draw"
    F_final1 = {}
    path = '../Results/lda/dump/'
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            print(a)
            with open(a, 'rb') as handle:
                F_final = {}
                F_final = pickle.load(handle)
                F_final1 = dict(F_final1.items() + F_final.items())

    filenamelist = [
        'beck-s.txt', 'farmer-d.txt', 'kaminski-v.txt', 'kitchen-l.txt', 'lokay-m.txt', 'sanders-r.txt',
        'williams-w3.txt']
    # issmote = ["no_smote"]
    plt.figure(num=0, figsize=(20, 6))
    plt.subplot(121)
    X = range(len(filenamelist))
    print(F_final1)
    Y_median = []
    Y_iqr = []
    for i, filename in enumerate(filenamelist):
        Y = F_final1[filename]
        Y_median.append(np.median(Y))
        Y_iqr.append(np.percentile(Y, 75) - np.percentile(Y, 25))

    line, = plt.plot(X, Y_median, label="median")
    plt.plot(X, Y_iqr, "-.", color=line.get_color(), label="iqr")
    plt.xticks(X, filenamelist, size='xx-small')
    plt.ylabel("F score")
    plt.xlabel("Datasets")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0.)
    plt.savefig("lda_SVM_100.png")
