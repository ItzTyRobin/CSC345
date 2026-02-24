import sys
global inputFile
# global binaryLine

# To run:
# cd project-06/assembler
# python assembler.py ../tests/Add.asm
# ^^ should add the Add.hack file to the /tests folder

def main():
   if len(sys.argv) > 1:
       inputFile = sys.argv[1]
   else:
       inputFile = "../tests/Prog.asm"

   outputFile = inputFile.replace(".asm", ".hack")

   with open(inputFile, "r") as asm, open(outputFile, "w") as hack:
       for line in asm:
           # step 1: clean the file
           # just removes any comments in the .asm file and then writes to the .hack file 
           lines = cleanLine(line)
           lines = decideAorC(lines) 
           hack.write(lines)
  
   # read the file
   print("The current input is in:", inputFile)
   print("The current output is in:", outputFile)

#    # step 2: create the symbol table
#    symbolTable = createSymbolTable(lines)



# -----------------------------
# step 1: clean the file
# -----------------------------
def cleanLine(line):
    # remove comments and in-line comments 
    line = line.split("//")[0]

    # remove whitespace 
    line = line.strip()

    #ignore empty lines 
    if line == "":
        return ""
    
    return line + "\n"

# def decideAorC(lines): 
#     binaryLine = ""
#     for line in lines:
#         if line.startswith('@'):
#          # this is an A-instruction
#             binaryLine = createAInstruction(line, )
#         else:
#         # this is a C-instruction
#             binaryLine = createCInstruction(line)
#     return binaryLine

def decideAorC(line):
    line = line.strip() 
    if line == "":
        return ""

    if line.startswith("@"):
        return createAInstruction(line) + "\n"
    else:
        return createCInstruction(line) + "\n"

def createAInstruction(line):
    number = line[1:] 
    if not number.isdigit():
        raise ValueError(f"Milestone 1 only supports numeric A-instructions, got: {line}")

    value = int(number)
    if value < 0 or value > 32767:
        raise ValueError(f"A-instruction out of range (0..32767): {line}")

    return "0" + format(value, "015b")

dest_table = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
}

jump_table = {
    "":     "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111",
}

comp_table = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}



#    # step 3: convert the assembly code to binary machine code 
#    binaryLines = createBinaryLines(lines, symbolTable)

#    # step 4: write the binary machine code to a .hack file
#    writeToHackFile(binaryLines, outputFile)

# -----------------------------
# step 2: create the symbol table
# -----------------------------
def createSymbolTable(lines):
   """
   we want to create a symbol table that maps the
   symbols in the assembly code to their corresponding
   addresses in the machine code.
   """
    
  
def createCInstruction(line):
    destSymbol = ""
    compSymbol = ""
    jumpSymbol = ""

    if "=" in line:
        destSymbol, rest = line.split("=")
    else:
        rest = line

    if ";" in rest:
        compSymbol, jumpSymbol = rest.split(";")
    else:
        compSymbol = rest
        jumpSymbol = ""
        
    destSymbol = destSymbol.strip()
    compSymbol = compSymbol.strip()
    jumpSymbol = jumpSymbol.strip()

    dest_bits = dest_table[destSymbol]
    comp_bits = comp_table[compSymbol]
    jump_bits = jump_table[jumpSymbol]

    # build full C-instruction
    binary = "111" + comp_bits + dest_bits + jump_bits
    return binary


main()