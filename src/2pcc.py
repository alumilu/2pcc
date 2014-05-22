import sys
import os
import time
import pprint
import smtplib
import email.utils
from email.mime.text import MIMEText

from dropbox import client, rest, session
from ListenerClient import WhatsappListenerClient

#dropbox
APP_KEY = 'q1ru9t5gazblj6k'
APP_SECRET = 'rksdnwguwh99tqq'

#gmail
fromaddr = 'hubert.lu@gmail.com'  
toaddrs  = 'hubert.lu@gmail.com'  
username = 'hubert.lu@gmail.com'  
password = '@luminum013175'  

#Whatsapp
phone = "886929810849"
pwd="1xclLFIzKGgRihMBWJZub+n8Ifc="

def handleDelta(dropboxclt, entries):
    print "handling changes: " 
    pprint.PrettyPrinter(indent=2).pprint(entries)

    for e in entries:	
	if e[1] is not None:
		print 'Change: %s is added, copy it to local' % e[0]
		with open(os.path.join('download/', os.path.basename(e[1]['path'])), 'wb') as of:
			with dropboxclt.get_file(e[1]['path'])  as f:
				of.write(f.read())
				try:
				    dropboxclt.file_delete(e[1]['path'])
				    print '%s is downloaded' % e[1]['path'] #if downloaded, then delete the file from dropbox
				except:
				    os.remove(os.path.join('download/', os.path.basename(e[1]['path'])))
				    print '%s download failed, just keep it upon dropbox' %  e[1]['path']
	else:
		print 'Change: %s is deleted, do nothing' % e[0]
  
    return

def main():
    if APP_KEY == '' or  APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")
        
    whatsappListner = WhatsappListenerClient(True, True)
    whatsappListner.login(phone, base64.b64decode(bytes(pwd.encode('utf-8'))))
	
    sess = session.DropboxSession(APP_KEY, APP_SECRET)
    request_token = sess.obtain_request_token()
    authorize_url = sess.build_authorize_url(request_token)
	
    #print "1. Go to: " + authorize_url + "\n"
    #print "2. Click \"Allow\" (you might have to log in first).\n"
  	
    # The actual mail send
    msg = MIMEText(authorize_url)
    msg['Subject'] = '2pcc message'
	
    print "\n"	
    print "sending email to get auth...\n"

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')  
	server.ehlo()
        server.starttls()  
        server.login(username,password)  
        server.sendmail(fromaddr, toaddrs, msg.as_string())  
        server.quit()
    except:
	print "fail to send email notification!!"
	return
	
    print "email has been sent successfully!\n"
	
    bAllow = False
	
    while (bAllow is False):
	time.sleep(3)
	
        try:
            access_token = sess.obtain_access_token()
	    bAllow = True
        except rest.ErrorResponse, e:
            print 'waitting user\'s auth...'
	    continue
    
    dropboxClt = client.DropboxClient(sess)	
    accountInfo = dropboxClt.account_info()
	
    print "hello %s ! You just allow 2pcc to access and monitor changes in your dropbox.\n" % accountInfo['display_name']
   
    #pprint.PrettyPrinter(indent=2).pprint(accountInfo)

    rt = None
    path_prefix = '/2pcc'
	
    while True:	
	
        if rt is None: #initial check, ignore verything	
	    rt = dropboxClt.delta(None, path_prefix)
	    print 'this is initail check, will ignore everything\n'
	    time.sleep(30)
	    continue
	else:
	    rt = dropboxClt.delta(rt['cursor'], path_prefix)
		
	if len(rt['entries']) > 0:
	    handleDelta(dropboxClt, rt['entries'])
		
            while rt['has_more'] is True:
	        rt = dropboxClt.delta(rt['cursor'], path_prefix)
		handleDelta(dropboxClt, rt['entries'])
			 
	    print "all changes are handled, will check again after 5 mins.\n"
	    time.sleep(30) #if no change, then wait at least 5 min. per dropbox api req.
	else:
	    print "no change found, will check again after 30secs.\n"
	    time.sleep(30)
		    

if __name__ == '__main__':
    main()
