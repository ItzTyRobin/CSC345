class SymbolTable: 
    
    # need two seperate symbol tables, so 
    # we make each one its own dictionary 
    
    # a new class, means we should reset both tables. 
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
        table.subroutine = {}
        
    def enterIntoData(table, name, type, kind):
        if kind in ("static", "field"):
            index = table.countVariables(kind)
            table.classTable[name] = (type, kind, index)
        else:
            index = table.countVariables(kind)
            table.subroutineTable[name] = (type, kind, index)
            
    # counts how many variables of the given kind are already defined 
    def countVariables(table, kind): 
        count = 0 
        if kind in ("static", "field"): 
            for symbol in table.classTable.values(): 
                if symbol[1] == kind: 
                    count += 1
        else: 
            for symbol in table.subroutineTable.values(): 
                if symbol[1] == kind: 
                    count += 1 
            
            
    # lookup method that finds which table a name lives in 
    # check subroutine first, then class 
    
    # write get methods for each type, kind, and index of a symbol in the table. 