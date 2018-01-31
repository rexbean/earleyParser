class MyChart:
    def __init__(self,index):
        self.index = index
        self.states = []

    def addState(self, state):
        self.states.append(state)

    def myOutput(self, index):
        string = ''
        for state in self.states:
            string += state.toString()+'\n'
        return string[0:-1]
