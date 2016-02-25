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
NumberOfFeatures = 300

#these two folder contains all the emails received and sent. No useful for our email labling jobs.
CategoryRemoveList = ['all_documents', '_sent_mail']

## Directly defined here. No need to download form nltk. Source is nltk.corpus.stopwords.words('english')
StopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']


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
    stopwords =[unicode(i) for i in StopWords]
    #stopwords = set(nltk.corpus.stopwords.words('english'))  ## requires to use nltk.download() at first. Removed for easy running.
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
            print cat + ' - ' + str(len(email_words))
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=NumberOfFeatures, stop_words='english')
        tf = tf_vectorizer.fit_transform(email_words)
        label_list.append(labels)
        wordVectors.append(tf.toarray())
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