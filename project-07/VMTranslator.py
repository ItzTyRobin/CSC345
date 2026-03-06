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


def main(): 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
    else:
        inputFile = "SimpleAdd/SimpleAdd.vm"       # default test
        
    outputFile = inputFile.replace(".vm", ".asm")
    
    fileNameSplit = inputFile.split("/")
    fileNameforTranslate = fileNameSplit[-1].replace(".vm", "")
    
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
        
        if wordsInLine[0] == "push" or wordsInLine[0] == "pop":
            command = wordsInLine[0]
            segment = wordsInLine[1]
            index = int(wordsInLine[2])
            
            translated = translateMemoryAccess(command, segment, index, fileNameforTranslate)
            asmLines.extend(translated)
            
        else: 
            command = wordsInLine[0]
            translated = translateArithmetic(command, counter)
            asmLines.extend(translated)
             
            if command in ["eq", "gt", "lt"]:
                counter += 1
                
    with open(outputFile, "w") as asm:
        # for line in asmLines:
        #     asm.write(line + "\n")
        asm.write("\n".join(asmLines))
            
main()   