P1.py is the file which has the "main" function of the project
    - Read the input from the stdin
    - Split the input String and generate all the data structures
    - Stem
    - generate the chart of the algorithm
    - output the chart
Util.py contains a class which is used to deal with the input string
    - separate the grammar and the input string
    - split the grammar
    - split the input String and merge the multipule lines
    - get the base form of the word
    - get the part-of-speech of the words
myChart.py is a class which represent the chart of the Earley Parsing Algorithm
    - the list named states has all the state in the specific chart
    - output method can output the states in the chart
myState.py is a class which represent the state in the chart
    - rule is a piece of grammar rule
    - positiion is the dot position
    - start is the parse begin
    - end is the parse end
myRule.py is a class of a piece of grammar rule
    - source is a NonTerminal
    - dest is a list of Terminal or another Terminal
myGlobal.py contains all the global variables
   
