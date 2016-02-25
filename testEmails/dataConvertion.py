import sys
import collections
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
random.seed(0)
# nltk.download("stopwords") # download stopwords if you don't have

ThresLength = 3
class_attr_separator = " ::::::>>>>>> "
subject_boday_separator = " ****** "
ThresEmailCount = 5
CategoryRemoveList = ['all_documents', '_sent_mail']
NumberOfFeatures = 300

#if len(sys.argv) != 2:
    #print "python dataConversion.py <path_to_datafile>"
    #exit(1)
path_to_datafile = "./dataset.txt"

def main():
    user_set, user_cat_text_Dict = load_data(path_to_datafile)
    wordVectors, category_list = convert_to_vector(user_set, user_cat_text_Dict)
    saveFeatures(user_set, category_list, wordVectors)
    #print len(category_list[0])
    #print wordVectors[0][0]


def load_data(path_to_dir):
    """
    Loads the text data set collected, and parse the hierarchical info into a layered dictionary
    """
    user_cat_text_Dict = {}
    textdata = []
    user_set = set();
    categories = []
    stopwords = set(nltk.corpus.stopwords.words('english'))
    with open(path_to_datafile, "r") as ftext:
        for line in ftext:
            words = [w.lower() for w in line.strip().split() if len(w)>=ThresLength and w not in stopwords]
            header = words[0].split('/')
            userID = header[1]
            category = header[2]
            if category in CategoryRemoveList:
                continue
            user_set.add(userID)
            categories.append(category)
            subjectFlag = True
            subject_words = []
            body_words = []
            for w in words[2:]:
                if w == subject_boday_separator.strip():
                    subjectFlag = False
                if subjectFlag:
                    subject_words.append(w)
                else:
                    if w != subject_boday_separator.strip():
                        body_words.append(w)
            text_Tuple = (subject_words, body_words)
            if user_cat_text_Dict.has_key(userID):
                if user_cat_text_Dict[userID].has_key(category):
                    user_cat_text_Dict[userID][category].append(text_Tuple)
                else:
                    user_cat_text_Dict[userID][category] = [text_Tuple]
            else:
                user_cat_text_Dict[userID] = {}
                user_cat_text_Dict[userID][category] = [text_Tuple]
    return user_set, user_cat_text_Dict

def convert_to_vector(user_set, user_cat_text_Dict):
    wordVectors = []
    label_list = []
    for userID in user_set:
        labels = []
        email_words = []
        category_list = user_cat_text_Dict[userID].keys()
        for cat in category_list:
            text = []
            if len(user_cat_text_Dict[userID][cat]) < ThresEmailCount:
                continue
            labels.append(cat)
            for term in user_cat_text_Dict[userID][cat]:
                text.extend(term[0])
                text.extend(term[1])
            email_words.append(' '.join(text))
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=NumberOfFeatures, stop_words='english')
        tf = tf_vectorizer.fit_transform(email_words)
        label_list.append(labels)
        wordVectors.append(tf)
    return wordVectors, label_list

def saveFeatures(user_set, category_list, wordVectors):
    user_index = 0
    fout = open("output.txt", 'w')
    for userID in user_set:
        fout.write("<<<<<<" + userID + "\n")
        cat_index = 0
        for cat in category_list[user_index]:
            fout.write(cat + "; ")
            fout.write(str(wordVectors[user_index][cat_index]))
            fout.write("\n")
            cat_index += 1
        user_index += 1
        fout.write(">>>>>>"+'\n')
    fout.close()


if __name__ == "__main__":
    main()