import os
import scipy
import numpy as np
import nltk
import gensim
import cPickle



def train():
    sentences = cPickle.load(open('user_corpus.p', 'rb'))
    model = model = gensim.models.Word2Vec(sentences, size=vector_size, window=5, min_count=1, workers=4)
    model.save('./Word2VectorModel')

def load():
    user_cat_text_Dict = cPickle.load(open('user_cat_text_Dict.p', 'rb'))
    user_set = cPickle.load(open('user_set.p', 'rb'))
    return user_set, user_cat_text_Dict

def main():
    #train()
    ## use model trained by user's corpus
    #model = gensim.models.Word2Vec.load('./Word2VectorModel')
    ##
    model = gensim.models.Word2Vec.load_word2vec_format('/Users/Jack/Downloads/GoogleNews-vectors-negative300.bin', binary=True)  # C binary format
    vector_size = 300
    user_set, user_cat_text_Dict = load()

    wordVectors = []
    label_list = []
    user_label = [None]*len(user_set)
    user_count = 0
    user_training_vector = []
    user_training_label = []
    for userID in user_set:
        training_vector = []
        training_label = []
        email_words = []
        cat_count = 0
        category_list = user_cat_text_Dict[userID].keys()
        for cat in category_list:
            cat_count = cat_count + 1
            category_vector = []
            category_label = []
            text = []
            email_count = len(user_cat_text_Dict[userID][cat])
            if  email_count < 10 or email_count > 100:
                continue
            else:
                for term in user_cat_text_Dict[userID][cat]:
                    text.extend(term[0])
                    text.extend(term[1])
                    doc_vector = [0 for t in range(vector_size)]
                    for word in text:
                        try:
                            word_vector = model[word]
                            #doc_vector = [x + y for x, y in zip(doc_vector,word_vector)]
                            doc_vector = np.add(doc_vector,word_vector)
                        except KeyError:
                            #print word + 'not in training corpus'
                            pass
                    category_vector.append(doc_vector)
                    category_label.append([cat_count])
                    print userID + ':' + cat
            training_vector.append(category_vector)
            training_label.append(category_label)
            cPickle.dump(training_vector,open('./new_subdata/training_vector_'+cat+'.p','wb'))
            cPickle.dump(training_label,open('./new_subdata/training_label_'+cat+'.p','wb'))
        user_training_vector.append(training_vector)
        user_training_label.append(training_label)
        cPickle.dump(user_training_vector,open('./new_subdata/user_training_vector_'+userID+'.p','wb'))
        cPickle.dump(user_training_label,open('./new_subdata/user_training_label_'+userID+'.p','wb'))


# for word in sentences[0]:
#     print word
#     try:
#         w_vector = model[word]
#     except KeyError:
#         print word + 'not in training corpus'
#         pass


# class_attr_separator = " ::::::>>>>>> "
# subject_boday_separator = " ****** "
# user_cat_text_Dict = {}
# textdata = []
# user_set = set()
# user_corpus = []
# u_count = 0
# categories = []
# stopwords = set(nltk.corpus.stopwords.words('english'))
# CategoryRemoveList = ['all_documents', '_sent_mail', 'inbox', 'outbox', 'sent_items', 'sent', 'deleted_items']

# with open('./dataset.txt', "r") as data:
#     for line in data:
#                 words = [w.lower() for w in line.strip().split() if len(w)>=3 and w not in stopwords]
#                 header = words[0].split('/')
#                 userID = header[1]
#                 category = ''.join(header[2:])
#                 if category in CategoryRemoveList:
#                     continue
#                 user_set.add(userID)
#                 if len(user_set) > 1:
#                     break
#                 print userID + '' + category
#                 categories.append(category)
#                 words = words[2:]
#                 rm = words.index(subject_boday_separator.strip())
#                 words.pop(rm)
#                 if u_count != len(user_set):
#                     user_corpus.append([])
#                     u_count = u_count + 1
#                 user_corpus[u_count-1] = user_corpus[u_count-1] + words
#                 # subjectFlag = True
#                 # subject_words = []
#                 # body_words = []
#                 # for w in words[2:]:
#                 #     if w == subject_boday_separator.strip():
#                 #         subjectFlag = False
#                 #     if subjectFlag:
#                 #         subject_words.append(w)
#                 #     else:
#                 #         if w != subject_boday_separator.strip():
#                 #             body_words.append(w)
#                 # text_Tuple = (subject_words, body_words)
#                 # print subject_words
#                 # if user_cat_text_Dict.has_key(userID):
#                 #     if user_cat_text_Dict[userID].has_key(category):
#                 #         user_cat_text_Dict[userID][category].append(text_Tuple)
#                 #     else:
#                 #         user_cat_text_Dict[userID][category] = [text_Tuple]
#                 # else:
#                 #     user_cat_text_Dict[userID] = {}
#                 #     user_cat_text_Dict[userID][category] = [text_Tuple]
#
#     print 'done 1'
#     cPickle.dump(user_corpus,open('user_corpus.p','wb'))
#     b = cPickle.load(open('user_corpus.p', 'rb'))
#     print 'done 2'


if __name__ == "__main__":
    main()