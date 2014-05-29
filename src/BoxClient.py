'''
Copyright (c) <2014> Hubert Lu <hubert.lu@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import sys
import os
import time
import pprint
import smtplib
import email.utils

from email.mime.text import MIMEText
from dropbox import client, rest, session

class DropboxClient:
	#registered dropbox app key and secret
        APP_KEY = 'q1ru9t5gazblj6k'
        APP_SECRET = 'rksdnwguwh99tqq'
	
	def __init__(self, mailbox, mailbox_usr, mailbox_pwd):
	    self.mailbox = mailbox
	    self.mailboxUsr = mailbox_usr
	    self.mailboxPwd = mailbox_pwd
	    self.mailServer = smtplib.SMTP('smtp.gmail.com:587') 
	    self.dropboxClt = None
	    self.accountInfo = None
	    self.msg = None
	    self.msgSubject = '2pcc message'
	    
        def sendMail()
	    bRt = True
		
	    try:
	        self.mail_server.ehlo()
		self.mail_server.starttls()  
		self.mail_server.login(self.mailboxUsr, self.mailboxPwd)  
		self.mail_server.sendmail(self.mailbox, self.mailbox, self.msg.as_string())  
		server.quit()
	     except:
		bRt = False
	    
	     return bRt
	
	def connect(self):
	    sess = session.DropboxSession(DropboxClient.APP_KEY, DropboxClient.APP_SECRET)
	    request_token = sess.obtain_request_token()
	    authorize_url = sess.build_authorize_url(request_token)
	
	    self.msg = MIMEText(authorize_url)
	    self.msg['Subject'] = self.msg_subject
		
	    print "sending email to get auth...\n"

	    if !self.sendMail():
	        print "fail to send email notification!!"
		return False
	
	    print "email has been sent successfully!\n"
		
	    while True:
		time.sleep(5)
		
		try:
		    access_token = sess.obtain_access_token()
		    break
		except rest.ErrorResponse, e:
		    print 'waitting user\'s auth...'
		    continue
    
	    self.dropboxClt = client.DropboxClient(sess)	
	    self.accountInfo = dropboxClt.account_info()
	
	    print "hello %s ! You just allow 2pcc to access and monitor changes in your dropbox.\n" % self.accountInfo['display_name']
	    #pprint.PrettyPrinter(indent=2).pprint(accountInfo)
	
	    return True
	    