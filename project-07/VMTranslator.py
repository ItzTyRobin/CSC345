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


def translateLabel(label_name):
    return [f"({label_name})"]


def main(): 
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
    else:
        inputFile = "SimpleAdd/SimpleAdd.vm"       # default test
        
    outputFile = inputFile.replace(".vm", ".asm")
    
    print("Input file:", inputFile)
    print("Output file:", outputFile)
    
    with open(inputFile, "r") as vm:
        lines = vm.readlines()
        
    with open(outputFile, "w") as asm:
        for line in lines:
            asm.write(line)



        