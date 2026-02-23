import os
import sys


global inputFile


# To run:
# cd project-06/assembler
# python assembler.py ../tests/Add.asm
# ^^ should add the Add.hack file to the /tests folder


def main():
   """
   we hopefully want the user to enter something like: python assembler.py Add.asm
   which python converts into: sys.argv == ["assembler.py", "Add.asm"]
   so we want to check if the sys.argv list is greter then 1 because that means
   there is an extra argument after the name of the script, which should be the
   name of the file we want to assemble.
   """


   if len(sys.argv) > 1:
       inputFile = sys.argv[1]
   else:
       inputFile = "../tests/Prog.asm"


   outputFile = inputFile.replace(".asm", ".hack")


   with open(inputFile, "r") as asm, open(outputFile, "w") as hack:
       for line in asm:
           hack.write(line)
  
   # read the file
   print("The current input is in:", inputFile)
   print("The current output is in:", outputFile)


   # step 1: clean the file
   lines = cleanLine(inputFile)

   # step 2: create the symbol table
   symbolTable = createSymbolTable(lines)

   # step 3: convert the assembly code to binary machine code 
   binaryLines = createBinaryLines(lines, symbolTable)

   # step 4: write the binary machine code to a .hack file
   writeToHackFile(binaryLines, outputFile)


# -----------------------------
# step 1: clean the file
# -----------------------------

# strip out the empty lines and comments
def cleanLine(line):
   currentChar = line[0]
   if currentChar == '/' or currentChar == '\n':
       return ''
   elif currentChar == ' ':
       return cleanLine(line[1:])
   else:
       return line


# -----------------------------
# step 2: create the symbol table
# -----------------------------
def createSymbolTable(lines):
   """
   we want to create a symbol table that maps the
   symbols in the assembly code to their corresponding
   addresses in the machine code.
   """

# -----------------------------
# step 3: convert the assembly code to binary machine code 
# -----------------------------
def createBinaryLines(lines, symbolTable):
    '''
    we want to: 
    1. ignore labels (LOOP)
    2. decide if it’s:
        - an A-instruction (@something)
        - a C-instruction (dest=comp;jump)
    3. translate it into binary
    4. collect the binary lines into a list and return it
    '''
  
# -----------------------------
# step 4: write the binary machine code to a .hack file
# ----------------------------- 
def writeToHackFile(binaryLines, outputFile):
    '''
    we want to: 
    1. open (or create) the .hack file
    2. for each binary instruction:
        - write it
        - add a newline
    3. close the file
    '''
    
main()