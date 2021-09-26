import random

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
            names_dup = names
            for name in names:
            
                if names_dup.count(name) > 0:
                    names_dup2 = names_dup[0:names_dup.index(name)] + names_dup[names_dup.index(name) + 1:]
                else:
                    names_dup2 = names_dup.copy()
            
                maxIndex = len(names_dup2) - 1
                if (maxIndex < 0):
                    # indicator that the last name was removed from names_dup2, which means the last person is paired with itself
                    # -> stop this loop and begin again
                    isValid = False
                    self.pairs.clear()
                    break
                elif (maxIndex < 1):
                    randomIndex = 0
                    isValid = True
                else:
                    randomIndex = random.randrange(0, maxIndex, 1)

                partner = names_dup2[randomIndex]
                self.pairs.append((name, partner))
                names_dup = names_dup[0:names_dup.index(partner)] + names_dup[names_dup.index(partner) + 1:]

    def IsSuccessful(self):
        return self.successful

    def GetPartner(self, name):
        for pair in self.pairs:
            if pair[0] == name:
                return pair[1]
        return "Did not find your name, check your spelling"


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

        print("\nTest if name randomizer returns the same results for the same seed")
        for i in range(1000):
            partnerChooser = PartnerChooser(names, seed)
            if not partnerChooser.IsSuccessful():
                print("Failed, NameRandomizer was not successful after {0} tries".format(i+1))
                return
            for index in range(len(names)):
                if not partners[index] == partnerChooser.GetPartner(names[index]):
                    print("Failed, NameRandomizer returned different partner after {0} tries".format(i+1))
                    return
        print("Passed")

    else:
        print("Failed, nameRandomizer was not successful with the given seed")

if __name__ == '__main__':
    test()



