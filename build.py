import csv
from collections import Counter

class builder:

    def startBuild(self, path, binsNum):
        global averageDict
        global structureData
        global trainData
        global fields
        global minValues
        global maxValues
        global bins

        averageDict = {}
        minValues = {}
        maxValues = {}
        structureData = ''
        fields = []
        trainData = []
        bins = []

        #Read the structure file
        with open(path+"\\Structure.txt", "r") as structure:
            structureData = structure.read()

        #Read the train file and insert the data to 2 arrays:
        #1. Fields
        #2. trainData
        with open(path+"\\train.csv",'r') as train:
            csvTrainData = csv.reader(train)
            fields = csvTrainData.next()
            for row in csvTrainData:
                trainData.append(row)

        #Check if the field is numeric or not to find average or common
        structureData = structureData.split("\n")
        for line in structureData:
            splitBySpaceLine = line.split(" ")
            if splitBySpaceLine[2] == "NUMERIC":
                self.average(splitBySpaceLine[1])
            else:
                self.common(splitBySpaceLine[1])

        #Fill empty fields with average or most common as needed
        for line in trainData:
            for i in range(0, len(line)):
                if line[i] == "":
                    line[i] = averageDict[str(i)]

        #CALL THE DISCRETIZATION FUNCTION FOR EACH NUMERIC FIELD
        for line in structureData:
            splitBySpaceLine = line.split(" ")
            if splitBySpaceLine[2] == "NUMERIC":
                self.binner(splitBySpaceLine[1], binsNum)

        return trainData


    #make the discretization for numeric fields
    def binner(self, className, binsNum):
        global averageDict
        global structureData
        global trainData
        global fields
        global minValues
        global maxValues
        global bins

        #find the size of each bin
        size = (maxValues[className] - minValues[className])/binsNum
        for i in range(0, binsNum):
            bins.append(minValues[className] + (size*(i+1)))

        colNumber = 0
        for field in fields:
            if field == className:
                break
            colNumber = colNumber + 1

        #seperate to bins
        for row in trainData:
            num = float(row[colNumber])
            for i in range(0, len(bins)):
                if num <= bins[i]:
                    row[colNumber] = str(i+1)
                    break


    #calculate the average of the class
    def average(self, className):
        global averageDict
        global structureData
        global trainData
        global fields
        global minValues
        global maxValues

        colNumber = 0
        for field in fields:
            if field == className:
                break
            colNumber = colNumber + 1
        allCol = []
        for line in trainData:
            if (line[colNumber] != ""):
                allCol.append(float(line[colNumber]))
        averageDict[str(colNumber)] = sum(allCol) / len(allCol)
        minValues[className] = min(allCol)
        maxValues[className] = max(allCol)


    #Find the most common field of the class
    def common(self, className):
        global averageDict
        global structureData
        global trainData
        global fields

        colNumber = 0
        for field in fields:
            if field == className:
                break
            colNumber = colNumber + 1

        allCol = []
        for line in trainData:
            if(line[colNumber] != ""):
                allCol.append(line[colNumber])

        occurence_count = Counter(allCol)
        averageDict[str(colNumber)] = occurence_count.most_common(1)[0][0]




