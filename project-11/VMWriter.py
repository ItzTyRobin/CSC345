class VMWriter: 
    
    # Creates a new output .vm file / stream, 
    # and repares it for writing 
    def __intit__(fileName): 
        file = open(fileName, 'w')

    # write a VM push command
    def writePush(segment, index):
        VMWriter.file.write("push " + segment + " " + str(index))

    # writes a VM pop command 
    def writePop(segment, index): 
        VMWriter.file.write("pop " + segment + " " + str(index))

    # writes a VM arithmetic-logical command 
    def writeArithmetic(command): 
        VMWriter.file.write(command.lower())
    
    # writes a VM label command 
    def writeLable(label): 
        VMWriter.file.write("label " + label)
       
    # write a VM goto command  
    def writeGoto(label): 
        VMWriter.file.write("goto " + label)
        
    # writes a VM call command
    def writeIf(label): 
        VMWriter.file.write("if-goto " + label) 
    
    # writes a VM call command 
    def writeCall(label, nArgs): 
        VMWriter.file.write("call " + label + " " + nArgs)
        
    # writes a VM function command 
    def writeFunction(name, nVars): 
        VMWriter.file.write("function " + name + " " + nVars)
        
    # writes a VM return command 
    def writeReturn(): 
        VMWriter.file.write("return")
    






    # closes the output file / stream 
    def close(): 
        VMWriter.file.close()