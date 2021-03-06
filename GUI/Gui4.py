from __future__ import print_function, division

__author__ = 'Amrit, Zhe, Jerry, Jack'

from Tkinter import *
import os
from func_GUI import *
import re
import random
from email import message_from_string


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Mails_directory = "../Mails/initial2.txt"

"convert the original email to string list"


def email_parser(mailText):
    content = message_from_string(mailText)  # extract email content totally
    subject = content['subject']  # parse for email subject
    body = []
    if content.is_multipart():  # parse for email body
        for payload in content.get_payload():
            body.append(payload.get_payload())
    else:
        body.append(content.get_payload())
    body_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '',
                           ''.join(body))  # filter characters for email body
    body_keywords = re.sub('\s+', ' ', body_segments)
    subject_segments = re.sub(r"\n|(\\(.*?){)|}|[!$%^&*#()_+|~\-={}\[\]:\";'<>?,.\/\\]|[0-9]|[@]", '',
                              ''.join(subject))  # filter characters for email subject
    subject_keywords = re.sub('\s+', ' ', subject_segments)
    mail_subject = subject_keywords.lower()
    mail_body = body_keywords.lower()
    return subject, body, mail_subject, mail_body  # return original subject, body, and processed subject and body


"read the initial setup from initial.txt"


def readfile(filename):
    global my_folder, pool, list_mails
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                mailText=''
                with open("../"+doc.strip(), 'r') as fd:
                    for docc in fd.readlines():
                        mailText+=docc
                subject, body, mail_subject, mail_body = email_parser(mailText)
                true_label = get_true_label(mailText).lower()
                mail_body = mail_subject + " "+mail_body
                newmail = Email(mail_body)
                newmail.set_read()
                newmail.raw_email = body[0]
                newmail.subject=subject
                newmail.trueLabel = true_label
                newmail.set_folder(true_label)
                newmail.set_label(true_label)
                newmail.credit=1
                if not newmail.label in my_folder.names:
                    my_folder.addfolder(newmail.label)
                pool.append(newmail)
            except:
                pass
    my_folder.train(pool)
    list_mails = pool


def readnew():
    with open("../Mails/newmails.txt", 'r') as f:
        for doc in f.readlines():
            new_mails.append(doc.strip())


def get_true_label(raw_email):
    for line in raw_email.split('\r\n'):
        if line.startswith('X-Folder:'):
            folder = line.split('X-Folder:')[1]
            true_lable = folder.split('\\')[-1]
            print ('folder: ' + true_lable)
            return true_lable


"when new email comes in"
def new_email(mailText):
    global list_mails, my_folder
    subject, body, mail_subject, mail_body = email_parser(mailText)
    true_label = get_true_label(mailText).lower()
    mail_body = mail_subject + " "+mail_body
    newmail = Email(mail_body)
    newmail.raw_email = body[0]
    newmail.trueLabel = true_label
    newmail.subject=subject
    list_mails.append(newmail)
    my_folder.predict(newmail)


