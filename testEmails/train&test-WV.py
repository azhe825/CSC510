import sys
from sklearn import svm
import numpy as np
import cPickle
from ABCD import ABCD
from collections import Counter

user_training_label = cPickle.load(open('./subdata/user_training_label_beck-s.p', 'rb'))
user_training_vector = cPickle.load(open('./subdata/user_training_vector_beck-s.p', 'rb'))
category_vector = []
category_label = []
training_folder_vector = []
training_folder_label = []
test_folder_vector = []
test_folder_label = []
for training_vector in user_training_vector:
    i = user_training_vector.index(training_vector)
    training_label = user_training_label [i]
    for category_vector in training_vector:
        if(len(category_vector)<20):
            continue
        j = training_vector.index(category_vector)
        category_label = training_label[j]
        training_folder_vector.extend(category_vector[:10])
        training_folder_label.extend(category_label[:10])
        test_folder_vector.extend(category_vector[10:])
        test_folder_label.extend(category_label[10:])

new_training_folder_label = []
new_test_folder_label = []
for i in training_folder_label:
    new_training_folder_label.extend(i)
for i in test_folder_label:
    new_test_folder_label.extend(i)
print 'done'

clf = svm.SVC()
clf.fit(training_folder_vector, new_training_folder_label)
predict = clf.predict(test_folder_vector)
actual = new_test_folder_label
predict = predict.tolist()
abcd = ABCD(actual,predict)
F = np.array([k.stats()[4] for k in abcd()])
recall = np.array([k.stats()[0] for k in abcd()])
precision = np.array([k.stats()[2] for k in abcd()])
accuracy = np.array([k.stats()[3] for k in abcd()])
print 'done'