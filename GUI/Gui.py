__author__ = 'amrit'

from Tkinter import *
import ttk

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.m = PanedWindow(self, orient=HORIZONTAL)
        self.m.pack(fill=BOTH, expand=1)

        self.INBOX = Button(self.m, text = "INBOX", fg   = "red", command =  self.quit)
        self.INBOX.pack(side=TOP, anchor=W, fill=X, expand=YES, )
        self.m.add(self.INBOX)
        self.SPAM = Button(self.m, text = "SPAM", fg   = "red", command =  self.quit)
        self.SPAM.pack(side=TOP, anchor=W, fill=X, expand=YES, )
        self.m.add(self.SPAM, after=self.INBOX)
        self.RANDOM = Button(self.m, text = "RANDOM", fg   = "red", command =  self.quit)
        self.RANDOM.pack(side=TOP, anchor=W, fill=X, expand=YES, )
        self.m.add(self.RANDOM, after=self.SPAM)
        self.USER = Button(self.m, text = "USER", fg   = "red", command =  self.quit)
        self.USER.pack(side=TOP, anchor=W, fill=X, expand=YES, )
        self.m.add(self.USER, after=self.RANDOM)
        self.m2 = PanedWindow(self.m, orient=VERTICAL)
        self.m2.pack(fill=BOTH, expand=1)
        self.m.add(self.m2)

        #.hi_there = Button(self.m2, text = "Hello", command = self.say_hi)
        #self.m2.add(self.hi_there)

        self.top_right = Label(self.m2, text="Unread")
        self.m2.add(self.top_right)

        self.unread = Listbox(self.m2, width=120, height=20)
        self.unread.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.unread.yview, orient='vertical')
        #self.s.grid(column=0, row=0, sticky="ns")
        self.unread.config(yscrollcommand = self.s.set)
        for i in range(100):
            self.unread.insert('end', "Email %d" % i)
        self.unread.pack()
        self.m2.add(self.unread)

        self.bottom_right = Label(self.m2, text="Read")
        self.m2.add(self.bottom_right)
        self.read = Listbox(self.m2, width=120, height=20)
        self.read.grid(column=0, row=0, sticky='nwes')
        self.s = Scrollbar(command=self.read.yview, orient='vertical')
        #self.s.grid(column=0, row=0, sticky="ns")
        self.read.config(yscrollcommand = self.s.set)
        for i in range(100):
            self.read.insert('end', "Email %d" % i)
        self.read.pack()
        self.m2.add(self.read)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("Mailbox")
root.minsize(width=1000,height=600 )
app = Application(master=root)
app.mainloop()
root.destroy()
'''
root = Tk()
root.title("Mailbox")
root.minsize(width=1000,height=600 )
#root.resizable(width=1000,height=1000)
PanedWindow
l = Tkinter.Listbox(height=5)
l.grid(column=0, row=0, sticky='nwes')
s = ttk.Scrollbar(command=l.yview, orient='vertical')
l['yscrollcommand'] = s.set
s.grid(column=1, row=0, sticky="ns")

stat = ttk.Label(text="Status message here", anchor='w')
stat.grid(column=0, row=1, sticky='we')

sz = ttk.Sizegrip()
sz.grid(column=1, row=1, sticky='se')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

for i in range(100):
    l.insert('end', "Line %d of 100" % i)

root.mainloop()'''