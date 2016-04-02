from __future__ import print_function, division
from pdb import set_trace

from time import time
from scipy.sparse import csr_matrix

from sklearn.neighbors import NearestNeighbors
from random import randint,random,shuffle
from sklearn import svm
from sklearn import neighbors
from sklearn.naive_bayes import GaussianNB,  MultinomialNB
from sklearn.feature_extraction import FeatureHasher
from sklearn import naive_bayes
from sklearn import tree
from sklearn.decomposition import LatentDirichletAllocation

from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import numpy as np
import pickle
from ABCD import ABCD
import cPickle

"save results"
def save(data,filename):
    cPickle.dump(data,open('../Results/'+filename+'.p','wb'))

"load results"
def load(filename):
    return cPickle.load(open('../Results/'+filename+'.p', 'rb'))

"Load data from txt"
def readfile(filename):
    corpus=[]
    label=[]
    with open(filename,'r') as f:
        for doc in f.readlines():
            try:
                corpus.append(doc.split(" ::::::>>>>>> ")[1][:-2])
                label.append(doc.split(" ::::::>>>>>> ")[0])
            except:
                pass

    label=np.array(label)

    return label, corpus

"Calculate iqr"
def iqr(array):
    return np.percentile(array,75)-np.percentile(array,25)

"Vector Space Model, input: list of str, output: list of dict"
def vsm(corpus):
    # tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=20000,
    #                                 stop_words='english')
    # return tf_vectorizer.fit_transform(corpus)
    return [Counter(row.split()) for row in corpus]




"Hash"
def hash(matrix,feature_number=4000):
    hasher = FeatureHasher(n_features=feature_number, non_negative=True)
    X=hasher.transform(matrix)
    return X

"Preprocessing, Vector space model"
def preprocess(filename):
    label, corpus=readfile(filename)
    matrix=vsm(corpus)
    matrix=hash(matrix)
    matrix=l2normalize(matrix)
    return label, matrix


"Topic Model"
def LDA(matrix,preserve,n_topics=100):

    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=10,
                                        learning_method='online', learning_offset=50.,
                                        random_state=randint(1,100))
    lda.fit(matrix[preserve])
    topic_model=lda.transform(matrix)

    return topic_model

"Shuffle"
def shuffle_tuple(my_tuple):
    tmp=[]
    aa=[]
    for i,array in enumerate(my_tuple):
        if not i:
            tmp=range(len(array))
            shuffle(tmp)
        aa.append(array[tmp])
    return tuple(aa)

"L2 normalization"
def l2normalize(mat):
    mat=mat.asfptype()
    for i in xrange(mat.shape[0]):
        nor=np.linalg.norm(mat[i].data,2)
        if not nor==0:
            for k in mat[i].indices:
                mat[i,k]=mat[i,k]/nor
    return mat

"Split data into training and testing"
def split_data(label,num_each=10):
    train=[]
    for ll in set(label):
        index=[i for i in xrange(len(label)) if label[i]==ll]
        train.extend(list(np.random.choice(index,size=num_each,replace=False)))
    test=list(set(range(len(label)))-set(train))
    return train,test

"Split each sub-folder into training(50%) and testing(50%)"
def split_data_50(label,num_each=10):
    train=[]
    for ll in set(label):
        index=[i for i in xrange(len(label)) if label[i]==ll]
        train.extend(list(np.random.choice(index,size=len(index)*0.5,replace=False)))
    test=list(set(range(len(label)))-set(train))
    return train,test




"Concatenate two csr into one (equal num of columns)"
def csr_vstack(a,b):
    data=np.array(list(a.data)+list(b.data))
    ind=np.array(list(a.indices)+list(b.indices))
    indp=list(a.indptr)+list(b.indptr+a.indptr[-1])[1:]
    return csr_matrix((data,ind,indp),shape=(a.shape[0]+b.shape[0],a.shape[1]))

"smote only oversample"
def smote_most(data,label,k=5):
    labelCont=Counter(label)
    # num=int(sum(labelCont.values())/len(labelCont.values()))
    num=int(np.max(labelCont.values()))
    labelmade=[]
    balanced=[]
    for l in labelCont:
        id=[i for i,x in enumerate(label) if x==l]
        sub=data[id]
        labelmade+=[l]*num
        if labelCont[l]<num:
            num_s=num-labelCont[l]
            nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='brute').fit(sub)
            distances, indices = nbrs.kneighbors(sub)
            row=[]
            column=[]
            new=[]
            for i in xrange(num_s):
                mid=randint(0,sub.shape[0]-1)
                nn=indices[mid,randint(1,k)]
                indx=list(set(list(sub[mid].indices)+list(sub[nn].indices)))
                datamade=[]
                for j in indx:
                    gap=random()
                    datamade.append((sub[nn,j]-sub[mid,j])*gap+sub[mid,j])
                row.extend([i]*len(indx))
                column.extend(indx)
                new.extend(datamade)
            mat=csr_matrix((new, (row, column)), shape=(num_s, sub.shape[1]))
            if balanced == []:
                balanced=mat
            else:
                balanced=csr_vstack(balanced,mat)
            balanced=csr_vstack(balanced,sub)
        else:
            ind=np.random.choice(labelCont[l],num,replace=False)
            if balanced == []:
                balanced=sub[ind]
            else:
                balanced=csr_vstack(balanced,sub[ind])
    labelmade=np.array(labelmade)
    return balanced, labelmade


"Classifier: linear SVM"
def do_SVM_noSMOTE(label,data):
    clf = svm.SVC(probability=True,kernel='linear')
    clf.fit(data,label)
    return clf

"Classifier: linear SVM"
def do_SVM(label,data):
    # data,label=smote_most(data,label)
    clf = svm.SVC(probability=True,kernel='linear')
    clf.fit(data,label)
    return clf

"Classifier: KNN"
def do_KNN(label,data):
    # tried 5, 10 , 15, 20.   10 performs best.
    n_neighbors = 10
    knn = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')  # or 'distance'
    clf = knn.fit(data, label)
    return clf

# "Classifier: Gaussian Naive-Bayes"
# def do_GNB(label,data):
#     gnb = GaussianNB()
#     clf = gnb.fit(data, label)
#     return clf

"Classifier: Multinomial Naive-Bayes"
def do_MNB(label,data):
    mnb = MultinomialNB()
    clf = mnb.fit(data, label)
    return clf

"Classifier: Decision Tree"
def do_DT(label,data):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, label)
    return clf


"Evaluation"
def evaluate(true_label,prediction):
    dict={}
    labellist=set(true_label)
    abcd=ABCD(before=true_label,after=prediction)
    tmp = np.array([k.stats() for k in abcd()])
    for i,label in enumerate(labellist):
        dict[label]=tmp[i,-2]  # f-score
    pre=np.mean(tmp[:,1])
    rec=np.mean(tmp[:,0])
    if pre==0 or rec==0:
        dict['F_M']=0
    else:
        dict['F_M']=2*pre*rec/(pre+rec)
    return dict










