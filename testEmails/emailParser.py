#!/usr/bin/python

# by Shijie Li to parse email content and filter out subject and body parts.

import os
import sys
import os.path as sp
import re
import email
from email.parser import Parser

class_attr_separator = " ::::::>>>>>> "


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
dataset = [] # all the data set
ft = open("dataset.txt", 'w')
#for rootx, subx, filex in os.walk(rootdir):
    #for fx in filex: 
        #fpath = sp.abspath(fx)
        #print rootx.split(rootdir)[1]
        #print fpath
        #print fpath.split(rootdir)[1]

# extract user data
for ud in userdir: # iterate over all users
    try:
        userdata = [] # to save user data set
        os.chdir(ud) # enter user dir
        print os.getcwd()
        for udir, subdirs, files in os.walk(os.getcwd()):
            print udir
            for fm in files:
                #print 'yes', os.getcwd()
                fmail = open(fm, 'r')
                mailText = ''.join(fmail.readlines())
                content = email.message_from_string(mailText)
                subject = content['subject']
                if subject is None: # discard mail without subject
                    continue
                body = []
                if content.is_multipart():
                    for payload in content.get_payload():
                        body.append(payload.get_payload())
                else:
                    body.append(content.get_payload())
                fmail.close()
                if body is None: # discard mail without body
                    continue
                class_tag = udir
                body_keyword = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '', ''.join(body))
                user_mail_entry = class_tag + class_attr_separator + subject + body_keyword
                userdata.append(user_mail_entry)
        #os.chdir(ud) # enter user dir
        fp = open("data.txt", 'w')
        fp.write('\n'.join(userdata))
        fp.close()
        dataset.extend(userdata) # merge into total dataset
        os.chdir('../') # change back to the root dir
    except:
        continue # skip unaccessible user dir

ft.write('\n'.join(dataset))
ft.close()
