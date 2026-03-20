import sys

def translateMemoryAccess(command, segment, index, filename):
    asm = []
    
    segment_map = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT"
    }
    
    if command == "push":
        if segment == "constant":
            asm.append(f"@{index}")
            asm.append("D=A")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M+1")
            
        elif segment in segment_map:
            asm.append(f"@{index}")
            asm.append("D=A")
            asm.append(f"@{segment_map[segment]}")
            asm.append("A=D+M")
            asm.append("D=M")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M+1")
            
        elif segment == "static":
            asm.append(f"@{filename}.{index}")
            asm.append("D=M")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M+1")
            
        elif segment == "temp":
            asm.append(f"@{5 + index}")
            asm.append("D=M")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M+1")
            
        elif segment == "pointer":
            asm.append(f"@{3 + index}")
            asm.append("D=M")
            asm.append("@SP")
            asm.append("A=M")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M+1")
    
    elif command == "pop":
        if segment in segment_map:
            asm.append(f"@{index}")
            asm.append("D=A")
            asm.append(f"@{segment_map[segment]}")
            asm.append("A=D+M")
            asm.append("D=A")
            asm.append("@R13")
            asm.append("M=D")
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")
            asm.append("@R13")
            asm.append("A=M")
            asm.append("M=D")
            
        elif segment == "static":
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")
            asm.append(f"@{filename}.{index}")
            asm.append("M=D")
            
        elif segment == "temp":
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")
            asm.append(f"@{5 + index}")
            asm.append("M=D")
            
        elif segment == "pointer":
            asm.append("@SP")
            asm.append("M=M-1")
            asm.append("A=M")
            asm.append("D=M")
            asm.append(f"@{3 + index}")
            asm.append("M=D")
    
    return asm


def translateArithmetic(command, counter):
    asm = []
    
    if command == "add":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=D+M")
        asm.append("@SP")
        asm.append("M=M+1")
        
    elif command == "sub":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=M-D")
        asm.append("@SP")
        asm.append("M=M+1")
        
    elif command == "neg":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=-M")
        asm.append("@SP")
        asm.append("M=M+1")
        
    elif command == "eq": 
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M-D")
        asm.append(f"@EQ_TRUE{counter}")
        asm.append("D;JEQ")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=0")
        asm.append(f"@EQ_END{counter}")
        asm.append("0;JMP")
        asm.append(f"(EQ_TRUE{counter})")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=-1")
        asm.append(f"(EQ_END{counter})")
        
    elif command == "gt": 
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M-D")
        asm.append(f"@GT_TRUE{counter}")
        asm.append("D;JGT")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=0")
        asm.append(f"@GT_END{counter}")
        asm.append("0;JMP")
        asm.append(f"(GT_TRUE{counter})")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=-1")
        asm.append(f"(GT_END{counter})")
    
    elif command == "lt":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M-D")
        asm.append(f"@LT_TRUE{counter}")
        asm.append("D;JLT")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=0")
        asm.append(f"@LT_END{counter}")
        asm.append("0;JMP")
        asm.append(f"(LT_TRUE{counter})")
        asm.append("@SP")
        asm.append("A=M")
        asm.append("M=-1")
        asm.append(f"(LT_END{counter})")

    elif command == "and":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=D&M")
        asm.append("@SP")
        asm.append("M=M+1")
        
    elif command == "or":
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=D|M")
        asm.append("@SP")
        asm.append("M=M+1")
        
    elif command == "not": 
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("M=!M")
        asm.append("@SP")
        asm.append("M=M+1")
    
    return asm

def cleanLine(line):
    line = line.split("//")[0]

    line = line.strip()

    if line == "":
        return ""

    return line
    
def translateBranching(command, labelName, functionName): 
    asm = []
    if command == "label":
        asm.append(f"({functionName}${labelName})")
    elif command == "goto":
        asm.append(f"@{functionName}${labelName}")
        asm.append("0;JMP")
    elif command == "if-goto":
       ## pop the top of the stack into D,
        asm.append("@SP")
        asm.append("M=M-1")
        asm.append("A=M")
        asm.append("D=M")
        asm.append(f"@{functionName}${labelName}")
        asm.append("D;JNE") ## jump if it's not zero (true) 
        
    return asm

def translateFunction(functionName, howManyTimes):
    asm = []
    asm.append(f"({functionName})")
    for _ in range(howManyTimes):
        # pushes a 0 onto the stack and increments SP
        # local 0 ... local howmanytimes-1 should all be initialized to 0
        asm.append("@SP") # point A to address 256 (where SP lives)
        asm.append("A=M") # follow the pointer — now A = the current top of stack address
        asm.append("M=0") # write 0 into that address
        asm.append("@SP") # point A to SP again
        asm.append("M=M+1") # increment SP
    return asm

