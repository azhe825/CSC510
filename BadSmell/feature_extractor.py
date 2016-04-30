import os
import csv


def extract_feature():
    base = os.path.abspath(os.path.dirname(__file__))
    csvpath = os.path.join(base, 'dataCollectionInCSV')
    events = [event for event in os.listdir(csvpath) if event.__contains__('event')]
    group_features = {}
    for group in events:
        with open(os.path.join(csvpath,group),'r') as csvinput:
            user_assigned = {}
            reader = csv.DictReader(csvinput)
            ## begin extract information from each row, i.e. event.
            for row in reader:
                ## (4)  Equal Number of Issue Assignees
                if row['action'] == 'assigned':
                    user = (row['user'].split('/'))[1]
                    if not user_assigned.get(user):
                        user_assigned[user] = [row['issueID']]
                    else:
                        user_assigned[user].append(row['issueID'])
        groupID = (group.split('-'))[0][5:]
        if not group_features.get(groupID):
            group_features[groupID] = {}
        group_features[groupID]['Issue Assignees'] = user_assigned
        print  group + ' finished'
    generate_assignees_csv(base, group_features)
    print 'csv generated'

def generate_assignees_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/issueAssignees.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issue Assignees']
            users = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update({user: len(issues) for user, issues in dict.iteritems()})
            fileds = ['groupID']
            fileds.extend(users)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)



if __name__ == "__main__":
    extract_feature()