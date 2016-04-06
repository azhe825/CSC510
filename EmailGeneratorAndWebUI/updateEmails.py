import imaplib
import sys

def loginMail(loginID, password):
    status = 'Unconnected'
    mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
    if '@gmail.com' not in loginID:
        print "We currently support gmail only!"
    status = mailbox.login(loginID, password)
    if  status[0] != 'OK':
        print "Login failed: Check ID and password."
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
        result, data = mailbox.fetch(id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        if result == 'OK':
            mailList.append(data[0][1])
        else:
            print "Email not available!"
    return mailList

def main():
    loginID = 'test2016emailreceiver@gmail.com'
    password = 'password2016END'
    status, mailPort = loginMail(loginID, password)
    print status
    mailList = list()
    if status[0] == 'OK':
        mailList = fetchMail(mailPort)
    for mail in mailList:
        print mail

if __name__ == "__main__":
    main()