class Application(Frame):

    def refresh(self):
        global list_mails, currentfolder, my_folder
        self.unread.delete(first=0, last=self.unread.size())
        self.read.delete(first=0, last=self.read.size())
        folder_unreadNum = {foldername: 0 for foldername in my_folder.names}
        for i, mail in enumerate(list_mails):
            # Count the unread emails for each folder.
            for f in mail.folder:
                if f not in folder_unreadNum:
                    folder_unreadNum[f] = 0
                if not mail.read:
                    folder_unreadNum[f] += 1
            ## update Read and Unread Box Widget
            if currentfolder in mail.folder:
                if mail.read:
                    self.read.insert('end', "%0.4d : %s" % (i, mail.subject))
                else:
                    self.unread.insert('end', "%0.4d : %s" % (i, mail.subject))
        for folder, button in self.folderName_button.iteritems():
            # if folder in ['uncertain', 'trash']:
            #     continue
            unreadNum = folder_unreadNum[folder]
            if unreadNum == 0:
                button.config(text=folder)
                button.config(bg='White')
            else:
                button.config(text=folder + ' (' + str(unreadNum) + ')' )

    def button_command(self, a):
        global currentfolder
        currentfolder = a
        self.refresh()

    # def del_un(self):
    #     x= int(self.unread.get(ANCHOR).split(' : ')[0])
    #     self.unread.delete(ANCHOR)
    #     for i,k in enumerate(list_labels_mails[x]):
    #         if k == "trash":
    #             list_labels_mails[x][i] = ""
    #         if k == "inbox":
    #             list_labels_mails[x][i] = "trash"
    #         if k == "uncertain":
    #             list_labels_mails[x][i] = "trash"
    #
    # def del_re(self):
    #     x= int(self.read.get(ANCHOR).split(' : ')[0])
    #     self.read.delete(ANCHOR)
    #     for i,k in enumerate(list_labels_mails[x]):
    #         if k == "trash":
    #             list_labels_mails[x][i] = ""
    #         if k == "inbox":
    #             list_labels_mails[x][i] = "trash"
    #         if k == "uncertain":
    #             list_labels_mails[x][i] = "trash"

    def read_user(self, event):
        global list_mails, currentfolder
        w = event.widget
        email_id = w.get(w.curselection()).split(' : ')[0]
        email = list_mails[int(email_id)]
        true_label = email.get_trueLabel()
        if email.get_raw() == '':
            pop_message = email.get_body()
        else:
            pop_message = '*** '+ true_label + ' *** \n' + email.get_raw()[:500]
        self.popup1(pop_message)
        if not (currentfolder == 'uncertain' or currentfolder == 'trash'):
            activity_yes(list_mails[int(w.get(w.curselection()).split(' : ')[0])], currentfolder)
        self.refresh()

    def showscore(self):
        global my_folder
        message1="Precision: %f" %my_folder.P
        message2="Recall: %f" %my_folder.R
        message3="F1: %f" %my_folder.F1
        print("Precision: %f" %my_folder.P)
        print("Recall: %f" %my_folder.R)
        print("F1: %f" %my_folder.F1)
        self.popup1(message1+'\n'+message2+'\n'+message3)

    def incoming(self):
        try:
            x=random.randint(0,len(new_mails)-1)
            l=''
            with open("../"+new_mails.pop(x), 'r') as f:
                for doc in f.readlines():
                    l+=doc
            new_email(l)

            self.refresh()
        except:
            self.showscore()




    def unread_user(self, event):
        # w = event.widget
        # self.popup1(w.get(w.curselection()).split(' : ')[1])
        # global list_mails, currentfolder
        global list_mails, currentfolder
        w = event.widget
        email_id = w.get(w.curselection()).split(' : ')[0]
        email = list_mails[int(email_id)]
        true_label = email.get_trueLabel()
        if email.get_raw() == '':
            pop_message = email.get_body()
        else:
            pop_message = '*** '+ true_label + ' *** \n' + email.get_raw()[:500]
        self.popup1(pop_message)

        list_mails[int(w.get(w.curselection()).split(' : ')[0])].set_read()
        if not (currentfolder == 'uncertain' or currentfolder == 'trash'):
            activity_yes(list_mails[int(w.get(w.curselection()).split(' : ')[0])], currentfolder)
        self.refresh()

    def mov_command(self, targetfolder):
        global list_mails, currentfolder
        list_mails[int(self.waste)].folder = [targetfolder]
        if not (targetfolder == 'uncertain' or targetfolder == 'trash'):
            activity_no(list_mails[int(self.waste)], targetfolder)
        self.refresh()

    def c_labels_command(self):
        self.popup()
        if (self.entryValue() != ''):
            a = self.entryValue()
            global my_folder
            my_folder.addfolder(a)
            self.create_folder(a)

    def create_folder(self, name):
        self.buttons.append(name)
        x1 = Button(self.m, text=name, fg="red", command=lambda name=name: self.button_command(name), state=ACTIVE)
        self.m.add(x1)
        self.folderName_button[name] = x1
        self.count += 1


    def change_checkbox(self, bv, id):
        now = bv.get()
        self.checkbox[id] = now
        # print (now)
        features[id] = now
        print(features)

    def create_checkbox(self, id, default=True):
        bv = BooleanVar()
        bv.set(default)
        bv.trace("w", lambda name, index, mode, bv=bv: self.change_checkbox(bv, id))
        self.checkbox[id] = bv
        c = Checkbutton(self.m3, text=feature_names[id], variable=bv)
        self.m3.add(c)

    def createWidgets(self):
        self.m = PanedWindow(self, orient=VERTICAL)
        self.m.pack(side=LEFT, expand=1)
        for name in my_folder.names:
            self.create_folder(name)
        # self.USER.pack(side=BOTTOM, anchor=W, fill=X)
        self.m2 = PanedWindow(self, orient=VERTICAL)
        self.m2.pack(fill=BOTH, side=LEFT, expand=1)
        # self.m.add(self.m2)
        # New incoming mail


        self.top_right = Label(self.m2, text="Unread")
        self.m2.add(self.top_right)

        self.unread = Listbox(self.m2, width=120, height=20)
        self.unread.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.unread.yview, orient='vertical')
        # self.s.grid(column=0, row=0, sticky="ns")
        self.unread.config(yscrollcommand=self.s.set)
        self.unread.insert('end', "Unread Mails")
        self.unread.bind("<Double-Button-1>", self.unread_user)
        self.unread.bind("<Button-2>", self.popup_menu)
        self.unread.pack()
        self.m2.add(self.unread)

        self.bottom_right = Label(self.m2, text="Read")
        self.m2.add(self.bottom_right)
        self.read = Listbox(self.m2, width=120, height=20)
        self.read.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.read.yview, orient='vertical')
        # self.s.grid(column=0, row=0, sticky="ns")
        self.read.config(yscrollcommand=self.s.set)
        self.read.insert('end', "Read Mails")
        self.read.bind("<Double-Button-1>", self.read_user)
        self.read.bind("<Button-2>", self.popup_menu)

        self.read.pack()
        self.m2.add(self.read)

        self.m3 = PanedWindow(self, orient=VERTICAL)
        self.m3.pack(side=RIGHT, expand=1)
        # self.delete_un = Button(self, text="DELETE UNREAD", command=self.del_un)
        # self.delete_re = Button(self, text="DELETE READ", command=self.del_re)
        self.CREATE_Labels = Button(self, text="CREATE_LABELS", fg="red", command=self.c_labels_command, state=ACTIVE)
        self.newm = Button(self, text="New Mail", fg="red", command=self.incoming, state=ACTIVE)
        self.show = Button(self, text="Show Score", fg="red", command=self.showscore, state=ACTIVE)
        self.m3.add(self.newm)
        self.m3.add(self.CREATE_Labels)
        self.m3.add(self.show)

        for feature_id in range(len(features)):
            self.create_checkbox(feature_id)

        self.button_command('uncertain')

    def popup_menu(self, event):
        w = event.widget
        self.aMenu = Menu(self, tearoff=0)
        # print(labels_gui)
        for i in my_folder.names:
            if i != 'uncertain' and i != 'trash':
                self.aMenu.add_command(label=i, command=lambda i=i: self.mov_command(i.lower()))
        self.waste = w.get(w.curselection()).split(' : ')[0]
        self.aMenu.post(event.x_root, event.y_root)

    def popup(self):
        self.w = popupWindow(self.Frame)
        self.Frame.wait_window(self.w.top)

    def popup1(self, data):
        self.w = popupWindow1(self.Frame, data)
        self.Frame.wait_window(self.w.top)

    def entryValue(self):
        return self.w.value

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.Frame = master
        self.count = 0
        self.buttons = []
        self.folderName_button = {}
        self.checkbox = {}
        self.pack()
        self.waste = ''
        self.createWidgets()
        # print(Application.__getitem__(self, Button)


