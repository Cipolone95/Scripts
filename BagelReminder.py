import smtplib, datetime


###Acquire Email and password of the user
print('Please enter your email:')
senderEmail = input()

print('Please enter your password:')
senderPassword = input()

##Acquiring the email of the recipient
print('Please enter the email address of the recipient')
recipientEmail = input()

###Setting date for when to bring bagels
d = datetime.date.today() + datetime.timedelta(days=1)
tomorrowDate = d.strftime('%m/%d/%Y') 


Subject = 'Bagels Tomorrow!'
Message = ('This automated message is reminding you' +
'that you have signed up to bring bagels tomorrow,' +
tomorrowDate + '. If you no longer can, please respond to' + 
' this message so the back up person can be notified.' + 
' Thank you.') 





smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('senderEmail', 'senderPassword')


EmailBodyString = 'Subject:' + Subject + '\n' + Message


smtpObj.sendmail(senderEmail, recipientEmail, EmailBodyString)

smtpObj.quit()
