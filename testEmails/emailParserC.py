#!/usr/bin/python

# by Shijie Li to parse email content and filter out subject and body parts. Modified by Zhe to clean the data.

import os
import sys
import os.path as sp
import re
import email
from pdb import set_trace
from email.parser import Parser

class_attr_separator = " ::::::>>>>>> "


# Set directory
Dir='/Users/zhe/PycharmProjects/Email_Data'
category=""


# extract user data
for classdir, users, files in os.walk(Dir):
    break

for user in users:
    userdata = []
    for classdir, subdirs, files in os.walk(Dir+'/'+user):
        if len(files)<4:
            continue
        for fm in files:

            #fpath = sp.abspath(fm)
            category = classdir.split(Dir+'/'+user+'/')[1]

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

                #print 'done'
                body_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '', ''.join(body))
                body_keywords = re.sub('\s+', ' ', body_segments)

                subject_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '', ''.join(subject))
                subject_keywords = re.sub('\s+', ' ', subject_segments)

                user_mail_entry = category + class_attr_separator + subject_keywords.lower() + ' ' +  body_keywords.lower()
                userdata.append(user_mail_entry)
                #print user_mail_entry
                fmail.close()
            except:
                continue
    with open('../Cleaned_Data/'+user+'.txt', 'w') as ft:
        ft.write('\n'.join(userdata))