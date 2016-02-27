from __future__ import print_function, division
from func import *
import pickle
from demos import cmd

def _test(filename):
    filepath='../Cleaned_Data/'
    filetype='.txt'
    Classify=do_SVM
    repeats=10

    label,matrix=preprocess(filepath+filename+filetype)
    result={}
    for key in set(label):
        result[key]=[]
    result['F_M']=[]
    for i in xrange(repeats):
        train,test=split_data(label)
        clf=Classify(label[train],matrix[train])
        prediction=clf.predict(matrix[test])
        dict_tmp=evaluate(label[test],prediction)
        for key in dict_tmp:
            result[key].append(dict_tmp[key])
    print(result)



if __name__ == '__main__':
    eval(cmd())
