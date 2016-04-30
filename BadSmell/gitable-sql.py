#  gitabel
#  the world's smallest project management tool
#  reports relabelling times in github (time in seconds since epoch)
#  thanks to dr parnin
#  todo:
#    - ensure events sorted by time
#    - add issue id
#    - add person handle

"""
You will need to add your authorization token in the code.
Here is how you do it.

1) In terminal run the following command

curl -i -u <your_username> -d '{"scopes": ["repo", "user"], "note": "OpenSciences"}' https://api.github.com/authorizations

2) Enter ur password on prompt. You will get a JSON response. 
In that response there will be a key called "token" . 
Copy the value for that key and paste it on line marked "token" in the attached source code. 

3) Run the python file. 

     python gitable.py

"""

from __future__ import print_function
import urllib2
import json
import re,datetime
import sys
import sqlite3
import ConfigParser
import os.path
import argparse

from pdb import set_trace

early=1457049600
last=1460073600
timebound=last


def lCompare(item1, item2):
  if item1[0] == item2[0]:
    if item1[1] == item2[1]:
      if item1[2] == item2[2]:
        if item1[3] == item2[3]:
          print('duplicates: '+str(item1))
          return 0
        else:
          return 1 if item1[3] > item2[3] else -1
      else:
        return 1 if item1[2] > item2[2] else -1
    else:
      return int(item1[1] - item2[1])
  else:
    return item1[0] - item2[0]

class L():
  "Anonymous container"
  def __init__(i,**fields) : 
    i.override(fields)
  def override(i,d): i.__dict__.update(d); return i
  def __repr__(i):
    d = i.__dict__
    name = i.__class__.__name__
    return name+'{'+' '.join([':%s %s' % (k,pretty(d[k])) 
                     for k in i.show()])+ '}'
  def show(i):
    lst = [str(k)+" : "+str(v) for k,v in i.__dict__.iteritems() if v != None]
    return ',\t'.join(map(str,lst))

  