def translateReturn(functionName):
    asm = [] 
    # asm.append(f"({functionName})")
    # save LCL into R14 so we can return to the correct place after restoring the caller's state
    asm.append("@LCL")
    asm.append("D=M")
    asm.append("@R14")
    asm.append("M=D")
    # save the return address (FRAME - 5) into R15 so we can jump to it after restoring the caller's state
    asm.append("@5")
    asm.append("D=A")
    asm.append("@R14")
    asm.append("A=M-D")
    asm.append("D=M")
    asm.append("@R15")
    asm.append("M=D")
    # reposition the return value ARG = pop()
    asm.append("@SP")
    asm.append("M=M-1")
    asm.append("A=M")
    asm.append("D=M")
    asm.append("@ARG")
    asm.append("A=M")
    asm.append("M=D")
    # restore SP = ARG + 1
    asm.append("@ARG")
    asm.append("D=M+1")
    asm.append("@SP")
    asm.append("M=D")
    # restore THAT, THIS, ARG, LCL from the saved frame
    asm.append("@R14")
    asm.append("AM=M-1")
    asm.append("D=M")
    asm.append("@THAT")
    asm.append("M=D")
    asm.append("@R14")
    asm.append("AM=M-1")
    asm.append("D=M")
    asm.append("@THIS")
    asm.append("M=D")
    asm.append("@R14")
    asm.append("AM=M-1")
    asm.append("D=M")
    asm.append("@ARG")
    asm.append("M=D")
    asm.append("@R14")
    asm.append("AM=M-1")
    asm.append("D=M")
    asm.append("@LCL")
    asm.append("M=D")
    # jump to address saved in R15
    asm.append("@R15")
    asm.append("A=M")
    asm.append("0;JMP")
    return asm

def translateCall(functionName, numArgs, counter):
    asm = []
    
    # Push return address 
    # it needs to know where to jump back to.
    # The return address is stored at FRAME-5, it should get popped 
    returnLabel = f"RETURN_{functionName}_{counter}"
    asm.append(f"@{returnLabel}")
    asm.append("D=A")
    asm.append("@SP")
    asm.append("A=M")
    asm.append("M=D")
    asm.append("@SP")
    asm.append("M=M+1")
    
    # Push LCL / frame 4
    asm.append("@LCL")
    asm.append("D=M")
    asm.append("@SP")
    asm.append("A=M")
    asm.append("M=D")
    asm.append("@SP")
    asm.append("M=M+1")
    
    # Push ARG / frame 3
    asm.append("@ARG")
    asm.append("D=M")
    asm.append("@SP")
    asm.append("A=M")
    asm.append("M=D")
    asm.append("@SP")
    asm.append("M=M+1")
    
    # Push THIS / frame 2
    asm.append("@THIS")
    asm.append("D=M")
    asm.append("@SP")
    asm.append("A=M")
    asm.append("M=D")
    asm.append("@SP")
    asm.append("M=M+1")
    
    # Push THAT / frame 1
    asm.append("@THAT")
    asm.append("D=M")
    asm.append("@SP")
    asm.append("A=M")
    asm.append("M=D")
    asm.append("@SP")
    asm.append("M=M+1")

    # ARG = SP - numArgs - 5 (return address + 4 saved pointers),
    asm.append(f"@{numArgs + 5}")
    asm.append("D=A")
    asm.append("@SP")
    asm.append("D=M-D")
    asm.append("@ARG")
    asm.append("M=D")
    # LCL = SP
    asm.append("@SP")
    asm.append("D=M")
    asm.append("@LCL")
    asm.append("M=D")
    # Jump to the called function
    # The function should execute its code and that should be it idk frl
    asm.append(f"@{functionName}")
    asm.append("0;JMP")
    
    # Return label
    asm.append(f"({returnLabel})")
    
    return asm

def main(): 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
    else:
        inputFile = "SimpleAdd/SimpleAdd.vm"       # default test
        
    outputFile = inputFile.replace(".vm", ".asm")
    
    fileNameSplit = inputFile.split("/")
    fileNameforTranslate = fileNameSplit[-1].replace(".vm", "")
    currentFunction = fileNameforTranslate
    
    print("Input file:", inputFile)
    print("Output file:", outputFile)
    
    with open(inputFile, "r") as vm:
        cleaned = []
        for line in vm:
            newLine = cleanLine(line)
            if newLine != "":
                cleaned.append(newLine)
                
    asmLines = []
    counter = 0 # need this for the eq, gt, lt commands to create unique labels
    
    for line in cleaned:
        wordsInLine = line.split() 
        
        if wordsInLine[0] == "function":
            currentFunction = wordsInLine[1]
            numTimes = int(wordsInLine[2])
            translated = translateFunction(currentFunction, numTimes)
            asmLines.extend(translated) 
        
        elif wordsInLine[0] == "push" or wordsInLine[0] == "pop":
            command = wordsInLine[0]
            segment = wordsInLine[1]
            index = int(wordsInLine[2])
            
            translated = translateMemoryAccess(command, segment, index, fileNameforTranslate)
            asmLines.extend(translated)
            
        elif wordsInLine[0] in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            command = wordsInLine[0]
            translated = translateArithmetic(command, counter)
            asmLines.extend(translated)
             
            if command in ["eq", "gt", "lt"]:
                counter += 1
                
        elif wordsInLine[0] in ["label", "goto", "if-goto"]:
            command = wordsInLine[0]
            translated = translateBranching(wordsInLine[0], wordsInLine[1], currentFunction)
            asmLines.extend(translated)
        
        elif wordsInLine[0] == "return":
            translated = translateReturn(currentFunction)
            asmLines.extend(translated)
            
        ## call 
        ## initizalize SP = 256 
        ## call sys.init at the start of every program 
        ## instead of passing a single .vm file, needs to pass a diractory 
            ## find alll of the .vm files in the directory and translate them all, putting the asm code into a single .asm file
        

    with open(outputFile, "w") as asm:
        # for line in asmLines:
        #     asm.write(line + "\n")
        asm.write("\n".join(asmLines))
            
main()   