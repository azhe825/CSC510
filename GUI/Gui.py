__author__ = 'amrit'

from Tkinter import *
import ttk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Mails_directory="/../Cleaned_Data/beck-s.txt1"

def readfile(filename):
    corpus=[]
    with open(filename,'r') as f:
        for doc in f.readlines():
            try:
                corpus.append(doc.split(" ::::::>>>>>> ")[1][:-2])
            except:
                pass

    return corpus

class Application(Frame):


    def inbox_command(self):
        mails= readfile(BASE_DIR+Mails_directory)
        self.unread.delete(first=0, last=self.unread.size())
        for i in range(len(mails)):
            self.unread.insert('end', "%0.4d : %s" % (i, mails[i]))

    def spam_command(self):
        mails= readfile(BASE_DIR+Mails_directory)
        self.unread.delete(first=0, last=self.unread.size())
        for i in range(len(mails)):
            self.unread.insert('end', "%0.4d : %s" % (i, mails[i]))

    def trash_command(self):
        mails= readfile(BASE_DIR+Mails_directory)
        self.unread.delete(first=0, last=self.unread.size())
        for i in range(len(mails)):
            self.unread.insert('end', "%0.4d : %s" % (i, mails[i]))

    def mov_command(self):
        print "Move"

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
        self.CREATE_Labels = Button(self.m, text = "CREATE_LABELS", fg   = "red", command =  self.c_labels_command, state=ACTIVE)
        self.m.add(self.INBOX)
        self.m.add(self.SPAM)
        self.m.add(self.TRASH)
        #self.USER.pack(side=BOTTOM, anchor=W, fill=X)
        self.m.add(self.CREATE_Labels)
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
        self.read.pack()
        self.m2.add(self.read)

        self.m3 = PanedWindow(self, orient=VERTICAL)
        self.m3.pack(side=RIGHT, expand=1)
        self.delete = Button(self, text="DELETE", command=lambda lb=self.unread: lb.delete(ANCHOR))
        self.mov = Button(self, text="MOVE", command=self.mov_command)
        self.m3.add(self.delete)
        self.m3.add(self.mov)

    def popup(self):
        self.w=popupWindow(self.Frame)
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


root = Tk()
root.title("Mailbox")
root.minsize(width=1000,height=600 )
app = Application(master=root)
app.mainloop()
root.destroy()