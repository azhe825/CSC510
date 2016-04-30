import os
import csv


def extract_feature():
    base = os.path.abspath(os.path.dirname(__file__))
    csvpath = os.path.join(base, 'dataCollectionInCSV')
    events = [event for event in os.listdir(csvpath) if event.__contains__('event')]
    comments = [comment for comment in os.listdir(csvpath) if comment.__contains__('comment')]
    group_features1 = process_event(csvpath, events)
    group_features2 = process_comment(csvpath, comments)
    generate_assignees_csv(base, group_features1)
    generate_issueDuration_csv(base, group_features1)
    generate_userCommentNum_csv(base, group_features2)
    generate_issueCommentNum_csv(base, group_features2)
    generate_issueParticipants_csv(base, group_features2)
    print 'csv generated'


def process_comment(csvpath, comments):
    group_features = {}
    for group in comments:
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            user_comments = {}
            issue_comments = {}
            issue_uniqeUser = {}
            reader = csv.DictReader(csvinput)
            ## begin extract information from each row, i.e. event.
            for row in reader:
                ## (5) Number of People Commenting on an Issue
                user = (row['user'].split('/'))[1]
                if not user_comments.get(user):
                        user_comments[user] = 1
                user_comments[user] += 1

                ## (8) Number of Comments on an Issue
                issueID = row['issueID']
                if not issue_comments.get(issueID):
                        issue_comments[issueID] = 1
                issue_comments[issueID] += 1

                ## (11) Percentage of Comments by User
                if not issue_uniqeUser.get(issueID):
                        issue_uniqeUser[issueID] = set([user])
                issue_uniqeUser[issueID].add(user)
        groupID = (group.split('-'))[0][5:]
        if not group_features.get(groupID):
            group_features[groupID] = {}
        group_features[groupID]['User: CommentNum'] = user_comments
        group_features[groupID]['Issues: CommentNum'] = issue_comments
        group_features[groupID]['Issues: Participants'] = {k: len(v) for k,v in issue_uniqeUser.iteritems()}
        print  group + ' finished'
    return group_features


def process_event(csvpath, events):
    group_features = {}
    for group in events:
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            issue_times = {}
            user_assigned = {}
            reader = csv.DictReader(csvinput)
            ## begin extract information from each row, i.e. event.
            for row in reader:
                ## (1) Long Open Issues
                issueID = row['issueID']
                if not issue_times.get(issueID):
                    issue_times[issueID] = [row['time']]
                else:
                    issue_times[issueID].append(row['time'])

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
        group_features[groupID]['Issue Times'] = issue_times
        group_features[groupID]['Issue Duration'] = {k: get_duration(v) for k,v in issue_times.iteritems()}
        print  group + ' finished'
    return group_features


def get_duration(times):
    "return time in days"
    if len(times) <= 1:
        return 0
    else:
        return (int(max(times))-int(min(times))) / (24*3600)


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


def generate_userCommentNum_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/userCommentNum.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['User: CommentNum']
            users = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update(dict)
            fileds = ['groupID']
            fileds.extend(users)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)


def generate_issueDuration_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/issueDuration.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issue Duration']
            issues = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update(dict)
            fileds = ['groupID']
            fileds.extend(issues)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)


def generate_issueCommentNum_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/issueCommentNum.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issues: CommentNum']
            issues = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update(dict)
            fileds = ['groupID']
            fileds.extend(issues)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)


def generate_issueParticipants_csv(base, group_features):
    result_file = csvpath = os.path.join(base, 'featureCSV/issueParticipants.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issues: Participants']
            issues = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update(dict)
            fileds = ['groupID']
            fileds.extend(issues)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)


if __name__ == "__main__":
    extract_feature()