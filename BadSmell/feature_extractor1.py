import os
import csv
import operator

def extract_feature():
    base = os.path.abspath(os.path.dirname(__file__))
    csvpath = os.path.join(base, 'dataCollectionInCSV')
    events = [event for event in os.listdir(csvpath) if event.__contains__('event')]
    comments = [comment for comment in os.listdir(csvpath) if comment.__contains__('comment')]
    group_features = process_event(csvpath, events)
    group_features1 = process_comment(csvpath, comments)
    #generate_events_csv(base, group_features)
    #generate_events_csv(base, group_features1)


def process_event(csvpath, events):
    group_features = {}
    for group in events:
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            groupid=''
            dict={}
            reader = csv.DictReader(csvinput)
            for row in reader:
                groupid=row['user'].split('/')[0]
                if row['user'].split('/')[1] in dict.keys():
                    dict[row['user'].split('/')[1]]+=1
                else:
                    dict[row['user'].split('/')[1]]=1
            group_features[groupid]=dict
    return group_features

def process_comment(csvpath, comments):
    group_features = {}
    for group in comments:
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            groupid=''
            dict={}
            i=1
            reader = csv.DictReader(csvinput)
            sortedlist = sorted(reader, key=lambda d: int(d['issueID']))
            for row in sortedlist:
                groupid=row['user'].split('/')[0]
                if row['issueID']==str(i):
                    if row['user'].split('/')[1] in dict.keys():
                        dict[row['user'].split('/')[1]]+=1
                    else:
                        dict[row['user'].split('/')[1]]=1
                i+=1
            group_features[groupid]=dict
    return group_features

def generate_events_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/Actions.csv')
    with open(result_file, 'w') as csvinput:
        fileds = ['groupID', 'users','actions']
        writer = csv.DictWriter(csvinput, fieldnames=fileds)
        writer.writeheader()
        for groupID in group_features.keys():
            dict = group_features[groupID]
            for users in dict.keys():
                writer.writerow({'groupID': groupID, 'users':users, 'actions':dict[users]})


if __name__ == "__main__":
    extract_feature()