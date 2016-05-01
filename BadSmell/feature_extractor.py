import os
import csv
from pdb import set_trace
import pickle


def extract_feature(base, csvpath):
    events = [event for event in os.listdir(csvpath) if event.__contains__('event')]
    comments = [comment for comment in os.listdir(csvpath) if comment.__contains__('comment')]
    milestones = [milestone for milestone in os.listdir(csvpath) if milestone.__contains__('milestone')]
    # milestone_dict = get_milestone_dict(csvpath, milestones)
    milestone_dict = load_obj(os.path.join(csvpath, 'DictMilestone'))
    group_features1 = process_event(csvpath, events)
    group_features2 = process_comment(csvpath, comments)
    generate_assignees_csv(base, group_features1)
    generate_issueDuration_csv(base, group_features1)
    generate_issueMilestone_csv(base, group_features1)
    generate_issueDelay_csv(base, group_features1)
    generate_userCommentNum_csv(base, group_features2)
    generate_issueCommentNum_csv(base, group_features2)
    generate_issueParticipants_csv(base, group_features2)
    print 'csv generated'


def get_milestone_dict(csvpath, comments):
    group_dict = {}
    for group in comments:
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            milestone_dict = {}
            reader = csv.DictReader(csvinput)
            ## begin extract information from each row, i.e. event.
            for row in reader:
                tmp = {row['id']: {'created_at': row['created_at'], 'due_at': row['due_at'], 'closed_at': row['closed_at']}}
                milestone_dict.update(tmp)
        groupID = (group.split('-'))[0][5:]
        group_dict.update({groupID: milestone_dict})
    save_obj(group_dict, os.path.join(csvpath, 'DictMilestone'))
    return group_dict


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
    milestone_dict = load_obj(os.path.join(csvpath, 'DictMilestone'))
    group_features = {}
    for group in events:
        groupID = (group.split('-'))[0][5:]
        with open(os.path.join(csvpath, group), 'r') as csvinput:
            issue_times = {}
            issue_milestone = {}
            issue_delay = {}
            user_assigned = {}
            reader = csv.DictReader(csvinput)
            ## begin extract information from each row, i.e. event.
            for row in reader:
                issueID = row['issueID']
                ## (1) Issues Durations
                if not issue_times.get(issueID):
                    issue_times[issueID] = [row['time']]
                else:
                    issue_times[issueID].append(row['time'])

                ## Issue missing milestones
                if not issue_milestone.get(issueID):
                    issue_milestone[issueID] = row['milestone']

                ## (2) Issues delay for its milestone
                if row['action'] == 'closed' and row['milestone'] != '':
                    milestoneID = row['milestone']
                    tClose = row['time']
                    try:
                        ErrorFlag = 0
                        tDue = milestone_dict[groupID][milestoneID]['due_at']
                    except KeyError:
                        ErrorFlag = 1
                        print 'group ID: ' + groupID + ' milestone ID: ' + milestoneID
                    if not tDue or ErrorFlag:
                        delay = 0
                    else:
                        delay = (int(tDue)-int(tClose)) / (24*3600)
                    issue_delay[issueID] = delay

                ## (4)  Equal Number of Issue Assignees
                if row['action'] == 'assigned':
                    user = (row['user'].split('/'))[1]
                    if not user_assigned.get(user):
                        user_assigned[user] = [row['issueID']]
                    else:
                        user_assigned[user].append(row['issueID'])
        if not group_features.get(groupID):
            group_features[groupID] = {}
        group_features[groupID]['Issue Assignees'] = user_assigned
        group_features[groupID]['Issue Times'] = issue_times
        group_features[groupID]['Issue Delays'] = issue_delay
        group_features[groupID]['Issue Duration'] = {k: get_duration(v) for k,v in issue_times.iteritems()}
        group_features[groupID]['Issue Milestones'] = issue_milestone
        print  group + ' finished'
    return group_features


