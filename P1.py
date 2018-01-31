from util import Util
from myChart import MyChart
from myRule import Rule
from myState import State
import myGlobal
import queue

def generateChart():
    typeDict = myGlobal.typeDict
    extendDict = myGlobal.extendDict
    firstChart = MyChart(0)
    # add initial rule

    rule = Rule()
    rule.setSource('gammar')
    typeDict['gammar'] = ['symbol']
    rule.addDest(myGlobal.startNT)
    initialState = State(rule, 0, 0)
    initialState.operator = 'Dummy start state'
    firstChart.addState(initialState)

    myGlobal.chartList.append(firstChart)

    lenInput = len(myGlobal.inputTokenList)
    if lenInput == 0 or (lenInput == 1 and myGlobal.inputTokenList[0] == ''):
        print("No input")
        return False
    for i in range(0, lenInput+1):
        if(len(myGlobal.chartList) <= i):
            chart = MyChart(i)
            myGlobal.chartList.append(chart)
        else:
            chart = myGlobal.chartList[i]
        index = 0
        for state in chart.states:
            if state.hasFinished() == False \
            and extendDict[state.getNextToken()] == True:
                predict(state, i)
            elif state.hasFinished() == False \
            and extendDict[state.getNextToken()] == False:
                if scanner(state,i):
                    break

            else:
                complete(state)
    return True
def predict(state, index):
    # print('predict')
    ruleList = myGlobal.ruleList
    for rule in ruleList:
        if(state.getNextToken() == rule.getSource()):
            s = State(rule, index, index)
            s.operator = 'Predictor'
            addToChart(s, index)

def scanner(state, index):
    if index >= len(myGlobal.inputTokenList):
        return False
    # print('scanner')
    word = myGlobal.inputTokenList[index]
    wordDict = myGlobal.wordDict
    POS = state.getNextToken()
    if word not in wordDict:
        print('lack of words in grammar')
        return
    if POS in wordDict[word]:
        rule = Rule()
        rule.setSource(POS)
        rule.addDest(word)
        state = State(rule, index, index + 1)
        state.operator = 'Scannner'
        state.position += 1
        addToChart(state, index+1)
        return True

def complete(state):
    # print('completer')
    start = state.getStart()
    end = state.getEnd()
    for s in myGlobal.chartList[start].states:
        if(s.end == start):
            if(s.hasFinished() == False \
            and s.getNextToken() == state.rule.getSource()):
                rule = Rule()
                if(s.rule.getSource() == 'gammar'):
                    continue
                rule.setSource(s.rule.getSource())
                rule.dest = s.rule.getDest().copy()
                newState = State(rule, s.start, end)
                newState.operator = 'Completer'
                newState.position = s.getPosition() + 1
                addToChart(newState, end)


def addToChart(state, index):
    duplicate = False
    if(len(myGlobal.chartList) <= index):
        chart = MyChart(index)
        myGlobal.chartList.append(chart)
    else:
        chart = myGlobal.chartList[index]
    for s in chart.states:
        if state.rule == s.rule:
            duplicate = True
    if not duplicate :
        chart.addState(state)


def myOutput():
    #output
    # for g in myGlobal.grammarTokenList:
    #     print(g)
    # print('input')
    # for i in myGlobal.inputStrTokenList:
    #     print(i)
    #
    # print(myGlobal.inputTokenList)
    # print(myGlobal.inputText)
    # print(len(myGlobal.ruleList))
    # for rule in myGlobal.ruleList:
    #     rule.toString()
    #
    # print(len(myGlobal.typeDict))
    # print(myGlobal.typeDict)
    # print(len(myGlobal.wordDict))
    # print(myGlobal.wordDict)
    i=0
    for chart in myGlobal.chartList:
        print('chart'+ str(i))
        print('---------------------------------------------------------------')
        print(chart.myOutput(i))
        print()
        i+=1
    #print(myGlobal.chartList[0].myOutput())


if __name__ == '__main__':

    util = Util()
    util.readFromStdin()
    util.splitInput()
    result = generateChart()
    if result:
        util.stemmerOutput(myGlobal.grammarTokenList,True)
        util.stemmerOutput(myGlobal.inputStrTokenList,False)
        print('ENDFILE')
        myOutput()
