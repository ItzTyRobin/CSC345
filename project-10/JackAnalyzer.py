import sys
import os

from JackTokenizer import Tokenizer, tokenType
from CompilationEngine import Compilation

def fixSpecialChars(value):
    value = value.replace('&', '&amp;')
    value = value.replace('<', '&lt;')
    value = value.replace('>', '&gt;')
    return value

def writeTokens(tokenizer, outFile):
    outFile.write('<tokens>\n')
    for t in tokenizer.tokens:
        if t.type == tokenType.keyWord:
            outFile.write('<keyword> ' + t.value + ' </keyword>\n')
        elif t.type == tokenType.symbol:
            outFile.write('<symbol> ' + fixSpecialChars(t.value) + ' </symbol>\n')
        elif t.type == tokenType.identifier:
            outFile.write('<identifier> ' + t.value + ' </identifier>\n')
        elif t.type == tokenType.intConst:
            outFile.write('<integerConstant> ' + str(t.value) + ' </integerConstant>\n')
        elif t.type == tokenType.stringConst:
            outFile.write('<stringConstant> ' + t.value + ' </stringConstant>\n')
    outFile.write('</tokens>\n')

path = sys.argv[1]

# get all .jack files
if os.path.isdir(path):
    jackFiles = []
    for f in os.listdir(path):
        if f.endswith('.jack'):
            jackFiles.append(os.path.join(path, f))
else:
    jackFiles = [path]
    
    
    
if os.path.isdir(path):
    outDirectory = os.path.join(path, 'output')
else:
    outDirectory = os.path.join(os.path.dirname(path), 'output')
os.makedirs(outDirectory, exist_ok=True)

for jackFile in jackFiles:
    name = os.path.basename(jackFile).replace('.jack', '')

    # tokenizer output
    with open(jackFile, 'r') as f:
        tokenizer = Tokenizer(f)
    with open(os.path.join(outDirectory, name + 'T.xml'), 'w') as f:
        writeTokens(tokenizer, f)

    # parser output
    with open(jackFile, 'r') as f:
        tokenizer = Tokenizer(f)
    with open(os.path.join(outDirectory, name + '.xml'), 'w') as f:
        Compilation(tokenizer, f).compileClass()
    
