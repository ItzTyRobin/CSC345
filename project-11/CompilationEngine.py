from JackTokenizer import tokenType
from SymbolTable import SymbolTable

class Compilation:
    currentValKind = "var"
    

    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.out = outputFile
        self.symbolTable = SymbolTable() 

    def write(self, line):
        self.out.write(line + '\n')

    def writeSymbol(self, value):
        value = value.replace('&', '&amp;')
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        self.write('<symbol> ' + value + ' </symbol>')

    def currentVal(self):
        return self.tokenizer.currentToken.value

    def currentType(self):
        return self.tokenizer.currentToken.type

    def advance(self):
        self.tokenizer.advance()

    def compileClass(self):
        self.write('<class>')
        self.write('<keyword> class </keyword>')
        self.advance()
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        self.writeSymbol('{')
        self.advance()
        while self.currentVal() in ['static', 'field']:
            self.compileClassVarDec()
        while self.currentVal() in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        self.writeSymbol('}')
        self.write('</class>')

    def compileClassVarDec(self):
        self.write('<classVarDec>')
        # Static or field
        # kind = self.currentVal()
        self.write('<keyword> ' + self.currentVal() + ' </keyword>')
        
        self.advance()
        # Type
        if self.currentType() == tokenType.keyWord:
            self.write('<keyword> ' + self.currentVal() + ' </keyword>')
        else:
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        # Var name
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        # print("HERE HERE HERE HERE!!!!!: " + self.currentVal())
        self.symbolTable.define(self.currentVal(), self.currentType(), "var")
        self.advance()
        # More var names
        while self.currentVal() == ',':
            self.writeSymbol(',')
            self.advance()
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
            self.advance()
        # Semicolon
        self.writeSymbol(';')
        self.advance()
        self.write('</classVarDec>')

    def compileSubroutineDec(self):
        self.write('<subroutineDec>')
        # Constructor, function, or method
        self.write('<keyword> ' + self.currentVal() + ' </keyword>')
        currentValKind = self.currentVal()
        # self.symbolTable.define(, self.currentType(), currentValKind)
        # print("WHAT IS THE KIND: ", self.currentVal())
        self.advance()
        if self.currentType() == tokenType.keyWord:
            self.write('<keyword> ' + self.currentVal() + ' </keyword>')
        else:
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        print("current name: ", self.currentVal())
        self.advance()
        self.writeSymbol('(')
        self.advance()
        self.compileParameterList()
        self.writeSymbol(')')
        self.advance()
        self.compileSubroutineBody()
        
        self.write('</subroutineDec>')

    def compileParameterList(self):
        self.write('<parameterList>')
        if self.currentVal() != ')':
            if self.currentType() == tokenType.keyWord:
                self.write('<keyword> ' + self.currentVal() + ' </keyword>')
            else:
                self.write('<identifier> ' + self.currentVal() + ' </identifier>')
            self.advance()
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
            self.advance()
            while self.currentVal() == ',':
                self.writeSymbol(',')
                self.advance()
                if self.currentType() == tokenType.keyWord:
                    self.write('<keyword> ' + self.currentVal() + ' </keyword>')
                else:
                    self.write('<identifier> ' + self.currentVal() + ' </identifier>')
                self.advance()
                self.write('<identifier> ' + self.currentVal() + ' </identifier>')
                self.advance()
        self.write('</parameterList>')

    def compileSubroutineBody(self):
        self.write('<subroutineBody>')
        self.writeSymbol('{')
        self.advance()
        while self.currentVal() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.writeSymbol('}')
        self.advance()
        self.write('</subroutineBody>')

    def compileVarDec(self):
        self.write('<varDec>')
        self.write('<keyword> var </keyword>')
        self.advance()
        if self.currentType() == tokenType.keyWord:
            self.write('<keyword> ' + self.currentVal() + ' </keyword>')
        else:
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        while self.currentVal() == ',':
            self.writeSymbol(',')
            
            self.advance()
            # self.write(currentVal.)
            self.advance()
        self.writeSymbol(';')
        self.advance()
        self.write('</varDec>')

    def compileStatements(self):
        self.write('<statements>')
        while self.currentVal() in ['let', 'if', 'while', 'do', 'return']:
            if self.currentVal() == 'let':
                self.compileLet()
            elif self.currentVal() == 'if':
                self.compileIf()
            elif self.currentVal() == 'while':
                self.compileWhile()
            elif self.currentVal() == 'do':
                self.compileDo()
            elif self.currentVal() == 'return':
                self.compileReturn()
        self.write('</statements>')

    def compileLet(self):
        self.write('<letStatement>')
        self.write('<keyword> let </keyword>')
        self.advance()
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        if self.currentVal() == '[':
            self.writeSymbol('[')
            self.advance()
            self.compileExpression()
            self.writeSymbol(']')
            self.advance()
        self.writeSymbol('=')
        self.advance()
        self.compileExpression()
        self.writeSymbol(';')
        self.advance()
        self.write('</letStatement>')

    def compileIf(self):
        self.write('<ifStatement>')
        self.write('<keyword> if </keyword>')
        self.advance()
        self.writeSymbol('(')
        self.advance()
        self.compileExpression()
        self.writeSymbol(')')
        self.advance()
        self.writeSymbol('{')
        self.advance()
        self.compileStatements()
        self.writeSymbol('}')
        self.advance()
        if self.currentVal() == 'else':
            self.write('<keyword> else </keyword>')
            self.advance()
            self.writeSymbol('{')
            self.advance()
            self.compileStatements()
            self.writeSymbol('}')
            self.advance()
        self.write('</ifStatement>')

    def compileWhile(self):
        self.write('<whileStatement>')
        self.write('<keyword> while </keyword>')
        self.advance()
        self.writeSymbol('(')
        self.advance()
        self.compileExpression()
        self.writeSymbol(')')
        self.advance()
        self.writeSymbol('{')
        self.advance()
        self.compileStatements()
        self.writeSymbol('}')
        self.advance()
        self.write('</whileStatement>')

    def compileDo(self):
        self.write('<doStatement>')
        self.write('<keyword> do </keyword>')
        self.advance()
        self.write('<identifier> ' + self.currentVal() + ' </identifier>')
        self.advance()
        if self.currentVal() == '.':
            self.writeSymbol('.')
            self.advance()
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
            self.advance()
        self.writeSymbol('(')
        self.advance()
        self.compileExpressionList()
        self.writeSymbol(')')
        self.advance()
        self.writeSymbol(';')
        self.advance()
        self.write('</doStatement>')

    def compileReturn(self):
        self.write('<returnStatement>')
        self.write('<keyword> return </keyword>')
        self.advance()
        if self.currentVal() != ';':
            self.compileExpression()
        self.writeSymbol(';')
        self.advance()
        self.write('</returnStatement>')

    def compileExpression(self):
        self.write('<expression>')
        self.compileTerm()
        while self.currentVal() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.writeSymbol(self.currentVal())
            self.advance()
            self.compileTerm()
        self.write('</expression>')

    def compileTerm(self):
        self.write('<term>')
        if self.currentType() == tokenType.intConst:
            self.write('<integerConstant> ' + str(self.currentVal()) + ' </integerConstant>')
            self.advance()
        elif self.currentType() == tokenType.stringConst:
            self.write('<stringConstant> ' + self.currentVal() + ' </stringConstant>')
            self.advance()
        elif self.currentVal() in ['true', 'false', 'null', 'this']:
            self.write('<keyword> ' + self.currentVal() + ' </keyword>')
            self.advance()
        elif self.currentVal() == '(':
            self.writeSymbol('(')
            self.advance()
            self.compileExpression()
            self.writeSymbol(')')
            self.advance()
        elif self.currentVal() in ['-', '~']:
            self.writeSymbol(self.currentVal())
            self.advance()
            self.compileTerm()
        else:
            self.write('<identifier> ' + self.currentVal() + ' </identifier>')
            self.advance()
            if self.currentVal() == '[':
                self.writeSymbol('[')
                self.advance()
                self.compileExpression()
                self.writeSymbol(']')
                self.advance()
            elif self.currentVal() == '.':
                self.writeSymbol('.')
                self.advance()
                self.write('<identifier> ' + self.currentVal() + ' </identifier>')
                self.advance()
                self.writeSymbol('(')
                self.advance()
                self.compileExpressionList()
                self.writeSymbol(')')
                self.advance()
            elif self.currentVal() == '(':
                self.writeSymbol('(')
                self.advance()
                self.compileExpressionList()
                self.writeSymbol(')')
                self.advance()
        self.write('</term>')

    def compileExpressionList(self):
        self.write('<expressionList>')
        if self.currentVal() != ')':
            self.compileExpression()
            while self.currentVal() == ',':
                self.writeSymbol(',')
                self.advance()
                self.compileExpression()
        self.write('</expressionList>')