def get_duration(times):
    "return time in days"
    if len(times) <= 1:
        return 0
    else:
        return (int(max(times))-int(min(times))) / (24*3600)



def generate_assignees_csv(base, group_features):
    result_file = os.path.join(base, 'featureCSV/issueAssignees.csv')
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
    result_file = os.path.join(base, 'featureCSV/userCommentNum.csv')
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
    result_file = os.path.join(base, 'featureCSV/issueDuration.csv')
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


def generate_issueDelay_csv(base, group_features):
    result_file = os.path.join(base, 'featureCSV/issueDelay.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issue Delays']
            issues = dict.keys()
            input_data = {'groupID': groupID}
            input_data.update(dict)
            fileds = ['groupID']
            fileds.extend(issues)
            writer = csv.DictWriter(csvinput, fieldnames=fileds)
            writer.writeheader()
            writer.writerow(input_data)


def generate_issueMilestone_csv(base, group_features):
    result_file = os.path.join(base, 'featureCSV/issueMilestone.csv')
    with open(result_file, 'w') as csvinput:
        for groupID, feature in group_features.iteritems():
            dict = feature['Issue Milestones']
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


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def issueDiscussionScore():
    "for each issue, get the percentage of issues with < 3 followup comments"
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueCommentNum.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                commentNum = row[1:]
                lessParticipants3 = [i for i in commentNum if int(i) < 3]
                lessComment4 = [i for i in commentNum if int(i) < 4]
                # percentage of issues with less than 3 comments
                bad_smell[groupID] = {'Issue Discussions<3': float(len(lessParticipants3))/len(commentNum)}
                bad_smell[groupID].update({'Issue Discussions<4': (float(len(lessComment4))/len(commentNum))})
    return bad_smell


def issueParticipantScore():
    "for each issue, get the percentage of issues with < 50% participants"
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueParticipants.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                participantNum = row[1:]
                lessParticipants2 = [i for i in participantNum if int(i) < 2]
                lessParticipants3 = [i for i in participantNum if int(i) < 3]
                # percentage of issues with less than 3 comments
                bad_smell[groupID] = {'Issue Participant<2': float(len(lessParticipants2))/len(participantNum)}
                bad_smell[groupID].update({'Issue Participant<3': (float(len(lessParticipants3))/len(participantNum))})
    return bad_smell


def longOpenIssues():
    "for each issue, get the percentage of issues with >=20 days open"
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueDuration.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                duration = row[1:]
                longOpen0 = [i for i in duration if int(i) == 0]
                longOpen2 = [i for i in duration if int(i) >= 20]
                longOpen3 = [i for i in duration if int(i) >= 30]
                bad_smell[groupID] = {'Duration = 0': float(len(longOpen0))/len(duration)}
                bad_smell[groupID].update({'Duration > 20': float(len(longOpen2))/len(duration)})
                bad_smell[groupID].update({'Duration > 30': float(len(longOpen3))/len(duration)})
    return bad_smell

def silentUserNum():
    "for each group, find if some user far lower than 50% of average Comments Per User "
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/userCommentNum.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                user = removeTim_TA(row[1:])
                userCommentNum = [int(num) for num in user[1:]]
                average = float(sum(userCommentNum))/len(userCommentNum)
                threshold = 0.5 * average
                silentUser = 0
                for num in userCommentNum:
                    if num < threshold:
                        silentUser += 1
                bad_smell[groupID] = {'SilentUser Num': float(silentUser)/len(user)}
    return bad_smell


def relaxedUserNum():
    "for each group, find if some user far lower than 50% of average Issues Assigned to each User "
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueAssignees.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                user = removeTim_TA(row[1:])
                userAssignmentNum = [int(num) for num in user]
                average = float(sum(userAssignmentNum))/len(userAssignmentNum)
                threshold = 0.5 * average
                relaxedUser = 0
                for num in userAssignmentNum:
                    if num < threshold:
                        relaxedUser += 1
                bad_smell[groupID] = {'RelaxedUser Num': float(relaxedUser)/len(user)}
    return bad_smell


