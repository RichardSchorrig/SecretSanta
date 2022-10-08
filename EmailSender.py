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

    def __init__(self, subject, text, textArgs, *, emailaddress=None, password=None, doNotDeleteSentMails=False, test=False):
        """constructor is used to do all the work of sending the email template
        --- CAUTION: use a junk gmail account for this, to not lose important emails ---
        Gmail has to be set up that it allows less secure apps and allow access via IMAP and SMTP
        the list of receiving emails shall be provided with the textArgs directory.
        Example: textArg[test@test.com] = TextArg("test", 123)
        This way the receiver is tied to his personal email message.
        After the emails have been sent, they are deleted from the server using imap. Be careful, as this function simply
        searches for the subject. This could affect other emails, too.
        @param subject: the subject of the email
        @param text: a text template. This is formatted using the function 'format' and the given textArgs
        @param textArgs: a directory (key is the receivers email) of arguments to format the text
        @param test: set to true to use the localhost smtp daemon
        @param password: can be used to provide the password (if not provided, the function will ask for it
        @param emailaddress: the emailaddress to use, will be asked if not provided
        @param doNotDeleteSentMails: set this to true if you want to keep the sent emails in the sentbox of your email account
        """
        if (None == emailaddress):
            # ask for gmail address and password
            print("type your gmail address (only works with gmail) and password")
            print("email address: ", end="")
            emailaddress = input()
        if (None == password) & (not test):
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
                    #server.ehlo()
                    server.starttls()
                    #server.starttls(context=context) # and secure the connection
                    #server.ehlo()
                    server.login(emailaddress, password)

                message = EmailMessage()
                message['from'] = emailaddress
                message['subject'] = subject
                
                for receiver in textArgs.keys():
                    del message['to']
                    message['to'] = receiver
                    message.clear_content()
                    message.set_content(text.format(*textArgs[receiver].args))
                    server.sendmail(emailaddress, receiver, message.as_string())

            except Exception as e:
                print(e)
            finally:
                server.quit()

        # delete the sent emails right after
        if (not doNotDeleteSentMails) & (not test):
            with imaplib.IMAP4_SSL(EmailSender.imap_server) as imap:
                try:
                    imap.login(emailaddress, password)
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
    """For this test, the build in smtp daemon shall be used, run:
    python -m smtpd -c DebuggingServer -n localhost:1025
    in a console / shell
    """

    text = "This is a test for {0}\n" +\
           "Hello {0} {1},\n" +\
           "You are won ${2},{3:02d}!\n" +\
           "\n" +\
           "Yours sincerely\n" +\
           "Newman\n"
    textArgs = {}
    emailReceiver = ("george.costanza@seinfeld.com",
                     "jerry.seinfeld@seinfeld.com",
                     "elaine.benes@seinfeld.com",
                     "cosmo.kramer@seinfeld.com")

    import random
    import time
    import re

    random.seed(time.time())
    for receiver in emailReceiver:
        firstName = str.capitalize(re.split("[.@]", receiver)[0])
        lastName = str.capitalize(re.split("[.@]", receiver)[1])
        textArgs[receiver] = EmailSender.TextArgs((firstName, lastName, random.randint(0,1), random.randint(0,99)))

    EmailSender("You Win!", text, textArgs, test=True, emailaddress="newman@hawaiianpostaloffice.com")

if __name__ == '__main__':
    test()