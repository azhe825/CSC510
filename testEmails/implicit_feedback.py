from __future__ import print_function, division
from func_GUI import *
import pickle
from demos import cmd


def initial():
    feature_number=4000

    hashemail=hasher(feature_number)

"format email, str to csr"
def format(email):
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

    def predict(self,mail):
        proba=self.classifier.predict_proba(mail.mat)
        mail.folder=[]
        for ind,label in enumerate(self.classifier._classes):
            mail.proba[label]=proba[ind]
            if proba[ind]>self.thres:
                mail.folder.append(label)
        if not mail.folder:
            mail.folder=['uncertain']
        return mail.folder




my_folder=Folder()
pool=[]
iteration=10
step=10


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

    def set_label(self,label):
        self.label=label

    def set_body(self,body):
        self.body=body
        self.mat=format(body)

    def set_credit(self,credit):
        self.credit=credit



"If user read, forward, reply this email. Will not trigger if current_folder is uncertain or trash"
def activity_yes(email,current_folder):
    email.set_label(current_folder)
    email.set_credit(1-email.proba[current_folder])
    if email not in pool:
        pool.append(email)

"If user move this email into a target_folder. Will not trigger if target_folder is uncertain or trash."
def activity_no(email,target_folder):
    email.set_label(target_folder)
    email.set_credit(1)
    if email not in pool:
        pool.append(email)

"Runs every mid-night? Retrain the classifier"
def check_credit():
    if len(pool) >= my_folder.num*iteration*step:
        can=[]
        for label in my_folder.classifier._classes:
            collect=[x for x in pool if x.label==label]
            credits=[x.credit for x in collect]
            can.extend(list(np.array(collect)[np.argsort(credits)[-iteration*step:]]))
        my_folder.train(can)
        iteration=iteration+1
        return True




def incremental_credit(label,matrix,Classify,is_LDA=False):
    step_count=1
    step=1
    total=10
    dict={}
    for key in set(label):
        dict[key]={}
    dict['F_M']={}
    XX=map(str,range(100,100+total*10,step*10))

    preserve,val,train,test=pre_inc(label)

    if is_LDA:
        topic_model=LDA(matrix,preserve)
    else:
        topic_model=matrix

    clf=Classify(label[train],topic_model[train])
    prediction=clf.predict(topic_model[preserve])
    dict_tmp=evaluate(label[preserve],prediction)
    for key in dict:
        dict[key][XX[0]]=dict_tmp[key]

    shuffle(test)
    collect={}
    pool=[]
    for ind in test:
        pool.append(ind)
        if clf.predict(topic_model[ind])==label[ind]:
            score=1-clf.predict_proba(topic_model[ind])[0,list(clf.classes_).index(label[ind])]
        else:
            score=1.0
        try:
            collect[label[ind]][ind]=score
        except:
            collect[label[ind]]={ind:score}

        if len(pool)==step_count*100:
            num=int(len(pool)/len(set(label)))
            add=[]
            for ll in collect:
                add.extend(list(np.array(collect[ll].keys())[np.argsort(collect[ll].values())][-num:]))

            # test_new=list(set(test)-set(pool))
            clf=Classify(label[train+add],topic_model[train+add])
            prediction=clf.predict(topic_model[preserve])
            dict_tmp=evaluate(label[preserve],prediction)
            for key in dict_tmp:
                dict[key][str(100+step_count*10)]=dict_tmp[key]
            step_count=step_count+step
            if step_count==total:
                break
    return dict






if __name__ == '__main__':
    eval(cmd())
