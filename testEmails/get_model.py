import os
import scipy
import numpy
import nltk
import gensim
import cPickle

MAX_Training_Emails = 10
class_attr_separator = " ::::::>>>>>> "
subject_boday_separator = " ****** "
user_cat_text_Dict = {}
textdata = []
user_set = set()
user_corpus = []
u_count = 0
categories = {}
stopwords = set(nltk.corpus.stopwords.words('english'))
CategoryRemoveList = ['all_documents', '_sent_mail', 'inbox', 'outbox', 'sent_items', 'sent', 'deleted_items']

with open('./dataset.txt', "r") as data:
    for line in data:
            words = [w.lower() for w in line.strip().split() if len(w)>=3 and w not in stopwords]
            header = words[0].split('/')
            userID = header[1]
            category = ''.join(header[2:])
            if category in CategoryRemoveList:
                continue
            user_set.add(userID)
            if not categories.has_key(category):
                training_count = 1
                categories.update({category: training_count})
            print userID + '' + category
            words = words[2:]
            rm = words.index(subject_boday_separator.strip())
            words.pop(rm)
            if u_count != len(user_set):
                user_corpus.append([])
                u_count = u_count + 1
            if categories.get(category) < MAX_Training_Emails:
                user_corpus[u_count-1] = user_corpus[u_count-1] + words
                training_count = training_count + 1
                categories.update({category: training_count})
            else:
                continue
            # subjectFlag = True
            # subject_words = []
            # body_words = []
            # for w in words[2:]:
            #     if w == subject_boday_separator.strip():
            #         subjectFlag = False
            #     if subjectFlag:
            #         subject_words.append(w)
            #     else:
            #         if w != subject_boday_separator.strip():
            #             body_words.append(w)
            # text_Tuple = (subject_words, body_words)
            # print subject_words
            # if user_cat_text_Dict.has_key(userID):
            #     if user_cat_text_Dict[userID].has_key(category):
            #         user_cat_text_Dict[userID][category].append(text_Tuple)
            #     else:
            #         user_cat_text_Dict[userID][category] = [text_Tuple]
            # else:
            #     user_cat_text_Dict[userID] = {}
            #     user_cat_text_Dict[userID][category] = [text_Tuple]

    print 'done 1'
    cPickle.dump(user_corpus,open('user_corpus.p','wb'))
    b = cPickle.load(open('user_corpus.p', 'rb'))
    print 'done 2'