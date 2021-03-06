#!/usr/bin/python

# by Shijie Li to parse email content and filter out subject and body parts.

import os
import sys
import os.path as sp
import re
import email
from email.parser import Parser

class_attr_separator = " ::::::>>>>>> "
subject_body_separator = " ****** "
ThresBodyLength = 10
ThresSubjectLength = 10

#these two folder contains all the emails received and sent. No useful for our email labling jobs.
CategoryRemoveList = ['all_documents', '_sent_mail' 'inbox', 'outbox', 'sent_items', 'sent']

# Given path of the root folder of email data set
if len(sys.argv) != 2:
    print("Usage: emailParser.py <path to root directory of email data set.>")
    sys.exit(1)
rootdir = sys.argv[1]

# extract all user folders
userdir = [fn for fn in os.listdir(rootdir) if not sp.isfile(fn)]
print "Users: %s" % ' '.join(userdir)
rootdir = os.getcwd() # save root path

# total data set
#dataset = [] # all the data set
ft = open("dataset.txt", 'w')
# extract user data
userdata = []
for classdir, subdirs, files in os.walk(rootdir):
    print classdir
    for fm in files: 
        #fpath = sp.abspath(fm)
        class_tag = classdir.split(rootdir)[1]
        #print class_tag
        header = class_tag.split('/')
        if(len(header) == 3):
            userID = header[1]
            category = ''.join(header[2:])
        elif(len(header) > 3):
            userID = header[1]
            category = '/'.join(header[2:])
        else:
            userID = ''
            category = ''
        if category in CategoryRemoveList:
            print "Ignored above folder..."
            break
        try:
            #print 'open', classdir+'/'+fm
            fmail = open(classdir+'/'+fm, 'r')
            mailText = ''.join(fmail.readlines())
            #print mailText
            content = email.message_from_string(mailText)
            subject = content['subject']
            #print subject
            if subject is None: # discard mail without subject
                fmail.close()
                continue
            body = []
            #print 'half'
            if content.is_multipart():
                for payload in content.get_payload():
                    body.append(payload.get_payload())
            else:
                body.append(content.get_payload())
            if body is None: # discard mail without body
                fmail.close()
                continue
            #print 'done'
            body_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '', ''.join(body))
            body_keywords = re.sub('\s+', ' ', body_segments)
            if len(body_keywords) < ThresBodyLength:
                fmail.close()
                continue
            subject_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '', ''.join(subject))
            subject_keywords = re.sub('\s+', ' ', subject_segments)
            if len(subject_keywords) < ThresSubjectLength:
                fmail.close()
                continue
            user_mail_entry = class_tag + class_attr_separator + subject_keywords + subject_body_separator +  body_keywords
            userdata.append(user_mail_entry)
            #print user_mail_entry
            fmail.close()
        except:
            continue
ft.write('\n'.join(userdata))
ft.close()