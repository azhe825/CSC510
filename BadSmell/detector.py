from __future__ import print_function, division
from pdb import set_trace
import csv


import numpy as np

from sklearn import svm
from feature_score import Score

def iqr(array):
    return np.percentile(array,75)-np.percentile(array,25)

def evaluate(true_label,prediction):
    m=len(true_label)
    n=len(true_label[0])
    return [sum([1 if true_label[i,j]==prediction[i,j] else 0 for i in range(m)])/m for j in range(n)]

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
    # train=[0,1,5,6,9,11,12]
    x=range(len(score))
    repeats=50
    accuracy=[]
    filename="./badSmellScoreCSV_early/allBadSmell.csv"
    data=readcsv(filename)
    for repeat in range(repeats):
        train=np.random.choice(x,7,replace=False)
        test=list(set(range(len(score)))-set(train))
        x_train=np.array(data)[train]
        y_train=np.array(score)[train]
        x_test=np.array(data)[test]
        y_test=np.array(score)[test]
        n_label=len(y_train[0])
        clf=[]
        for i in range(n_label):
            clf.append(svm.SVC(kernel='linear'))
            clf[i].fit(x_train,np.array(y_train)[:,i])
        y_pre=np.array([clf[i].predict(x_test) for i in range(n_label)]).transpose()
        acc=evaluate(y_test,y_pre)
        accuracy.append(acc)

    median=np.median(np.array(accuracy),axis=0)
    iqr=np.percentile(np.array(accuracy),75,axis=0)-np.percentile(np.array(accuracy),25,axis=0)
    set_trace()
    print()