class popupWindow1(object):
    def __init__(self, master, data):
        self.data = data
        top = self.top = Toplevel(master)
        self.l = Label(top, text=self.data)
        self.l.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.top.destroy()


class popupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.l = Label(top, text="Label Creation")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


"format email, str to csr"


def format(email):
    global hashemail
    x = vsm([email])
    x = hashemail(x)
    x = l2normalize(x)
    return x


class Folder(object):
    def __init__(self, thres=0.35):
        self.names = ['uncertain', 'trash']
        self.classifier = []
        self.thres = thres
        self.num = 0
        self.T={}
        self.F={}
        self.P=0
        self.R=0
        self.F1=0
        self.FR={}

    def addfolder(self, name):
        self.names.append(name)
        self.num = self.num + 1
        self.T[name]=0
        self.F[name]=0
        self.FR[name]=0

    def update(self):
        folders=self.names[2:]
        self.P=0
        self.R=0
        self.F1=0
        if folders:
            for fold in folders:
                if self.T[fold]==0:
                    self.P=self.P+0
                    self.R=self.R+0
                else:
                    self.P=self.P+self.T[fold]/(self.T[fold]+self.F[fold])
                    self.R=self.R+self.T[fold]/(self.T[fold]+self.FR[fold])
            self.P=self.P/len(folders)
            self.R=self.R/len(folders)
            if self.P and self.R:
                self.F1=self.P*self.R*2/(self.P+self.R)
            else:
                self.F1=0



    "call this to train the classifier"

    def train(self, training_set):
        labels = []
        bodies = []
        for mail in training_set:
            labels.append(mail.label)
            tmp = mail.mat
            if not bodies == []:
                bodies = csr_vstack(bodies, tmp)
            else:
                bodies = tmp
        self.classifier = do_SVM(labels, bodies)

    "return the list of folder names the email would belong to, also will change mail.folder"

    def predict(self, mail):
        global features
        proba = self.classifier.predict_proba(mail.mat)[0]
        mail.folder = []
        for ind, label in enumerate(self.classifier.classes_):
            mail.proba[label] = proba[ind]
            if proba[ind] > self.thres:
                mail.folder.append(label)
        if not mail.folder:
            mail.folder = ['uncertain']
        if not features[2]:
            if len(mail.folder) > 1:
                mail.folder = [self.classifier.classes_[np.argmax(proba)]]

        for fold in mail.folder:
            if fold == mail.trueLabel:
                try:
                    self.T[fold]=self.T[fold]+1
                except:
                    self.T[fold]=1
            else:
                try:
                    self.F[fold]=self.F[fold]+1
                except:
                    self.F[fold]=1
        if mail.trueLabel not in mail.folder:
            try:
                self.FR[mail.trueLabel]=self.FR[mail.trueLabel]+1
            except:
                self.FR[mail.trueLabel]=1
        self.update()

        return mail.folder