def secs(d0):
  d     = datetime.datetime(*map(int, re.split('[^\d]', d0)[:-1]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = d - epoch
  return delta.total_seconds()

def dumpCommit1(u,commits,token, timebound):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for commit in w:
    sha = commit['sha']
    user = commit['author']['login']
    time = secs(commit['commit']['author']['date'])
    message = commit['commit']['message']
    if time>timebound:
      continue
    commitObj = L(sha = sha,
                user = user,
                time = time,
                message = message)
    commits.append(commitObj)
  return True

def dumpComments1(u, comments, token, timebound):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for comment in w:
    user = comment['user']['login']
    identifier = comment['id']
    issueid = int((comment['issue_url'].split('/'))[-1])
    comment_text = comment['body']
    created_at = secs(comment['created_at'])
    updated_at = secs(comment['updated_at'])
    if created_at>timebound:
      continue
    commentObj = L(ident = identifier,
                issue = issueid, 
                user = user,
                text = comment_text,
                created_at = created_at,
                updated_at = updated_at)
    comments.append(commentObj)
  return True


def dumpMilestone1(u, milestones, token, timebound):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w or ('message' in w and w['message'] == "Not Found"): return False
  milestone = w
  identifier = milestone['id']
  milestone_id = milestone['number']
  milestone_title = milestone['title']
  milestone_description = milestone['description']
  created_at = secs(milestone['created_at'])
  due_at_string = milestone['due_on']
  due_at = secs(due_at_string) if due_at_string != None else due_at_string
  closed_at_string = milestone['closed_at']
  closed_at = secs(closed_at_string) if closed_at_string != None else closed_at_string
  user = milestone['creator']['login']

  if due_at==None:
    return True
  if due_at>timebound:
    return True
  if closed_at==None:
    closed_at=timebound+1
  if closed_at>timebound:
    closed_at=timebound+1


  milestoneObj = L(ident=identifier,
               m_id = milestone_id,
               m_title = milestone_title,
               m_description = milestone_description,
               created_at=created_at,
               due_at = due_at,
               closed_at = closed_at,
               user = user)
  milestones.append(milestoneObj)
  return True

def dump1(u,issues, token, timebound):
  request = urllib2.Request(u, headers={"Authorization" : "token "+token})
  v = urllib2.urlopen(request).read()
  w = json.loads(v)
  if not w: return False
  for event in w:
    identifier = event['id']
    issue_id = event['issue']['number']
    issue_name = event['issue']['title']
    created_at = secs(event['created_at'])
    action = event['event']
    label_name = event['label']['name'] if 'label' in event else event['assignee']['login'] if action == 'assigned' else event['milestone']['title'] if action in ['milestoned', 'demilestoned'] else action
    user = event['actor']['login']
    milestone = event['issue']['milestone']
    if milestone != None : milestone = milestone['number']
    if created_at>timebound:
      continue
    eventObj = L(ident=identifier,
                 when=created_at,
                 action = action,
                 what = label_name,
                 user = user,
                 milestone = milestone)
    issue_obj = issues.get(issue_id)
    if not issue_obj: issue_obj = [issue_name, []]
    all_events = issue_obj[1]
    all_events.append(eventObj)
    issues[issue_id] = issue_obj
  return True

def dumpCommit(*arg,**kwarg):
  try:
    return dumpCommit1(*arg,**kwarg)
  except Exception as e:
    print(arg[0])
    print(e)
    print("Contact TA")
    return False

def dumpComments(*arg,**kwarg):
  try:
    return dumpComments1(*arg,**kwarg)
  except Exception as e:
    print(arg[0])
    print(e)
    print("Contact TA")
    return False

def dumpMilestone(*arg,**kwarg):
  try:
    return dumpMilestone1(*arg,**kwarg)
  except urllib2.HTTPError as e:
    if e.code != 404:
      print(e)
      print("404 Contact TA")
    return False
  except Exception as e:
    print(arg[0])
    print(e)
    print("other Contact TA")
    return False

def dump(*arg,**kwarg):
  try:
    return dump1(*arg,**kwarg)
  except Exception as e: 
    print(arg[0])
    print(e)
    print("Contact TA")
    return False

def launchDump(timebound=-1):
  if timebound<0:
    import time
    timebound=time.time()
  if os.path.isfile("./gitable.conf"):
    config = ConfigParser.ConfigParser()
    config.read("./gitable.conf")
  else:
    print("gitable.conf not found, make sure to make one!")
    sys.exit()

  if not config.has_option('options', 'token'):
    print("gitable.conf does not have token, fix!")
    sys.exit()

  parser = argparse.ArgumentParser(description='Process GitHub issue records and record to SQLite database')
  parser.add_argument('repo',help='repo to process')
  parser.add_argument('groupname',help='anonymization to apply to project title')
  parser.add_argument('-db','--database',default='', help='specify db filename, default (repo).db')

  args = parser.parse_args()
  dbFile = '{}.db'.format(args.groupname.replace('\\','_').replace('/','_'))
  if len(args.database)>0:
    dbFile = args.database.format(args.repo.replace('\\','_').replace('/','_'))
    #can't handle bad strings very well, be nice to it D:
  repo = args.repo

  group = args.groupname
  token = config.get('options','token')

  conn = sqlite3.connect(dbFile)

  #SQL stuffs
  conn.execute('''CREATE TABLE IF NOT EXISTS issue(id INTEGER, name VARCHAR(128),
        CONSTRAINT pk_issue PRIMARY KEY (id) ON CONFLICT ABORT)''')
  conn.execute('''CREATE TABLE IF NOT EXISTS milestone(id INTEGER, title VARCHAR(128), description VARCHAR(1024),
        created_at DATETIME, due_at DATETIME, closed_at DATETIME, user VARCHAR(128), identifier INTEGER,
        CONSTRAINT pk_milestone PRIMARY KEY(id) ON CONFLICT ABORT)''')

  #unsure if ignoring duplicate event tuples is a good idea, but the unique information is pretty much all we care about
  #duplicates aren't meaningful, so I guess it 's ok
  conn.execute('''CREATE TABLE IF NOT EXISTS event(issueID INTEGER NOT NULL, time DATETIME NOT NULL, action VARCHAR(128),
        label VARCHAR(128), user VARCHAR(128), milestone INTEGER, identifier INTEGER,
        CONSTRAINT pk_event PRIMARY KEY (issueID, time, action, label) ON CONFLICT IGNORE,
        CONSTRAINT fk_event_issue FOREIGN KEY (issueID) REFERENCES issue(id) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT fk_event_milestone FOREIGN KEY (milestone) REFERENCES milestone(id) ON UPDATE CASCADE ON DELETE CASCADE)''')
  conn.execute('''CREATE TABLE IF NOT EXISTS comment(issueID INTEGER NOT NULL, user VARCHAR(128), createtime DATETIME NOT NULL,
        updatetime DATETIME, text VARCHAR(1024), identifier INTEGER,
        CONSTRAINT pk_comment PRIMARY KEY (issueID, user, createtime) ON CONFLICT IGNORE,
        CONSTRAINT fk_comment_issue FOREIGN KEY (issueID) REFERENCES issue(id) ON UPDATE CASCADE ON DELETE CASCADE)''')
  conn.execute('''CREATE TABLE IF NOT EXISTS commits(id INTEGER NOT NULL, time DATETIME NOT NULL, sha VARCHAR(128),
        user VARCHAR(128), message VARCHAR(128),
        CONSTRAINT pk_commits PRIMARY KEY (id) ON CONFLICT ABORT)''')        
  nameNum = 1
  nameMap = dict()

  milestoneNum = 1
  milestoneMap = dict()

  page = 1
  milestones = []
  print('getting records from '+repo)
  Flag=True
  while(True):
    url = 'https://api.github.com/repos/'+repo+'/milestones/' + str(page)
    doNext = dumpMilestone(url, milestones, token, timebound)
    print("milestone "+ str(page))
    page += 1
    if not doNext :
      if not Flag:
        break
      else:
        Flag=False
    else:
      Flag=True
  page = 1
  issues = dict()
  Flag=True
  while(True):
    url = 'https://api.github.com/repos/'+repo+'/issues/events?page=' + str(page)
    doNext = dump(url, issues, token, timebound)
    print("issue page "+ str(page))
    page += 1
    if not doNext :
      if not Flag:
        break
      else:
        Flag=False
    else:
      Flag=True
  page = 1
  comments = []
  Flag=True
  while(True):
    url = 'https://api.github.com/repos/'+repo+'/issues/comments?page='+str(page)
    doNext = dumpComments(url, comments, token, timebound)
    print("comments page "+ str(page))
    page += 1
    if not doNext :
      if not Flag:
        break
      else:
        Flag=False
    else:
      Flag=True
  page = 1
  commits = []
  Flag=True
  while(True):
    url = 'https://api.github.com/repos/'+repo+'/commits?page=' + str(page)
    doNext = dumpCommit(url, commits, token, timebound)
    print("commit page "+ str(page))
    page += 1
    if not doNext :
      if not Flag:
        break
      else:
        Flag=False
    else:
      Flag=True
  issueTuples = []
  eventTuples = []
  milestoneTuples = []
  commentTuples = []
  commitTuples = []


  for milestone in milestones:
    if not milestone.user in nameMap:
      nameMap[milestone.user] = group+'/user'+str(nameNum)
      nameNum+=1
    milestoneMap[milestone.m_title] = milestone.m_id
    milestoneTuples.append([milestone.m_id, milestone.m_title, milestone.m_description, milestone.created_at, milestone.due_at, milestone.closed_at, nameMap[milestone.user], milestone.ident])


  for issue, issueObj in issues.iteritems():
    events = issueObj[1]
    issueTuples.append([issue, issueObj[0]]);
    #print("ISSUE " + str(issue) + ", " + issueObj[0])
    for event in events:
      #print(event.show())
      if not event.user in nameMap:
        nameMap[event.user] = group+'/user'+str(nameNum)
        nameNum+=1
      if event.action == 'assigned' and not event.what in nameMap:
        nameMap[event.what] = group+'/user'+str(nameNum)
        nameNum+=1
      eventTuples.append([issue, event.when, event.action, nameMap[event.what] if event.action == 'assigned' else event.what, nameMap[event.user], event.milestone if 'milestone' in event.__dict__ else None, event.ident])
    #print('')

  for comment in comments:
    if not comment.user in nameMap:
      nameMap[comment.user] = group+'/user'+str(nameNum)
      nameNum+=1
    commentTuples.append([comment.issue, nameMap[comment.user], comment.created_at, comment.updated_at, comment.text, comment.ident])

  for commit in commits:
    if not commit.user in nameMap:
      nameMap[commit.user] = group+'/user'+str(nameNum)
      nameNum+=1
    commitTuples.append([commit.time, commit.sha, nameMap[commit.user], commit.message])



  try:
    if len(issueTuples) > 0:
      conn.executemany('INSERT INTO issue VALUES (?,?)', issueTuples)
      conn.commit()
      print('committed issues')
    if len(milestoneTuples) > 0:
      conn.executemany('INSERT INTO milestone VALUES (?, ?, ?, ?, ?, ?, ?, ?)', milestoneTuples)
      conn.commit()
      print('committed milestones')
    if len(eventTuples) > 0:
      conn.executemany('INSERT INTO event VALUES (?, ?, ?, ?, ?, ?, ?)', eventTuples)
      conn.commit()
      print('committed events')
    if len(commentTuples) > 0:
      conn.executemany('INSERT INTO comment VALUES (?, ?, ?, ?, ?, ?)', commentTuples)
      conn.commit()
      print('committed comments')
    if len(commitTuples) > 0:
      conn.executemany('INSERT INTO commits (time, sha, user, message) VALUES (?,?,?,?)', commitTuples)
      conn.commit()
      print('committed commits')
  except sqlite3.Error as er:
    print(er)

  conn.close()
  print('done!')
    
launchDump(timebound)

