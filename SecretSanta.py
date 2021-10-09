import csv
from getpass import getpass
import getopt
import sys

from PartnerChooser import PartnerChooser
from EmailSender import EmailSender

class SecretSanta:

    def __init__(self, wishlist, template, *, emailaddress=None, password=None, doNotDeleteSentMails=False, test=False):

        emails = {}
        wishes = {}

        # open and parse the csv file
        csvFile = open(wishlist)
        csvReader = csv.reader(csvFile, delimiter=";", quotechar="\"")
        for row in csvReader:
            if len(row) < 2:
                raise Exception("in the csv file, at least the email address and the name is expected, actual: " *row)

            emails[row[1]] = row[0]
            if len(row) > 2:
                wishes[row[1]] = row[2]
            else:
                wishes[row[1]] = "nothing special"
        csvFile.close()

        # open and read the email template; the first line is used as the subject
        templateFile = open(template, "rt")
        text = templateFile.read()
        subject = text.splitlines(False)[0]
        text = "".join(text.splitlines(True)[1:])
        templateFile.close()

        print("now smash your keyboard to generate a random seed")
        seed = getpass()
        if len(seed) > 20:
            print("nice...")
        else:
            print("you can do better")

        print("with your seed, choosing a partner")
        partnerChooser = PartnerChooser(list(wishes.keys()), seed)

        if not partnerChooser.IsSuccessful():
            print("could not assign all persons with a different partner. Try another seed.")
            return

        textArgs = {}
        for name in emails.keys():
            partner = partnerChooser.GetPartner(name)
            textArgs[emails[name]] = EmailSender.TextArgs((name, partner, wishes[partner]))

        EmailSender(subject, text, textArgs, emailaddress=emailaddress, password=password, doNotDeleteSentMails=doNotDeleteSentMails, test=test)

def printHelp():
    help(main)

def main(argv):
    """Secret Santa partner chooser and email sender
    this script will shuffle a list of names to provide each person with a partner and send
    emails out to inform the person which partner was assigned (and an optional wish)
    Arguments: <path to a csv file> <path to a text file>
    --email=<email address of the sender (gmail only)> --password<password of the email account>
    --keepEmails --test
    positional arguments:
    the first argument is the path to a csv file where all attendees are listed. The first column
    is the email address, the second is the name, and in the third column a wish can be provided
    Example:
    --randymarsh@southpark.com;Randy Marsh;Beer--
    the second argument is the email template. Use the spaceholders {0}, {1} and {2} to provide
    the gaps where the values from the csv are filled in. The first line is used as the subject.
    {0} is the name of the receiver
    {1} is the name of the partner
    {2} is the wish
    Example:
    --Secret Santa--
    --Hello {0}, your secret santa is {1} and wishes for {2}--
    
    keyword arguments:
    --email: optionally provide the email address for a gmail account (use a throwaway account)
    --password: the password for the account
            if no credentials are provided, they can be put in later
    --keepEmails: this keeps the emails in your email account's sent folder, so you can see who
            got who
    --test: use this parameter and the smtp daemon to see the result of your email, without
            actually sending them
    """
    if len(argv) < 3:
        printHelp()
        print("\nnot enough arguments provided, exiting...")
        return

    csvFile = argv[1]
    templateFile = argv[2]
    emailAddress = None
    password = None
    keepEmails = False
    test = False

    try:
        opts, args = getopt.getopt(argv[3:], "h", ["email=", "password=", "keepEmails", "test"])
    except getopt.GetoptError as error:
        printHelp()
        print(error)
        return

    for opt, arg in opts:
        if "--email" == opt:
            emailAddress = arg
        elif "--password" == opt:
            password = arg
        elif "--keepEmails" == opt:
            keepEmails = True
        elif "--test" == opt:
            test = True
        elif "-h" == opt:
            printHelp()
        else:
            print("unknown argument " + arg)

    SecretSanta(csvFile, templateFile, emailaddress=emailAddress, password=password, doNotDeleteSentMails=keepEmails, test=test)

if __name__ == '__main__':
    main(sys.argv)
