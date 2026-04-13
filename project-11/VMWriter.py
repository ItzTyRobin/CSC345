class VMWriter: 
    
    # Creates a new output .vm file / stream, 
    # and repares it for writing 
    def __intit__(self, fileName): 
        self.file = open(fileName, 'w')

    def writePush(self, segment, index):
        self.file.write('push ' + segment + ' ' + str(index))



        
        