import os, sys

mainFile = sys.argv[1]

# strip out the empty lines and comments 
def clean_line(line): 
    for line in mainFile : 
        currentLine = cleanLine(line) ## removes all whitespace and comments from the line 

def cleanLine(line): 
    currentChar = line[0]
    if currentChar == '/' or currentChar == '\n':
        return ''
    elif currentChar == ' ':
        return cleanLine(line[1:])
    else:
        return line