from __future__ import print_function, division

__author__ = 'amrit'

from Tkinter import *
import os
from func_GUI import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Mails_directory="/../Mails/struct.txt"

list_mails=[]
list_labels_mails=[]
def readfile(filename):
    corpus=[]
    labels=[]
    with open(filename,'r') as f:
        for doc in f.readlines():
            try:
                x=Email(doc.split(" >>> ")[1])
                x.set_label(doc.split(" >>> ")[0].split()[1])
                corpus.append(x)
                labels.append(doc.split(" >>> ")[0].split())
            except:
                pass

    global list_mails
    list_mails = corpus
    global list_labels_mails
    list_labels_mails = labels


class Application(Frame):

    def inbox_command(self):
        self.unread.delete(first=0, last=self.unread.size())
        self.read.delete(first=0, last=self.read.size())
        for i in range(len(list_mails)):
            if "inbox" in list_labels_mails[i]:
                if "unread" in list_labels_mails[i]:
                    self.unread.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))
                if "read" in list_labels_mails[i]:
                    self.read.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))

    def spam_command(self):
        self.unread.delete(first=0, last=self.unread.size())
        self.read.delete(first=0, last=self.read.size())
        for i in range(len(list_mails)):
            if "spam" in list_labels_mails[i]:
                if "unread" in list_labels_mails[i]:
                    self.unread.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))
                if "read" in list_labels_mails[i]:
                    self.read.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))

    def trash_command(self):
        self.unread.delete(first=0, last=self.unread.size())
        self.read.delete(first=0, last=self.read.size())
        for i in range(len(list_mails)):
            if "trash" in list_labels_mails[i]:
                if "unread" in list_labels_mails[i]:
                    self.unread.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))
                if "read" in list_labels_mails[i]:
                    self.read.insert('end', "%0.4d : %s" % (i, list_mails[i].get_body()))

    def del_un(self):
        x= int(self.unread.get(ANCHOR).split(' : ')[0])
        self.unread.delete(ANCHOR)
        for i,k in enumerate(list_labels_mails[x]):
            if k == "trash":
                list_labels_mails[x][i] = ""
            if k == "inbox":
                list_labels_mails[x][i] = "trash"
            if k == "spam":
                list_labels_mails[x][i] = "trash"

    def del_re(self):
        x= int(self.read.get(ANCHOR).split(' : ')[0])
        self.read.delete(ANCHOR)
        for i,k in enumerate(list_labels_mails[x]):
            if k == "trash":
                list_labels_mails[x][i] = ""
            if k == "inbox":
                list_labels_mails[x][i] = "trash"
            if k == "spam":
                list_labels_mails[x][i] = "trash"

    def read_user(self, event):
        w = event.widget
        self.popup1(w.get(w.curselection()).split(' : ')[1])

    def unread_user(self,event):
        w = event.widget
        self.popup1(w.get(w.curselection()).split(' : ')[1])
        x = int(w.get(w.curselection()).split(' : ')[0])
        for i,k in enumerate(list_labels_mails[x]):
            if k == "unread":
                list_labels_mails[x][i] = "read"
        if "inbox" in list_labels_mails[x]:
            self.inbox_command()
        if "spam" in list_labels_mails[x]:
            self.spam_command()
        if "trash" in list_labels_mails[x]:
            self.trash_command()

    def mov_command(self):
        print("Move")

    def c_labels_command(self):
        self.popup()
        if (self.entryValue()!=''):
            self.buttons.append(self.entryValue())
            x1=Button(self.m, text = self.buttons[self.count], fg   = "red", command =  self.spam_command, state=ACTIVE)
            self.count+=1
            self.m.add(x1)

    def createWidgets(self):
        self.m = PanedWindow(self, orient=VERTICAL)
        self.m.pack(side=LEFT, expand=1)
        self.INBOX = Button(self.m, text = "INBOX", fg   = "red", command =  self.inbox_command, state=ACTIVE)
        self.SPAM = Button(self.m, text = "SPAM", fg   = "red", command =  self.spam_command, state=ACTIVE)
        self.TRASH = Button(self.m, text = "TRASH", fg   = "red", command =  self.trash_command, state=ACTIVE)
        self.m.add(self.INBOX)
        self.m.add(self.SPAM)
        self.m.add(self.TRASH)
        #self.USER.pack(side=BOTTOM, anchor=W, fill=X)
        self.m2 = PanedWindow(self, orient=VERTICAL)
        self.m2.pack(fill=BOTH, side= LEFT, expand=1)
        #self.m.add(self.m2)

        self.top_right = Label(self.m2, text="Unread")
        self.m2.add(self.top_right)

        self.unread = Listbox(self.m2, width=120, height=20)
        self.unread.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.unread.yview, orient='vertical')
        #self.s.grid(column=0, row=0, sticky="ns")
        self.unread.config(yscrollcommand = self.s.set)
        self.unread.insert('end', "Unread Mails")
        self.unread.bind("<Double-Button-1>", self.unread_user)
        self.unread.pack()
        self.m2.add(self.unread)

        self.bottom_right = Label(self.m2, text="Read")
        self.m2.add(self.bottom_right)
        self.read = Listbox(self.m2, width=120, height=20)
        self.read.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.read.yview, orient='vertical')
        #self.s.grid(column=0, row=0, sticky="ns")
        self.read.config(yscrollcommand = self.s.set)
        self.read.insert('end', "Read Mails")
        self.read.bind("<Double-Button-1>", self.read_user)

        self.read.pack()
        self.m2.add(self.read)

        self.m3 = PanedWindow(self, orient=VERTICAL)
        self.m3.pack(side=RIGHT, expand=1)
        self.delete_un = Button(self, text="DELETE UNREAD", command=self.del_un)
        self.delete_re = Button(self, text="DELETE READ", command=self.del_re)
        self.mov = Button(self, text="MOVE", command=self.mov_command)
        self.CREATE_Labels = Button(self, text = "CREATE_LABELS", fg   = "red", command =  self.c_labels_command, state=ACTIVE)
        self.m3.add(self.delete_un)
        self.m3.add(self.delete_re)
        self.m3.add(self.mov)
        self.m3.add(self.CREATE_Labels)

    def popup(self):
        self.w=popupWindow(self.Frame)
        self.Frame.wait_window(self.w.top)

    def popup1(self,data):
        self.w=popupWindow1(self.Frame,data)
        self.Frame.wait_window(self.w.top)

    def entryValue(self):
        return self.w.value

    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.Frame =master
        self.count=0
        self.buttons=[]
        self.pack()
        self.createWidgets()
        #print(Application.__getitem__(self, Button)

