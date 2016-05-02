from __future__ import print_function, division
from pdb import set_trace
import csv


import numpy as np

from sklearn import svm
from feature_score import Score

def evaluate(true_label,prediction):
    m=len(true_label)
    n=len(true_label[0])
    return [sum([1 if true_label[i][j]==prediction[i][j] else 0 for i in range(m)])/m for j in range(n)]

def readcsv(file):
    allBadSmells = []
    with open(file) as fin:
        cr = csv.reader(fin)
        rNum = 0
        for row in cr:
            if rNum == 0:
                header = row
            else:
                allBadSmells.append(map(float, row[1:]))
            rNum += 1
    return allBadSmells

if __name__ == "__main__":
    score=Score()
    train=[0,1,5,6,9,11,12]
    test=list(set(range(len(score)))-set(train))
    filename="./badSmellScoreCSV_early/allBadSmell.csv"
    data=readcsv(filename)

    set_trace()
    print()




