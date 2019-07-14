from twilio.rest import TwilioRestClient
from twilio.rest import Client
import smtplib, datetime, openpyxl, sys, xlwt 


#Twilio Variables - Will need to change these
accountSID = 'Twilio Account SID'
authToken = 'Twilio Auth Token'
myNumber = 'Your Phone Number'
twilioNumber = 'Twilio Phone Number'
resultMessage = '' 

#Email Variables
myEmail = 'Email of the sender'
myEmailPassword = 'Email Sender Password'
recipientEmail = ''
recipientName = ''

#Creating the body of the email
d = datetime.date.today() + datetime.timedelta(days=1)
tomorrowDate = d.strftime('%m/%d/%Y')

Subject = 'Bagels Tomorrow!'
TEXT = ("This message is reminding you " +
" that you have signed up to bring bagels tomorrow," + 
 tomorrowDate + '. If you no longer can, please respond to' +  
" this message so the back up person can be notified. Thank you.") 

#Getting the email of the recipient
#Opening up the signup sheet
wb = openpyxl.load_workbook('Path of spreadsheet containing list of individuals')
sheet = wb['Sheet1']
lastRow = sheet.max_row
lastCol = sheet.max_column
for r in range(2, lastRow + 1):
    turn = sheet.cell(row = r, column = lastCol).value
    if turn != 'x':
        recipientName = sheet.cell(row = r, column = 1).value
        sheet.cell(row = r, column = 2).value = 'x'
        wb.save('saving the spreadsheet after it has been updated')
        break

firstName, lastName = recipientName.split(" ")
recipientEmail = firstName[0] + lastName + "@SomeDomain.com" #Will need to change this
                                                             #to match format of email 



#Connecting to the email server and sending the email
smtpObj = smtplib.SMTP('Name of Email Server', 587) 
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(myEmail, myEmailPassword)



message = 'Subject: {}\n\n{}'.format(Subject,TEXT)
sendMailStatus = smtpObj.sendmail(myEmail, recipientEmail, message)

#Sending the text message receipt
client = Client(accountSID, authToken)
                                  
#Checking to see if email was sent sucessfully 
if sendMailStatus != {}:
    resultMessage = "Error sending bagel email reminder"
else:
    resultMessage = "Bagel email reminder sent successfully"
message = client.messages.create(
    to = myNumber, 
    from_ = twilioNumber,
    body = resultMessage)

#Close the smtp connection
smtpObj.quit()
