import os
import csv
import operator

def extract_feature():
    base = os.path.abspath(os.path.dirname(__file__))
    csvpath = os.path.join(base, 'dataCollectionInCSV')
    events = [event for event in os.listdir(csvpath) if event.__contains__('event')]
    group_features = process_event(csvpath, events)
    group_features1 = process_issues(csvpath, events)
    generate_events_csv(base, group_features)
    generate_issues_csv(base, group_features1)


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

def process_issues(csvpath, comments):
    group_features = {}
    for group in comments:
        with open(os.path.join(csvpath, group), 'r') as csvinput:

            groupid=group.split("-")[0]
            reader = csv.DictReader(csvinput)
            #sortedlist = sorted(reader, key=lambda d: int(d['issueID']))
            l=[]
            l_label=[]
            l_milestone=[]
            for row in reader:
                #print(row)
                if row['issueID'] not in l:
                    l.append(row['issueID'])
                if row['action']=='labeled':
                    if row['issueID'] not in l_label:
                        l_label.append(row['issueID'])
                if row['action']=='milestoned':
                    if row['issueID'] not in l_milestone:
                        l_milestone.append(row['issueID'])
            group_features[groupid]=[1-(float(len(l_label))/len(l)),1-(float(len(l_milestone))/len(l))]
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


def generate_issues_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/Issueswolabels.csv')
    with open(result_file, 'w') as csvinput:
        fileds = ['groupID', 'issueswolabels', 'issueswomilestones']
        writer = csv.DictWriter(csvinput, fieldnames=fileds)
        writer.writeheader()
        for groupID in group_features.keys():
                writer.writerow({'groupID': groupID, 'issueswolabels':group_features[groupID][0],'issueswomilestones':group_features[groupID][1]})


if __name__ == "__main__":
    extract_feature()