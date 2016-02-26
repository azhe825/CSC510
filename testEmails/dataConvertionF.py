import sys
import collections
import nltk
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
random.seed(0)
# nltk.download("stopwords") # download stopwords if you don't have



def main():
    user_set, user_cat_text_Dict = load_data()
    wordVectors, category_list = convert_to_vector(user_set, user_cat_text_Dict)
    saveFeatures("wordVectors.txt" ,user_set, category_list, wordVectors)


def load_data(path_to_datafile = "./dataset.txt", ThresWordLength = 3, CategoryRemoveList = ['all_documents', '_sent_mail' 'inbox', 'outbox', 'sent_items', 'sent', 'deleted_items']):
    """
    Loads the text data set collected, and parse the hierarchical info into a layered dictionary. Use ThresWordLength to filter out the short word. And CategoryRemoveList is to remove unrelated user subfolders.
    """
    class_attr_separator = " ::::::>>>>>> "
    subject_boday_separator = " ****** "
    user_cat_text_Dict = {}
    textdata = []
    user_set = set();
    categories = []
    stopwords = set(nltk.corpus.stopwords.words('english'))
    with open(path_to_datafile, "r") as ftext:
        for line in ftext:
            words = [w.lower() for w in line.strip().split() if len(w)>=ThresWordLength and w not in stopwords]
            header = words[0].split('/')
            userID = header[1]
            category = '_'.join(header[2:])
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

def convert_to_vector(user_set, user_cat_text_Dict, ThresEmailCountMin = 5, ThresEmailCountMax = 100, NumberOfFeatures = 4000):
    """
    Convert all selected emails into word vectors using TF values
    """
    wordVectors = []
    label_list = []
    for userID in user_set:
        labels = []
        email_words = []
        category_list = user_cat_text_Dict[userID].keys()
        for cat in category_list:
            text = []
            if len(user_cat_text_Dict[userID][cat]) < ThresEmailCountMin or len(user_cat_text_Dict[userID][cat]) > ThresEmailCountMax:
                continue
            for term in user_cat_text_Dict[userID][cat]:
                text.extend(term[0])
                text.extend(term[1])
                email_words.append(' '.join(text))
                labels.append(cat)
        label_list.append(labels)
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=NumberOfFeatures, stop_words='english')
        tf = tf_vectorizer.fit_transform(email_words)
        wordVectors.append(tf.toarray().tolist())
    return wordVectors, label_list

def saveFeatures(save_to_file, user_set, label_list, wordVectors):
    fout = open(save_to_file, 'w')
    user_index = 0
    for userID in user_set:
        fout.write("<<<<<<" + userID + "\n")
        for label_index, wvec in enumerate(wordVectors[user_index]):
            fout.write(label_list[user_index][label_index] + "; \n")
            fout.write(str(wvec))
            fout.write("\n")
        user_index += 1
        fout.write(">>>>>>"+'\n')
    fout.close()


if __name__ == "__main__":
    main()