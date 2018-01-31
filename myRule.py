class Rule:
    def __init__(self):
        self.source = ''
        self.dest = []
        self.start = 0
        self.end = 0
        self.isExtended = True

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def addDest(self,dest):
        self.dest.append(dest)

    def getDest(self):
        return self.dest

    def destToString(self):
        result = ''
        index = 0
        for d in self.dest:
            result += d
            result += ' '
            index+=1
        return result
    def toString(self):
        string = self.source+"->"+self.destToString() + str(self.isExtended)
        print(string)
