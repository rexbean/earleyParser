class State:
    def __init__(self, rule, start, end):
        self.rule = rule
        self.start = start
        self.end = end
        self.position = 0
        self.operator = ''

    def hasFinished(self):
        return self.position == len(self.rule.dest)

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getNextToken(self):
        return self.rule.dest[self.position]

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def setOperator(self, operator):
        self.operator = operator

    def destToString(self):
        result = ''
        index = 0
        for d in self.rule.getDest():
            if(index == self.position):
                result += '.'
            result += d
            if(index != self.position - 1):
                result += ' '
            index+=1
        if(self.position == index):
            result += '.'
        return result
    def toString(self):
        string = '{:<25}'.format(self.rule.getSource()+"->"+self.destToString())\
        +'['+str(self.start)+','+str(self.end)+']'+'{:>20}'.format(self.operator)
        return string
