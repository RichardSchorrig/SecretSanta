import smtplib, imaplib, ssl
from getpass import getpass

#from email import encoders
from email.message import EmailMessage

class EmailSender:
    """this class sends a template to multiple receivers"""

    smtp_server = "smtp.gmail.com"
    imap_server = "imap.gmail.com"
    port = 587

    class TextArgs:
        """this class is used as a way to personalize the email"""
        def __init__(self, args):
            """create a new argument list
            @param args: a list of arguments for the text template
            """
            self.args = args

    def __init__(self, subject, text, textArgs, *receiverList, test=False, password=None, emailaddress=None, doNotDeleteSentMails=False):
        """ constructor is used to to all the work of sending the email template
        @param subject: the subject of the email
        @param text: a text template. This is formatted using the function 'format' and the given textArgs
        @param textArgs: a directory (key is the receivers email) of arguments to format the text
        @param test: set to true to use the localhost smtp daemon
        @param password: can be used to provide the password (if not provided, the function will ask for it
        @param emailaddress: the emailaddress to use, will be asked if not provided
        @param doNotDeleteSentMails: set this to true if you want to keep the sent emails in the sentbox of your email account
        """
        if (None == password) & (None == emailaddress) & (not test):
            # ask for gmail address and password
            print("type your gmail address (only works with gmail) and password")
            print("email address: ", end="")
            sendMail = input()
            password = getpass()
        
        smtp_server = EmailSender.smtp_server
        smtp_port = EmailSender.port

        # for testing: use localhost
        if test:
            smtp_server = "localhost"
            smtp_port = 1025
        # send the emails
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            try:
                if not test:
                    # Create a secure SSL context
                    context = ssl.create_default_context()
                    server.ehlo()
                    server.starttls(context=context) # and secure the connection
                    server.ehlo()
                    server.login(sendMail, password)

                message = EmailMessage()
                message['from'] = sendMail
                message['subject'] = subject
                
                for receiver in receiverList:
                    del message['to']
                    message['to'] = receiver
                    message.clear_content()
                    message.set_content(text.format(*textArgs[receiver].args))
                    server.sendmail(sendMail, receiver, message.as_string())

            except Exception as e:
                print(e)
            finally:
                server.quit()

        # delete the sent emails right after
        if (not doNotDeleteSentMails) & (not test):
            with imaplib.IMAP4_SSL(EmailSender.imap_server) as imap:
                try:
                    imap.login(sendMail, password)
                    print(imap.select('[Gmail]/Gesendet', readonly=False))
                    typ, data = imap.search(None, 'SUBJECT \"' + subject + '\"')
                    for num in data[0].split():
                        imap.store(num, "+Flags", "\\Deleted")
                    imap.expunge()

                except Exception as e:
                    print(e)
                finally:
                    imap.close()
                    imap.logout()
    
def test():

    # For this test, the build in smtp daemon can be used, run:
    # python -m smtpd -c DebuggingServer -n localhost:1025

    text = "This is a test for {0}\n" +\
           "Hello {0},\n" +\
           "You are won Eur {1},{2:02d}!\n" +\
           "\n" +\
           "Yours sincerely\n" +\
           "Spammer\n"
    textArgs = {}
    emailReceiver = ("richard.schorrig@fn.de",
                      "richard.schorrig@web.de",
                      "richard.schorrig@outlook.de",
                      "richi.schorrig@t-online.de")

    import random
    import time

    random.seed(time.time())
    for receiver in emailReceiver:
        textArgs[receiver] = EmailSender.TextArgs(("Happy Winner #" + str(random.randint(1, 10000)), random.randint(0,1), random.randint(0,99)))
    
    for receiver in emailReceiver:
        print(text.format(*textArgs[receiver].args))

    EmailSender("You Won!", text, textArgs, *emailReceiver, test=True)

if __name__ == '__main__':
    test()