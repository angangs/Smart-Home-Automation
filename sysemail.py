import smtplib
import imaplib

port = 8080
relay1 = 7
relay2 = 6
relay3 = 5
relay4 = 4
relay5 = 3
relay6 = 2
relay7 = 1
relay8 = 0
in1 = 4
in2 = 17
in3 = 27
in4 = 23
in5 = 22
in6 = 24
in7 = 11
in8 = 7
in9 = 8
in10 = 9
in11 = 25
in12 = 10
out1 = 18
inputlist = [in1, in2, in3, in4, in5, in6, in7, in8, in9, in10, in11, in12]
outputlist = [out1]
relaylist = [relay1, relay2, relay3, relay4, relay5, relay6, relay7, relay8]

smtpUser = "vatomouro2016@gmail.com"
smtpPass = "basangelos"
fromAdd = smtpUser
subject = "Notification: Sweet Home"
body0 = "Server was started!"
body11 = "Input 11 is ON!"
body12 = "Input 12 is ON!"

def matchString(st):
    if st == str(1):
        newst = "O"
    elif st == str(0):
        newst = "I"
    elif st == str(False):
        newst = "OFF"
    elif st == str(True):
        newst = "ON"
    else:
        newst = str(st)
    return newst

def main(inputstate, email, home):
    toAdd = email
    header = "To: " + toAdd + "\n" + \
             "From: " + fromAdd + "\n" + \
             "Subject: " + subject + "\n"
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(smtpUser, smtpPass)
    if inputstate==11:
        mail.sendmail(smtpUser, toAdd, header+"\n"+body11)
    elif inputstate==12:
        mail.sendmail(smtpUser, toAdd, header + "\n" + body12)
    elif inputstate == "status":
        dinlist = home.readdigitalinput()
        bodystatus = "Digital Input 1: " + matchString(str(dinlist[0])) + "\n" + \
                     "Digital Input 2: " + matchString(str(dinlist[1])) + "\n" + \
                     "Digital Input 3: " + matchString(str(dinlist[2])) + "\n" + \
                     "Digital Input 4: " + matchString(str(dinlist[3])) + "\n" + \
                     "Digital Input 5: " + matchString(str(dinlist[4])) + "\n" + \
                     "Digital Input 6: " + matchString(str(dinlist[5])) + "\n" + \
                     "Digital Input 7: " + matchString(str(dinlist[6])) + "\n" + \
                     "Digital Input 8: " + matchString(str(dinlist[7])) + "\n" + \
                     "Digital Input 9: " + matchString(str(dinlist[8])) + "\n" + \
                     "Digital Input 10: " + matchString(str(dinlist[9])) + "\n" + \
                     "Digital Input 11: " + matchString(str(dinlist[10])) + "\n" + \
                     "Digital Input 12: " + matchString(str(dinlist[11])) + "\n\n" + \
                     "Digital Output 1: " + matchString(
            str(home.readrelay(home.io, relaylist[0]))) + "\n" + \
                     "Digital Output 2: " + matchString(
            str(home.readrelay(home.io, relaylist[1]))) + "\n" + \
                     "Digital Output 3: " + matchString(
            str(home.readrelay(home.io, relaylist[2]))) + "\n" + \
                     "Digital Output 4: " + matchString(
            str(home.readrelay(home.io, relaylist[3]))) + "\n" + \
                     "Digital Output 5: " + matchString(
            str(home.readrelay(home.io, relaylist[4]))) + "\n" + \
                     "Digital Output 6: " + matchString(
            str(home.readrelay(home.io, relaylist[5]))) + "\n" + \
                     "Digital Output 7: " + matchString(
            str(home.readrelay(home.io, relaylist[6]))) + "\n" + \
                     "Digital Output 8: " + matchString(
            str(home.readrelay(home.io, relaylist[7]))) + "\n\n" + \
                     "Analog Input 1: " + str(home.readanaloginput(0)) + "\n" + \
                     "Analog Input 2: " + str(home.readanaloginput(1)) + "\n\n" + \
                     "Analog Output: " + str(home.readvo()) + "\n\n"
        mail.sendmail(smtpUser, toAdd, header + "\n" + bodystatus)
        obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
        obj.login(smtpUser, smtpPass)
        obj.select('Inbox')
        typ, data = obj.search(None, 'UnSeen')
        data = str(data).replace("\'","").replace("[","").replace("]","").split()
        obj.store(data[0].replace(' ', ','), '+FLAGS', '\Seen')
    else:
        mail.sendmail(smtpUser, toAdd, header + "\n" + body0)
    mail.close()