class Email(object):
    def __init__(self, body=""):
        self.body = body
        if body:
            self.mat = format(body)
        else:
            self.mat = []
        self.folder = []
        self.label = ''
        self.trueLabel = ''
        self.credit = 0
        self.proba = {}
        self.read = False
        self.raw_email = ''
        self.subject=""

    def set_read(self):
        self.read = True

    def set_label(self, label):
        self.label = label

    def set_body(self, body):
        self.body = body
        self.mat = format(body)

    def set_credit(self, credit):
        self.credit = credit

    def set_folder(self, foldername):
        self.folder = [foldername]

    def get_body(self):
        return self.body

    def get_raw(self):
        return self.raw_email

    def get_probab(self):
        return self.proba

    def get_label(self):
        return self.label

    def get_trueLabel(self):
        return self.trueLabel

    def get_credit(self):
        return self.credit


"If user read, forward, reply this email. Will not trigger if current_folder is uncertain or trash"


def activity_yes(email, current_folder):
    global pool, features
    if features[0]:
        email.set_label(current_folder)
        try:
            email.set_credit(1 - email.proba[current_folder])
        except:
            pass
        if email not in pool:
            pool.append(email)
    check_credit()


"If user move this email into a target_folder. Will not trigger if target_folder is uncertain or trash."


def activity_no(email, target_folder):
    global pool, features
    if features[0] or features[1]:
        email.set_label(target_folder)
        try:
            email.set_credit(1 - email.proba[target_folder])
        except:
            email.set_credit(1)
        if email not in pool:
            pool.append(email)
    check_credit()


"Runs every mid-night? Retrain the classifier or not"


def check_credit():
    global pool, my_folder, saturation, lastcan
    can = []
    for label in my_folder.names:
        if label=='uncertain' or label=='trash': continue
        collect = [x for x in pool if x.label == label]
        credits = [x.credit for x in collect]
        many=int(len(pool)/(len(my_folder.names)-2))
        can.extend(list(np.array(collect)[np.argsort(credits)[-many:]]))
    if can!=lastcan:
        my_folder.train(can)
        lastcan=can
    if len(pool) > saturation:
        pool=can
    return True


if __name__ == '__main__':
    global feature_number, hashemail, my_folder, pool, saturation, currentfolder, features, feature_names, new_mails, list_mails, lastcan

    "Global variables, need to be initialized"
    feature_number = 4000
    hashemail = hasher(feature_number)
    my_folder = Folder()
    pool = []
    list_mails=[]
    saturation = 1000
    currentfolder = "uncertain"
    features = [True, True, True]
    feature_names = ['implicit feedback', 'explicit feedback', 'multi-folder']
    "feature[0]: implicit user feedback; feature[1]: explicit user feedback; feature[2]: multi-folder"
    new_mails=[]
    lastcan=[]

    #new mail reading
    readnew()

    # pool of mails with intial labels.
    readfile(Mails_directory)
    # check_credit()
    # GUI
    root = Tk()
    root.title("Mailbox")
    root.minsize(width=1000, height=600)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
