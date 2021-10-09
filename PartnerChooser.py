import random
from time import time

class PartnerChooser:

    def __init__(self, names, seed):
        self.pairs = []
        self.successful = True
        random.seed(seed)

        numberOfLoops = 0   # loop counter. If this reaches 100, the seed given is not usable
        isValid = False
        while not isValid:
            numberOfLoops += 1
            if numberOfLoops > 100:
                self.successful = False
                break

            partners = names
            for name in names:
                # remove the name from the partner list and make a duplicate
                if partners.count(name) > 0:
                    partners_dup = partners[0:partners.index(name)] + partners[partners.index(name) + 1:]
                else:
                    partners_dup = partners.copy()
            
                maxIndex = len(partners_dup) - 1
                if maxIndex < 0:
                    # indicator that the last name was removed from partners_dup, which means the last person is paired with itself
                    # -> stop this loop and begin again
                    isValid = False
                    self.pairs.clear()
                    break
                
                if maxIndex < 1:
                    randomIndex = 0
                    isValid = True
                else:
                    randomIndex = random.randint(0, maxIndex)

                partner = partners_dup[randomIndex]
                self.pairs.append((name, partner))
                # remove the chosen partner from the partner list
                partners = partners[0:partners.index(partner)] + partners[partners.index(partner) + 1:]

    def IsSuccessful(self):
        return self.successful

    def GetPartner(self, name):
        for pair in self.pairs:
            if pair[0] == name:
                return pair[1]
        raise Exception("the given name was not found in the database")


def test():
    names = ["Holt", "Peralta", "Santiago", "Boyle", "Diaz", "Linetti", "Jeffords", "Scully", "Hitchcock"]
    partners = []
    seed = "Brooklyn Nine-Nine"


    print("Test if name randomizer works")  # and put the partners into a list to check them later
    partnerChooser = PartnerChooser(names, seed)
    if partnerChooser.IsSuccessful():
        names_dup = names.copy()
        for name in names:
            partner = partnerChooser.GetPartner(name)
            partners.append(partner)
            print("{0} : {1}".format(name, partner))
            try:
                names_dup.remove(partner)
            except ValueError:
                print("Failed, two people where given the same partner")
                return

        print("Passed")
    else:
        print("Failed, nameRandomizer was not successful with the given seed")

    print("\nTest different seed")
    partnerChooser = PartnerChooser(names, seed + "!")
    if partnerChooser.IsSuccessful():
        machesToLastRun = 0
        for i in range(len(names)):            
            print("{0} : {1}".format(names[i], partnerChooser.GetPartner(names[i])))
            if partners[i] == partnerChooser.GetPartner(names[i]):
                machesToLastRun += 1
        if machesToLastRun > (len(names) / 2):
            print("Failed, the result is too close to the last run")
        else:
            print("Passed")
    else:        
        print("Failed, nameRandomizer was not successful with the given seed")

    print("\nTest assigning partners with only two names")
    names = ["Test1", "Test2"]
    seed = int(time())
    partnerChooser = PartnerChooser(names, seed)
    if not partnerChooser.IsSuccessful():
        print("Failed, two names could not be matched")
    elif (not "Test1" == partnerChooser.GetPartner("Test2")) | (not "Test2" == partnerChooser.GetPartner("Test1")):
        print("Failed, could not assign correct partner")
    else:
        print("Passed")

    print("\nTest the exception")
    try:
        partnerChooser.GetPartner("The Vulture")
        print("Failed, did not throw an exception")
    except:
        print("Passed")

if __name__ == '__main__':
    test()



