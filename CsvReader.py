import re

class CsvReader:
    """reads the content of a comma separated values file"""

    def __init__(self, file):
        try:
            file = open(file, "rt")
            self.content = file.read()
            file.close()

            self.rows = re.split("([\r\n])+", self.content)
        except FileNotFoundError:
            print("could not open " + file)

    def GetRows(self):
        return len(self.rows)

    def GetColumns(self, row=0):
        return len(re.split("[(\".+?\");,]", self.rows[row]))

    def GetCell(self, row, column):
        return re.split("\".+?\"?|;?", self.rows[row])[column]

def test():
    csvtext = "test; 1; 2; 3.14159; moep\n" +\
              "nothertest; lmaa; whatev\r\n" +\
              "\"no; you perv\"; \'this should belong together\'; ; 5\r" +\
              "idk; 1, 2, 3"

    file = open("test.csv", "wt")
    file.write(csvtext)
    file.close()

    import csv
    numRow = 0
    numCol = 0
    file = open("test.csv", "rt")
    reader = csv.reader(file, delimiter=";", quotechar="\"")
    for row in reader:
        numCol = 0
        for column in row:
            print("at {0}|{1}: {2}".format(numCol, numRow, column))
            numCol += 1
        numRow += 1

    file.close()

    reader = CsvReader("test.csv")
    rows = reader.GetRows()
    print("rows:", rows)
    for row in range(rows):
        cols = reader.GetColumns(row)
        print("cols:", cols)
        for col in range(cols):
            print("at {0}|{1}: {2}".format(col, row, reader.GetCell(row, col)))


if __name__ == "__main__":
    test()
