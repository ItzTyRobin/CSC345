import sys

nextVariableAddress = 16

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

    with open(inputFile, "r") as asm:
        cleaned = []
        for line in asm:
            newLine = cleanLine(line)
            if newLine != "":
                cleaned.append(newLine)

    symbolTable = createSymbolTable(cleaned) 
    binaryLines = createBinaryLines(cleaned, symbolTable) 

    with open(outputFile, "w") as hack:
        for line in binaryLines:
            hack.write("\n".join(binaryLines))

    # read the file
    print("The current input is in:", inputFile)
    print("The current output is in:", outputFile)


def cleanLine(line):
    # remove comments and in-line comments
    line = line.split("//")[0]

    # remove whitespace
    line = line.strip()

    # ignore empty lines
    if line == "":
        return ""

    return line


def decideAorC(line, symbolTable):
    line = line.strip()
    if line == "":
        return ""

    if line.startswith("(") and line.endswith(")"):
        return ""

    if line.startswith("@"):
        return createAInstruction(line, symbolTable)
    else:
        return createCInstruction(line)


def createAInstruction(line, symbolTable):
    global nextVariableAddress
    number = line[1:]

    # @number
    if number.isdigit():
        value = int(number)
        return "0" + format(value, "015b")

    # @symbol
    if number not in symbolTable:
        symbolTable[number] = nextVariableAddress
        nextVariableAddress += 1

    return "0" + format(symbolTable[number], "015b")


dest_table = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

jump_table = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

comp_table = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}


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


table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}


def createSymbolTable(lines):
    romAddress = 0
    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            symbol = line[1:-1]
            if symbol not in table:
                table[symbol] = romAddress
        else:
            romAddress += 1

    return table


def createBinaryLines(lines, symbolTable):
    binaryLines = []

    for line in lines:
        binary = decideAorC(line, symbolTable)
        if binary != "":
            binaryLines.append(binary)

    return binaryLines


main()
