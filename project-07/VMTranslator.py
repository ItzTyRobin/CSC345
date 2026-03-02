import sys

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
        