class popupWindow1(object):
    def __init__(self,master,data):
        self.data=data
        top=self.top=Toplevel(master)
        self.l=Label(top,text=self.data)
        self.l.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.top.destroy()

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Label Creation")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

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

    def get_body(self):
        return self.body

    def get_probab(self):
        return self.proba

    def get_label(self):
        return self.label

    def get_credit(self):
        return self.credit



"If user read, forward, reply this email. Will not trigger if current_folder is uncertain or trash"
def activity_yes(email,current_folder):
    global pool
    email.set_label(current_folder)
    email.set_credit(1-email.proba[current_folder])
    if email not in pool:
        pool.append(email)

"If user move this email into a target_folder. Will not trigger if target_folder is uncertain or trash."
'''def activity_no(email,target_folder):
    global pool
    email.set_label(target_folder)
    email.set_credit(1-email.proba[current_folder])
    if email not in pool:
        pool.append(email)'''

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

if __name__ == '__main__':
    text='abc hfsb hasb bsh'
    email= Email(text)
    readfile(BASE_DIR+Mails_directory)
    global list_labels_mails
    global list_mails
    list_mails.append(email)
    list_labels_mails.append(['unread', 'inbox'])
    global pool
    pool=list_mails
    root = Tk()
    root.title("Mailbox")
    root.minsize(width=1000,height=600 )
    app = Application(master=root)
    app.mainloop()
    root.destroy()