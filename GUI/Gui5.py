from __future__ import print_function, division

__author__ = 'Amrit, Zhe, Jerry, Jack'

from Tkinter import *
from func_GUI import *
import re
import random
from email import message_from_string
import imaplib

Mails_directory = "../Mails/struct2.txt"

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

"login the gmail account and extract all emails"

def loginMail(loginID, password):
    status = ('Unconnected',[])
    mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
    if '@gmail.com' not in loginID:
        print('We currently support gmail only')
    status = mailbox.login(loginID, password)
    if  status[0] != 'OK':
        print('Login failed: Check ID and password.')
    return status, mailbox

def fetchMail(mailbox):
    # mail.list() # list all folder in the email account
    # Out: list of "folders" aka labels in gmail.
    mailList = list()
    mailbox.select("inbox")  # connect to inbox.
    result, emailIndex = mailbox.search(None, "ALL") # select all emails, result = 'OK' if succeed
    ids = emailIndex[0]  # emailIndex is a list.
    id_list = ids.split()  # ids is a space separated string
    for id in id_list:
        result, mailtext = mailbox.fetch(id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        if result == 'OK':
            mailList.append(mailtext[0][1])
        else:
            print("Email not available")
    return id_list, mailList


"read the initial setup from struct2.txt"


def readfile(filename):
    global my_folder, pool, list_mails
    with open(filename, 'r') as f:
        for doc in f.readlines():
            try:
                x = Email(doc.split(" >>> ")[1].strip())
                x.set_label(doc.split(" >>> ")[0].split()[1])
                x.credit = 1
                x.folder.append(doc.split(" >>> ")[0].split()[1])
                if doc.split(" >>> ")[0].split()[0] == "read":
                    x.read = True
                else:
                    x.read = False
                if not x.label in my_folder.names:
                    my_folder.addfolder(x.label)
                pool.append(x)
            except:
                pass

    my_folder.train(pool)
    list_mails = pool


def readnew():
    # with open("../Mails/newmails.txt", 'r') as f:
    #     for doc in f.readlines():
    #         new_mails.append(doc.strip())
    global record_id_list, new_mails
    status, mailPort = loginMail(login_id, pass_word)
    mailList = list()
    if status[0] == 'OK':
        id_list, mailList = fetchMail(mailPort)
    # check for new mail update
    numberOfNewMail = len(id_list) - len(record_id_list)
    if numberOfNewMail != 0:
        for i in range(numberOfNewMail):
            new_mails.append(mailList[-(i + 1)])


"when new email comes in"
def new_email(mailText):
    global list_mails, my_folder
    subject, body, mail_subject, mail_body = email_parser(mailText)
    mail_body = mail_subject + mail_body
    newmail = Email(mail_body)
    newmail.read=False
    list_mails.append(newmail)
    my_folder.predict(newmail)


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.Frame = master
        self.count = 0
        self.buttons = []
        self.folderName_button = {}
        self.checkbox = {}
        self.pack()
        self.waste = ''
        self.poplogin()
        if (self.entryValue() == 1):
            readfile(Mails_directory)
            self.createWidgets()
        else:
            root.destroy()


    def refresh(self):
        global list_mails, currentfolder
        self.unread.delete(first=0, last=self.unread.size())
        self.read.delete(first=0, last=self.read.size())
        folder_unreadNum = {}
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
                    self.read.insert('end', "%0.4d : %s" % (i, mail.get_body()))
                else:
                    self.unread.insert('end', "%0.4d : %s" % (i, mail.get_body()))
        for folder, button in self.folderName_button.iteritems():
            if folder in ['uncertain', 'trash']:
                continue
            unreadNum = folder_unreadNum[folder]
            if unreadNum == 0:
                button.config(text=folder)
            else:
                button.config(text=folder + ' (' + str(unreadNum) + ')' )

    def button_command(self, a): # set the currentfolder to a
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
        w = event.widget
        self.popup1(w.get(w.curselection()).split(' : ')[1])
        global list_mails, currentfolder
        if not (currentfolder == 'uncertain' or currentfolder == 'trash'):
            activity_yes(list_mails[int(w.get(w.curselection()).split(' : ')[0])], currentfolder)
        self.refresh()

    def incoming(self):
        x=random.randint(0,len(new_mails)-1)
        print(x)
        l=''
        with open(new_mails.pop(x), 'r') as f:
            for doc in f.readlines():
                l+=doc
        new_email(l)

        self.refresh()


    def unread_user(self, event):
        w = event.widget
        self.popup1(w.get(w.curselection()).split(' : ')[1])
        global list_mails, currentfolder
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
            my_folder.names.append(a)
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
        self.m3.add(self.newm)
        self.m3.add(self.CREATE_Labels)
        self.Login = Button(self, text="Login", fg="red", command=self.poplogin, state=ACTIVE)
        self.m3.add(self.Login)

        for feature_id in range(len(features)):
            self.create_checkbox(feature_id)

        self.button_command('uncertain')

    def popup_menu(self, event):
        w = event.widget
        self.aMenu = Menu(self, tearoff=0)
        # print(labels_gui)
        for i in my_folder.names:
            #print(i)
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

    def poplogin(self):
        self.w = popupWindowLogin(self.Frame)
        self.Frame.wait_window(self.w.top)


    def entryValue(self):
        return self.w.value


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

class popupWindowLogin(object): ## not working now
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.l1 = Label(top, text="Login ID:")
        self.l1.pack()
        self.id = Entry(top)
        self.id.pack()
        self.l2 = Label(top, text="Password:")
        self.l2.pack()
        self.pwd = Entry(top)
        self.pwd.pack()
        self.b = Button(top, text='Submit', command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        login_id = self.id.get()
        pass_word = self.pwd.get()
        status, mailPort = loginMail(login_id, pass_word)
        if status[0] == 'OK':
            id_list, mailList = fetchMail(mailPort)
            numberOfNewMail = len(id_list) - len(record_id_list)
            if numberOfNewMail != 0:
                for i in range(numberOfNewMail):
                    new_mails.append(mailList[-(i + 1)])
            self.value=1
        else:
            self.value=0
            print("Connection Failed.")
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

    def addfolder(self, name):
        self.names.append(name)
        self.num = self.num + 1

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
        self.credit = 0
        self.proba = {}
        self.read = False

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

    def get_probab(self):
        return self.proba

    def get_label(self):
        return self.label

    def get_credit(self):
        return self.credit


"If user read, forward, reply this email. Will not trigger if current_folder is uncertain or trash"


def activity_yes(email, current_folder):
    global pool, features
    if features[0]:
        email.set_label(current_folder)
        if email.proba:
            email.set_credit(1 - email.proba[current_folder])
        if email not in pool:
            pool.append(email)
    check_credit()


"If user move this email into a target_folder. Will not trigger if target_folder is uncertain or trash."


def activity_no(email, target_folder):
    global pool, features
    if features[0] or features[1]:
        email.set_label(target_folder)
        if email.proba:
            email.set_credit(1 - email.proba[target_folder])
        if email not in pool:
            pool.append(email)
    check_credit()


"Runs every mid-night? Retrain the classifier or not"


def check_credit():
    global pool, prog, step, my_folder, saturation
    if len(pool) >= my_folder.num * prog * step:
        can = []
        for label in my_folder.classifier.classes_:
            collect = [x for x in pool if x.label == label]
            credits = [x.credit for x in collect]
            can.extend(list(np.array(collect)[np.argsort(credits)[-prog * step:]]))
        my_folder.train(can)
        if prog <= saturation:
            prog = prog + 1
        else:
            pool = can
        return True
    else:
        return False


if __name__ == '__main__':
    global feature_number, hashemail, my_folder, pool, prog, step, saturation, currentfolder, features, feature_names, new_mails, login_id, pass_word, record_id_list

    "Global variables, need to be initialized"
    feature_number = 4000
    hashemail = hasher(feature_number)
    my_folder = Folder()
    pool = []
    prog = 10
    step = 1
    saturation = 100
    currentfolder = "uncertain"
    features = [True, True, True]
    feature_names = ['implicit feedback', 'explicit feedback', 'multi-folder']
    new_mails=[]
    login_id = ''
    pass_word = ''
    record_id_list = []
    "feature[0]: implicit user feedback; feature[1]: explicit user feedback; feature[2]: multi-folder"

    #new mail reading
    #readnew()

    # pool of mails with intial labels.
    # check_credit()
    # GUI
    root = Tk()
    root.title("Mailbox")
    root.minsize(width=1000, height=600)
    app = Application(master=root)
    app.mainloop()
    root.destroy()
