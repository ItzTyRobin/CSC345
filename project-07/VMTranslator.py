import sys

def main(): 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
    else:
        inputFile = "SimpleAdd/SimpleAdd.vm"       # default test
        
    outputFile = inputFile.replace(".vm", ".asm")
    
    with open(inputFile, "r") as vm:
        cleaned = []
        for line in vm:
            newLine = cleanLine(line)
            if newLine != "":
                cleaned.append(newLine)
                
    asmLines = []
    for line in cleaned:
        # decide if its an arthemtic command 
        # (add, sub, neg, eq, gt, lt, and, or, not) or a memory 
        # access command (push/pop segment index)
        
        commandParts = line.split(" ")
        if len(commandParts) == 1: # -> all arthemtic command lines are only one word
            op = commandParts[0]
            asmLines.append(translateArithmetic(op))
        
        elif len(commandParts) == 3: # -> all memory access command lines are three words in the form of "action segment index"
            action = commandParts[0]
            segment = commandParts[1]
            index = commandParts[2]
            asmLines.append(translateMemoryAccess(action, segment, index))
            
        else: 
            print("Error: unrecognized command format:", line)
            

    with open(outputFile, "w") as asm:
        asm.write("\n".join(asmLines))
        
    print("Input file:", inputFile)
    print("Output file:", outputFile)
            
def cleanLine(line):
    # remove comments and in-line comments
    line = line.split("//")[0]

    # remove whitespace
    line = line.strip()

    # ignore empty lines
    if line == "":
        return ""

    return line
    
def translateArithmetic(op):
    # TODO - implement translation of arithmetic commands
    asm = []

    if op == "add":
        asm += [
            "@SP",
            "AM=M-1",   # SP--, A=SP
            "D=M",      # D = y
            "@SP",
            "AM=M-1",   # SP--, A=SP
            "M=M+D",    # x = x + y
            "@SP",
            "M=M+1"     # SP++
        ]

    elif op == "sub":
        asm += [
            "@SP",
            "AM=M-1",
            "D=M",      # D = y
            "@SP",
            "AM=M-1",
            "M=M-D",    # x = x - y
            "@SP",
            "M=M+1"
        ]

    elif op == "neg":
        asm += [
            "@SP",
            "AM=M-1",
            "M=-M",     # y = -y
            "@SP",
            "M=M+1"
        ]

    elif op == "and":
        asm += [
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "AM=M-1",
            "M=M&D",
            "@SP",
            "M=M+1"
        ]

    elif op == "or":
        asm += [
            "@SP",
            "AM=M-1",
            "D=M",
            "@SP",
            "AM=M-1",
            "M=M|D",
            "@SP",
            "M=M+1"
        ]

    elif op == "not":
        asm += [
            "@SP",
            "AM=M-1",
            "M=!M",
            "@SP",
            "M=M+1"
        ]

        return "\n".join(asm)
    
def translateMemoryAccess(action, segment, index): 
    # TODO - implement translation of memory access commands (push/pop)
    asm = []
    if action == "push":
        if segment == "constant":
            asm += [
                f"@{index}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]
        else:
            # TODO - handle other segments (local, argument, this, that, temp, pointer, static)
            pass

    elif action == "pop":
        # TODO - implement pop command translation
        pass



    