def issueWoMilestone():
    "for each group, find the percentage of issues without milestone"
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueMilestone.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                milestones = row[1:]
                noMilestone = [m for m in milestones if not m]
                percent = float(len(noMilestone))/len(milestones)
                bad_smell[groupID] = {'Issue wo Milstone': percent}
    return bad_smell


def issueDelayed():
    "for each group, find the percentage of issues that is closed after milestone duedate"
    bad_smell = {}
    inputFile = os.path.join(base, 'featureCSV/issueDelay.csv')
    with open(inputFile, 'r') as csvinput:
        reader = csv.reader(csvinput)
        odd = 1
        for row in reader:
            if odd:
                odd = 0
                continue
            else:
                odd = 1
                groupID = row[0]
                closeTime = row[1:]
                delays = [t for t in closeTime if int(t)>0 ]
                percent = float(len(delays))/len(closeTime)
                bad_smell[groupID] = {'Issue Delayed': percent}
    return bad_smell


def removeTim_TA(users):
    if len(users) <= 4:
        return users
    else:
        users.sort(reverse = True)
    return users[0:4]



def save_badsmell_csv(outputFile, bad_smell, fileds):
     with open(outputFile, 'w') as csvoutput:
        writer = csv.DictWriter(csvoutput, fieldnames=fileds)
        writer.writeheader()
        for groupID, bad_smells in bad_smell.iteritems():
            row = {'groupID': groupID}
            row.update(bad_smells)
            writer.writerow(row)


def merge_dict(bad_smell1, bad_smell2):
    for groupID, score in bad_smell1.iteritems():
        bad_smell1[groupID].update(bad_smell2[groupID])
    return  bad_smell1


def get_badSmell(base, csvpath):
    bad_smell1 = issueDiscussionScore()
    bad_smell2 = issueParticipantScore()
    bad_smell3 = silentUserNum()
    bad_smell4 = relaxedUserNum()
    bad_smell5 = longOpenIssues()
    bad_smell6 = issueWoMilestone()
    bad_smell7 = issueDelayed()

    bad_smell = merge_dict(bad_smell1, bad_smell2)
    bad_smell = merge_dict(bad_smell, bad_smell3)

    outputFile = os.path.join(base, 'badSmellScoreCSV/PoorCommunication.csv')
    fileds = ['groupID', 'Issue Discussions<3', 'Issue Discussions<4', 'Issue Participant<2', 'Issue Participant<3', 'SilentUser Num']
    save_badsmell_csv(outputFile, bad_smell, fileds)



    bad_smell = merge_dict(bad_smell, bad_smell4)
    outputFile = os.path.join(base, 'badSmellScoreCSV/AbsentGroupMember.csv')
    fileds = ['groupID', 'Issue Discussions<3', 'Issue Discussions<4', 'Issue Participant<2', 'Issue Participant<3', 'SilentUser Num', 'RelaxedUser Num']
    save_badsmell_csv(outputFile, bad_smell, fileds)

    bad_smell = merge_dict(bad_smell4, bad_smell5)
    bad_smell = merge_dict(bad_smell, bad_smell6)
    bad_smell = merge_dict(bad_smell, bad_smell7)
    outputFile = os.path.join(base, 'badSmellScoreCSV/PoorPlanning.csv')
    fileds = ['groupID', 'Duration = 0', 'Duration > 20', 'Duration > 30', 'RelaxedUser Num', 'Issue wo Milstone', 'Issue Delayed']
    save_badsmell_csv(outputFile, bad_smell, fileds)
    print 'done'






if __name__ == "__main__":
    base = os.path.abspath(os.path.dirname(__file__))
    csvpath = os.path.join(base, 'dataCollectionInCSV')
    #extract_feature(base, csvpath)
    get_badSmell(base, csvpath)