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

    with open(outputFile, "w") as asm:
        asm.write("\n".join(cleaned))
        
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