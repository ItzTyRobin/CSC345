"""
takes .jack files and turns them into XML files with the correct syntax for the Jack language
"""

import sys

from Tokenizer import Tokenizer, tokenType
from Compilation import Compilation

# 1. creates a tokenizer from the Xxx.jack file input file
# 2. creates an output file called Xxx.xml
# 3. uses the Tokenizer and Compilation to parse the input file and write the correct XML syntax to the output file

def main():
    inputFile = open('Main.jack', 'r')
    outputFile = open('Main.xml', 'w')
    compilationEngine = Compilation(Tokenizer(inputFile), outputFile)
    compilationEngine.compileClass()
    inputFile.close()
    outputFile.close()

if __name__ == '__main__':
    import os
    path = sys.argv[1]

    if os.path.isdir(path):
        jackFiles = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jack')]
    else:
        jackFiles = [path]

    outputDirectory = os.path.join(path if os.path.isdir(path) else os.path.dirname(path), 'output')
    os.makedirs(outputDirectory, exist_ok=True)

    for jackFile in jackFiles:
        baseName = os.path.basename(jackFile).replace('.jack', '')

        # Generate tokenizer output (XxxT.xml)
        tokenXmlFile = os.path.join(outputDirectory, baseName + 'T.xml')
        with open(jackFile, 'r') as inputFile:
            tokenizer = Tokenizer(inputFile)
        with open(tokenXmlFile, 'w') as tokenOutput:
            tokenOutput.write('<tokens>\n')
            for t in tokenizer.tokens:
                if t.type == tokenType.KEYWORD:
                    tokenOutput.write('<keyword> ' + t.value + ' </keyword>\n')
                elif t.type == tokenType.SYMBOL:
                    tokenOutput.write('<symbol> ' + t.value + ' </symbol>\n')
                elif t.type == tokenType.IDENTIFIER:
                    tokenOutput.write('<identifier> ' + t.value + ' </identifier>\n')
                elif t.type == tokenType.INT_CONST:
                    tokenOutput.write('<integerConstant> ' + str(t.value) + ' </integerConstant>\n')
                elif t.type == tokenType.STRING_CONST:
                    tokenOutput.write('<stringConstant> ' + t.value + ' </stringConstant>\n')
            tokenOutput.write('</tokens>\n')

        # Generate parser output (Xxx.xml)
        xmlFile = os.path.join(outputDirectory, baseName + '.xml')
        with open(jackFile, 'r') as inputFile:
            outputFile = open(xmlFile, 'w')
            compilation = Compilation(Tokenizer(inputFile), outputFile)
            compilation.compileClass()
            outputFile.close()



        




