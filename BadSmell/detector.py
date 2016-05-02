from __future__ import print_function, division
from pdb import set_trace


import numpy as np

from sklearn import svm


def evaluate(true_label,prediction):
    m=len(true_label)
    n=len(true_label[0])
    return [sum([1 if true_label[i][j]==prediction[i][j] else 0 for i in range(m)])/m for j in range(n)]




