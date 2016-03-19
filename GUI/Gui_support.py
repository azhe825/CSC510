from __future__ import print_function, division
from func_GUI import *



"format email, str to csr"
def format(email):
    global hashemail
    x=vsm(email)
    x=hashemail(x)
    x=l2normalize(x)
    return x



class Folder(object):
    def __init__(self,thres=0.3):
        self.names=['uncertain','trash']
        self.classifier=[]
        self.thres=thres
        self.num=0

    def addfolder(self,name):
        self.names.append(name)
        self.num=self.num+1
    
    "call this to train the classifier"
    def train(self,training_set):
        labels=[]
        bodies=[]
        for mail in training_set:
            labels.append(mail.label)
            tmp=mail.mat
            if bodies:
                csr_vstack(bodies,tmp)
            else:
                bodies=tmp
        self.classifier=do_SVM(labels,bodies)
    
    "return the list of folder names the email would belong to, also will change mail.folder"
    def predict(self,mail):
        proba=self.classifier.predict_proba(mail.mat)
        mail.folder=[]
        for ind,label in enumerate(self.classifier.classes_):
            mail.proba[label]=proba[ind]
            if proba[ind]>self.thres:
                mail.folder.append(label)
        if not mail.folder:
            mail.folder=['uncertain']
        return mail.folder

"Global variables, need to be initialized"
feature_number=4000
hashemail=hasher(feature_number)
my_folder=Folder()
pool=[]
prog=10
step=10
saturation=100


class Email(object):
    def __init__(self,body=""):
        self.body=body
        if body:
            self.mat=format(body)
        else:
            self.mat=[]
        self.folder=[]
        self.label=''
        self.credit=0
        self.proba={}
        self.read=False
    
    def set_read(self):
        self.read=True

    def set_label(self,label):
        self.label=label

    def set_body(self,body):
        self.body=body
        self.mat=format(body)

    def set_credit(self,credit):
        self.credit=credit

    def set_folder(self,foldername):
        self.folder=[foldername]



"If user read, forward, reply this email. Will not trigger if current_folder is uncertain or trash"
def activity_yes(email,current_folder):
    global pool
    email.set_label(current_folder)
    email.set_credit(1-email.proba[current_folder])
    if email not in pool:
        pool.append(email)

"If user move this email into a target_folder. Will not trigger if target_folder is uncertain or trash."
def activity_no(email,target_folder):
    global pool
    email.set_label(target_folder)
    email.set_credit(1-email.proba[current_folder])
    if email not in pool:
        pool.append(email)

"Runs every mid-night? Retrain the classifier or not"
def check_credit():
    global pool,prog,step,my_folder,saturation
    if len(pool) >= my_folder.num*prog*step:
        can=[]
        for label in my_folder.classifier.classes_:
            collect=[x for x in pool if x.label==label]
            credits=[x.credit for x in collect]
            can.extend(list(np.array(collect)[np.argsort(credits)[-prog*step:]]))
        my_folder.train(can)
        if prog<=saturation:
            prog=prog+1
        else:
            pool=can
        return True
    else:
        return False




