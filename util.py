import sys
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re
import myGlobal
import operator
from myRule import Rule
class Util(object):

    def __init__(self):
        pass

    def readFromStdin(self):
        for line in sys.stdin:
            # remove the \r\t\n
            line = line.replace('\r','').replace('\t','').replace('\n','')
            line = line.strip()
            # ignore the comment
            if line.startswith('#'):
                continue
            if line == '':
                continue
            myGlobal.inputList.append(line)

    def splitInput(self):
        inputList = myGlobal.inputList
        isInputStr = False
        isStart = True
        prevSource = ' '
        # input
        for myInput in inputList:
            # separate grammar and input str
            if not isInputStr:
                isInputStr = self.judgeInput(myInput)
                if not isInputStr:
                    prevSource = self.splitGrammar(prevSource, myInput)
                    continue

            splitedList = self.splitInputStr(myInput)
            # if the input string has multiple line, they should be merge together
            self.mergeInputStr(isStart, splitedList)
            isStart = False
        self.setIsExtended()
        inputTokenList = myGlobal.inputText.strip().split(' ')

        for token in inputTokenList:
            base = self.getBaseForm(token)
            myGlobal.baseDict[token] = base

        for token in inputTokenList:
            try:
                token = myGlobal.baseDict[token]
                myGlobal.inputTokenList.append(token)
            except:
                return False

    def judgeInput(self, myInput):
        iToken = 0
        if(myInput[iToken] == 'W' or myInput[iToken] == 'w'):
            iToken += 1
            while(myInput[iToken] == ' '):
                iToken += 1
            if(myInput[iToken] == '='):
                return True
            return False
        else:
            return False

    def mergeInputStr(self, isStart, splitedList):
        # start
        start = 2 if isStart else 0
        # get end when end with '-'
        isUnCompleted = self.isUnCompleted(splitedList[-1])
        end = len(splitedList) - 1 if isUnCompleted else len(splitedList)
        # merge
        self.mergeStr(start, end, isUnCompleted, splitedList)

    def isUnCompleted(self, charactor):
        if(charactor == '-'):
            return True
        else:
            return False

    def mergeStr(self, start, end, isUnCompleted, splitedList):
        while(start < end):
            # remove the punctuation in the senctence
            if(splitedList[start] == '.' or splitedList[start] == ';'
            or splitedList[start] == ':' or splitedList[start] == '|'
            or splitedList[start] == '=' or splitedList[start] == '?'):
                start += 1
                continue
            # when the sentence is uncompleted then do not add space
            # at the end of the of the line
            if isUnCompleted and start == end - 1:
                myGlobal.inputText += splitedList[start]
            else:
                myGlobal.inputText += splitedList[start]+' '
            start += 1
        # myGlobal.inputText = myGlobal.inputText.lower()
    def splitInputStr(self, myInput):
        tokenList = []
        equalList = myInput.split('=', 1)
        iEqual = 0
        lenEqual = len(equalList)
        if(lenEqual <= 0):
            return
        if(lenEqual == 1):
            startIndex = 0
        else:
            startIndex = 1
            tokenList.append('W')
            tokenList.append('=')
        spaceList = equalList[startIndex].strip().split(' ')
        iSpace = 0
        lenSpace = len(spaceList)
        while(iSpace < lenSpace):
            if(spaceList[iSpace] == ''):
                iSpace += 1
                continue
            # at the end of the line
            matchObj = re.search('[a-zA-Z]+([\.\-\?])$',spaceList[iSpace])
            if matchObj:
                tokenList.append(spaceList[iSpace][0:-1])
                tokenList.append(matchObj.group(1))
            else:
                tokenList.append(spaceList[iSpace])
            iSpace += 1
        myGlobal.inputStrTokenList.append(tokenList)
        return tokenList


    def splitGrammar(self, prevSource, myInput):
        tokenList = []
        source = ''
        source = self.splitColon(myInput, prevSource, tokenList)
        myGlobal.grammarTokenList.append(tokenList)
        return source

    def splitColon(self, myInput, prevSource, tokenList):
        # split by colon
        source = ''
        colonList = myInput.split(':', 1)
        lenColon = len(colonList)
        # myInput does not have ':', like '|' & ';'
        if(lenColon <= 0):
            return
        elif(lenColon == 1):
            startColon = 0
            source = prevSource
        else:
            startColon = 1
            # the token before ':' is source
            source = colonList[0].strip()
            # add initi Rule
            if(len(myGlobal.ruleList) == 0):
                myGlobal.startNT = source
            self.setTypeMap(source)
            # add to token list
            tokenList.append(source)
            tokenList.append(':')
        while(startColon < lenColon):
            myStr = colonList[startColon]
            self.splitOr(myStr, source, tokenList)
            startColon += 1
        return source


    def splitOr(self, myStr, source, tokenList):
        # split by '|'
        orList = myStr.split('|')
        lenOr = len(orList)
        iOr = 0
        while(iOr < lenOr):
            # split by ' '
            # add the source of the Rule
            rule = Rule()
            rule.setSource(source)
            # if it start with '|',# it has the same source as the previous one
            if(orList[iOr] == ''):
                tokenList.append("|")
                iOr+=1
                continue
            toAdd = self.splitSpace(orList, iOr, tokenList, rule)
            iOr += 1
            # not the last one
            if(iOr != lenOr):
                tokenList.append('|')
            if len(rule.dest) != 0:
                myGlobal.ruleList.append(rule)

    def splitSpace(self, orList, iOr, tokenList, rule):
        spaceList = orList[iOr].strip().split(' ')
        base = ''
        for myStr in spaceList:
            myStr = myStr.strip()
            # last charactor not ';'
            if(myStr[-1] != ';'):
                # a part of the dest
                dest = myStr
                # add the word to the word map
                self.setWordMap(dest,rule.getSource())
                # add to token list
                tokenList.append(dest)
                # add the dest to the rule
                rule.addDest(dest)
            else:
                # only have ';'
                # no dest
                if(len(myStr) == 1):
                    tokenList.append(';')
                else:
                    # a part of dest with ';'
                    dest = myStr[0:-1].strip()
                    # add to the token list
                    tokenList.append(dest)
                    tokenList.append(';')
                    # add the word to the word map
                    self.setWordMap(dest, rule.getSource())
                    # add dest to the rule
                    rule.addDest(dest)

    def setIsExtended(self):
        typeDict = myGlobal.typeDict
        for rule in myGlobal.ruleList:
            for dest in rule.getDest():
                if dest in typeDict:
                    rule.isExtended &= True
                else:
                    rule.isExtended &= False
        for rule in myGlobal.ruleList:
            if rule.isExtended:
                myGlobal.extendDict[rule.getSource()] = True
            else:
                myGlobal.extendDict[rule.getSource()] = False


    def stemmerOutput(self, tokenList,isGrammar):
        for tokens in tokenList:
            lineNumber = myGlobal.lineNumber
            for token in tokens:
                myType = self.getType(token)
                self.myOutput(isGrammar, lineNumber, token, myType)
            myGlobal.lineNumber += 1

    def getType(self, token):
        if self.isInteger(token):
            return 'INTEGER'
        if self.isDouble(token):
            return 'DOUBLE'
        if self.isString(token):
            return 'STRING'
        if self.isOP(token):
            return 'OP'

    def myOutput(self, isGrammar, lineNumber, token, myType):
        tab = self.getTab(token)
        base = ''
        if not isGrammar:
            if token in myGlobal.baseDict:
                base = myGlobal.baseDict[token]
            else:
                base = token
            # base = self.getBaseForm(token)
            if operator.eq(base,token):
                base = ''
        print(token+tab + myType + '\t' + str(lineNumber) + '\t'+base )


    def getBaseForm(self,token):
        baseList = []
        baseForm = ''
        token = token.lower()
        baseForm = self.getBaseFormNLTK(token, 'n')
        # print(baseForm)
        if (baseForm != ''):
            return baseForm

        baseForm = self.getBaseFormNLTK(token, 'v')
        if (baseForm != ''):
            return baseForm

        baseForm = self.getBaseFormNLTK(token, 'a')
        if (baseForm != ''):
            return baseForm
        return token

    def getBaseFormNLTK(self, token, pos):
        baseForm = ''
        baseList = wn._morphy(token, pos)
        if len(baseList) != 0:
            for base in baseList:
                if base in myGlobal.wordDict:
                    baseForm = base
        return baseForm


    def setTypeMap(self, source):
        # POS
        if self.isPOS(source):
            myGlobal.typeDict[source] = 'POS'
            return
        # noneTereminal
        if self.isNT(source):
            myGlobal.typeDict[source] = 'NT'
            return

    def setWordMap(self, dest, source):
        if self.isT(dest):
            if dest in myGlobal.wordDict:
                POSList = myGlobal.wordDict[dest]
            else:
                POSList = []
            POSList.append(source)
            myGlobal.wordDict[dest] = POSList

    def getTab(self, token):
        if(len(token) < 8):
            return '\t\t'
        else:
            return '\t'

    def isInteger(self, token):
        matchObj = re.match('^\d+$', token)
        if matchObj:
            return True
        else:
            return False

    def isDouble(self, token):
        matchObj = re.match('^\d*\.\d+$',token)
        if matchObj:
            return True
        else:
            return False

    def isString(self, token):
        matchObj = re.match('^[a-zA-Z]+([\.\'\-][a-zA-Z]+)?$', token)
        if matchObj:
            return True
        else:
            return False

    def isOP(self,token):
        matchObj = re.match('[:\'\"\-|;=\.\?]',token)
        if matchObj:
            return True
        else:
            return False

    def isPOS(self,token):
        matchObj = re.match('[A-Z][a-z]+',token)
        if matchObj:
            return True
        else:
            return False

    def isNT(self,token):
        matchObj = re.match('[A-Z]+$',token)
        if matchObj:
            return True
        else:
            return False

    def isT(self,token):
        matchObj = re.match('[a-z\d]+|(^\d*\.\d+)$',token)
        if matchObj:
            return True
        else:
            return False
