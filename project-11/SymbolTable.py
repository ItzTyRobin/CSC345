class SymbolTable: 
    subroutineCount = 0
    classCount = 0
    
    # need two seperate symbol tables, so 
    # we make each one its own dictionary 
    def symbolTable():
        table = {
            "classTable": {},  # static and field variables
            "subroutineTable": {}  # argument and local variables
            
            # example of input in table: 
            # { "x": ("int", "field", 0) }
            #  name   type   kind   index
        }
        return table
    
    # a new subroutine means we should reset the whole subroutine table 
    def resetSubroutine(table):
        table.subroutineTable = {}
    
    # a new class, means we should reset both tables. 
    def resetClass(table): 
        table.classTable = {}
        table.resetSubroutine(table.subroutineTable)
        
    # Defines (adds to table) a new variable of teh given name, type, and kind
    # Assigns to it the index value of that kind, 
    # and adds 1 to the index
    def define(table, name, type, kind):
        if kind in ("static", "field"):
            table.classTable[name] = (type, kind, classCount)
            classCount += 1
        else:
            table.subroutineTable[name] = (type, kind, subroutineCount)
            subroutineCount += 1
            
    # returns the number of variables of the given 
    # kind already defined in the table 
    def varCount(table, kind): 
        count = 0 
        if kind in ("static", "field"): 
            for symbol in table.classTable.values(): 
                if symbol[1] == kind: 
                    count += 1
        else: 
            for symbol in table.subroutineTable.values(): 
                if symbol[1] == kind: 
                    count += 1 
        return count 
            
    # kindOf
    # typeOf 
    # indexOf  