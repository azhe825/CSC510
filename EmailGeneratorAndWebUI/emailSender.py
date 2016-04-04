import smtplib

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems

problems = sendemail(from_addr    = 'test2016emailproject@gmail.com',
          to_addr_list = ['test2016emailreceiver@gmail.com'],
          cc_addr_list = [''],
          subject      = 'Hello gmail',
          message      = 'We are connected successfully!',
          login        = 'test2016emailproject',
          password     = 'password2016END',
          smtpserver   = 'smtp.gmail.com:587')

print problems