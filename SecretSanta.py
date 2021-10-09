import csv
from getpass import getpass

from PartnerChooser import PartnerChooser
from EmailSender import EmailSender

class SecretSanta:

    def __init__(self, wishlist):

        csvFile = open(wishlist)
        csvReader = csv.reader(csvFile, delimiter=";", quotechar="\"")

        emails = {}
        wishes = {}
        for row in csvReader:
            if len(row) < 2:
                raise Exception("in the csv file, at least the email address and the name is expected, actual: " *row)

            emails[row[1]] = row[0]
            if len(row) > 2:
                wishes[row[1]] = row[2]
            else:
                wishes[row[1]] = "nichts besonderes"

        print("now smash your keyboard to generate a random seed")
        seed = getpass()
        if len(seed) > 20:
            print("nice...")
        else:
            print("you can do better")

        print("with your seed, choosing a partner")
        partnerChooser = PartnerChooser(list(wishes.keys()), seed)

        text = "Hallo {0}\nDein zu Beschenkender heißt {1} und wünscht sich {2}\n"
        textArgs = {}
        for name in emails.keys():
            partner = partnerChooser.GetPartner(name)
            textArgs[emails[name]] = EmailSender.TextArgs((name, partner, wishes[partner]))

        EmailSender("Wichteln", text, textArgs, *list(emails.values()))

def test():
    SecretSanta("test3.csv")

if __name__ == "__main__":
    test()
