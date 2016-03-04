import os
import scipy
import numpy as np
import nltk
import cPickle
import gensim
from func import *
from gensim.models.doc2vec import TaggedDocument,LabeledSentence, Doc2Vec
from sklearn.metrics import precision_recall_fscore_support
import random
random.seed(0)
depth = 100

# "transform docmument list to Word Vector matrix"
# def get_WordVector_matrix(document):
#     model = Doc2Vec.load('./WordVector_model.d2v')
#     matrix = []
#     for doc in document:
#         doc_vector = model.docvecs[doc[1][0]]
#         matrix.append(doc_vector[0])


"Load document format for building WordVector model"
def get_documents(corpus,label):
    document=[]
    for i in range(len(label)):
        sentence = LabeledSentence(corpus[i][0].split(' '), [str(i)])
        document.append(sentence)
    return document

def train_WordVector_model(document,label):
    model = Doc2Vec(min_count=1, window=10, size=depth, workers=4)
    model.build_vocab(document)
    for i in range(5):
        print "Training iteration %d" %(i)
        random.shuffle(document)
        model.train(document)
    model.save('./WordVector_model.d2v')

"transform docmument list to Word Vector matrix"
def get_WordVector_matrix(label):
    model = Doc2Vec.load('./WordVector_model.d2v')
    size = len(label)
    vectors = np.zeros((size,depth))
    for i in range(size):
        try:
            doc_vector = model.docvecs[str(i)]
            vectors[i]=(doc_vector[0])
        except KeyError:
            print str(i) + ' occurs KeyError'
            pass
    return map(list,vectors)



filepath='../Cleaned_Data/'
filetype='.txt'
datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']
corpus=[]
label=[]
for dataset in datalist:
    filename = filepath+dataset+filetype
    tmp_label, tmp_corpus = readfile(filename)
    tmp_label = map(lambda x:[x], tmp_label)
    tmp_corpus = map(lambda x:[x], tmp_corpus)
    corpus.extend(tmp_corpus)
    label.extend(tmp_label)
document = get_documents(corpus,label)
# train_WordVector_model(document,label)
matrix = get_WordVector_matrix(label)
label = map(lambda x:x[0],label)
Classify = do_SVM_noSMOTE
train,test=split_data_50(label)
train_vectors = [matrix[i] for i in train]
test_vectors =  [matrix[i] for i in test]
train_label = [label[i] for i in train]
test_label = [label[i] for i in test]
clf=Classify(train_label,train_vectors)
prediction=clf.predict(test_vectors)
result = evaluate(test_label,prediction)
y_true = np.array(test_label)
y_pred = np.array(prediction)
print precision_recall_fscore_support(y_true, y_pred, average='macro')
# >>> (0.0028935031532752618, 0.013399361812185769, 0.0036415252615324602, None)