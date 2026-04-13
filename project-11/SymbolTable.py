class SymbolTable: 
    subroutineCount = 0
    classCount = 0
    table = {}
    
    # when labeled function, self cotained subroutine 
    # only count extra parameter when its a method 
    # 
    
    # need two seperate symbol tables, so 
    # we make each one its own dictionary 
    def __intit__():
        table = {
            "classTable": {},  # static and field variables
            "subroutineTable": {}  # argument and local variables
            
            # example of input in table: 
            # { "x": ("int", "field", 0) }
            #  name   type   kind   index
        }
        return table
    
    def resetSubroutine(table):
        table.subroutineTable = {}
    
    def resetClass(table): 
        table.classTable = {}
        
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
    
    # returns the kind of the named identifier 
    # if the identifier is not found, returns NONE 
    def kindOf(symbol): 
        for sym in symbol.table.classTable.keys(): 
            if sym == symbol: 
                return sym.values[1]
        
        for sym in symbol.table.subroutineTable.keys(): 
            if sym == symbol: 
                return sym.values[1]
            
    # return sthe type of the named variable
    def typeOf(symbol): 
        for sym in symbol.table.classTable.keys(): 
            if sym == symbol: 
                return sym.values[0]
        
        for sym in symbol.table.subroutineTable.keys(): 
            if sym == symbol: 
                return sym.values[0]
    
    # returns the index of the named variable
    def indexOf(symbol): 
        count = 0 
        for sym in symbol.table.classTable.keys(): 
            count += 1 
            if sym == symbol: 
                return count
    
        count = 0 
        for sym in symbol.table.subroutineTable.keys(): 
            count += 1 
            if sym == symbol: 
                return count 