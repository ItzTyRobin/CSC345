"""
recursive descent parser
"""

from Tokenizer import tokenType


class Compilation:
    escapesXML = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;'}

    def __init__(self, tokenizer, outputFile):
        self.tokenizer = tokenizer
        self.outputFile = outputFile

    def writeSymbol(self, value):
        escaped = self.escapesXML.get(value, value)
        
        self.outputFile.write('<symbol> ' + escaped + ' </symbol>\n')

    def compileClass(self):
        # write <class>
        self.outputFile.write('<class>\n')
        # write 'class' keyword 
        self.outputFile.write('<keyword> class </keyword>\n')
        self.tokenizer.advance()
        # write class name
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write '{' symbol
        self.outputFile.write('<symbol> { </symbol>\n')
        self.tokenizer.advance()
        # compile class var decs and subroutine decs
        while self.tokenizer.currentToken.value in ['static', 'field']:
            self.compileClassVarDec()
        while self.tokenizer.currentToken.value in ['constructor', 'function', 'method']:
            self.compileSubroutineDec()
        # write '}' symbol
        self.outputFile.write('<symbol> } </symbol>\n')
        # write </class>
        self.outputFile.write('</class>\n')

    def compileClassVarDec(self):
        # write <classVarDec>
        self.outputFile.write('<classVarDec>\n')
        # write 'static' or 'field' keyword
        self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
        self.tokenizer.advance()
        # write type
        if self.tokenizer.currentToken.type == tokenType.KEYWORD:
            self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
        else:
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write var name
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write (',' var name)*
        while self.tokenizer.currentToken.value == ',':
            self.outputFile.write('<symbol> , </symbol>\n')
            self.tokenizer.advance()
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
        # write ';' symbol
        self.outputFile.write('<symbol> ; </symbol>\n')
        self.tokenizer.advance()
        # write </classVarDec>
        self.outputFile.write('</classVarDec>\n')

    def compileSubroutineDec(self):
        # write <subroutineDec>
        self.outputFile.write('<subroutineDec>\n')
        # write 'constructor' or 'function' or 'method' keyword
        self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
        self.tokenizer.advance()
        # write 'void' or type
        if self.tokenizer.currentToken.value == 'void':
            self.outputFile.write('<keyword> void </keyword>\n')
        elif self.tokenizer.currentToken.type == tokenType.KEYWORD:
            self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
        else:
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write subroutine name
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write '(' symbol
        self.outputFile.write('<symbol> ( </symbol>\n')
        self.tokenizer.advance()
        # compile parameter list
        self.compileParameterList()
        # write ')' symbol
        self.outputFile.write('<symbol> ) </symbol>\n')
        self.tokenizer.advance()
        # compile subroutine body
        self.compileSubroutineBody()
        # write </subroutineDec>
        self.outputFile.write('</subroutineDec>\n')

    def compileParameterList(self):
        # write <parameterList>
        self.outputFile.write('<parameterList>\n')
        # write ((type varName) (',' type varName)*)? 
        if self.tokenizer.currentToken.value != ')':
            # write type
            if self.tokenizer.currentToken.type == tokenType.KEYWORD:
                self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
            else:
                self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
            # write var name
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
            while self.tokenizer.currentToken.value == ',':
                # write ',' symbol
                self.outputFile.write('<symbol> , </symbol>\n')
                self.tokenizer.advance()
                # write type
                if self.tokenizer.currentToken.type == tokenType.KEYWORD:
                    self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
                else:
                    self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
                self.tokenizer.advance()
                # write var name
                self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
                self.tokenizer.advance()
        # write </parameterList>
        self.outputFile.write('</parameterList>\n')

    def compileSubroutineBody(self):
        # write <subroutineBody>
        self.outputFile.write('<subroutineBody>\n')
        # write '{' symbol
        self.outputFile.write('<symbol> { </symbol>\n')
        self.tokenizer.advance()
        # compile var decs
        while self.tokenizer.currentToken.value == 'var':
            self.compileVarDec()
        # compile statements
        self.compileStatements()
        # write '}' symbol
        self.outputFile.write('<symbol> } </symbol>\n')
        self.tokenizer.advance()
        # write </subroutineBody>
        self.outputFile.write('</subroutineBody>\n')

    def compileVarDec(self):
        # write <varDec>
        self.outputFile.write('<varDec>\n')
        # write 'var' keyword
        self.outputFile.write('<keyword> var </keyword>\n')
        self.tokenizer.advance()
        # write type
        if self.tokenizer.currentToken.type == tokenType.KEYWORD:
            self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
        else:
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write var name
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write (',' var name)* 
        while self.tokenizer.currentToken.value == ',':
            self.outputFile.write('<symbol> , </symbol>\n')
            self.tokenizer.advance()
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
        # write ';' symbol
        self.outputFile.write('<symbol> ; </symbol>\n')
        self.tokenizer.advance()
        # write </varDec>
        self.outputFile.write('</varDec>\n')

    def compileStatements(self):
        # write <statements>
        self.outputFile.write('<statements>\n')
        # write statements
        while self.tokenizer.currentToken.value in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.currentToken.value == 'let':
                self.compileLet()
            elif self.tokenizer.currentToken.value == 'if':
                self.compileIf()
            elif self.tokenizer.currentToken.value == 'while':
                self.compileWhile()
            elif self.tokenizer.currentToken.value == 'do':
                self.compileDo()
            elif self.tokenizer.currentToken.value == 'return':
                self.compileReturn()
        # write </statements>
        self.outputFile.write('</statements>\n')

    def compileLet(self):
        # write <letStatement>
        self.outputFile.write('<letStatement>\n')
        # write 'let' keyword
        self.outputFile.write('<keyword> let </keyword>\n')
        self.tokenizer.advance()
        # write var name
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write '[' expression ']' if array access
        if self.tokenizer.currentToken.value == '[':
            self.outputFile.write('<symbol> [ </symbol>\n')
            self.tokenizer.advance()
            self.compileExpression()
            self.outputFile.write('<symbol> ] </symbol>\n')
            self.tokenizer.advance()
        # write '=' symbol
        self.outputFile.write('<symbol> = </symbol>\n')
        self.tokenizer.advance()
        # compile expression
        self.compileExpression()
        # write ';' symbol
        self.outputFile.write('<symbol> ; </symbol>\n')
        self.tokenizer.advance()
        # write </letStatement>
        self.outputFile.write('</letStatement>\n')

    def compileIf(self):
        # write <ifStatement>
        self.outputFile.write('<ifStatement>\n')
        # write 'if' keyword
        self.outputFile.write('<keyword> if </keyword>\n')
        self.tokenizer.advance()
        # write '(' symbol
        self.outputFile.write('<symbol> ( </symbol>\n')
        self.tokenizer.advance()
        # compile expression
        self.compileExpression()
        # write ')' symbol
        self.outputFile.write('<symbol> ) </symbol>\n')
        self.tokenizer.advance()
        # write '{' symbol
        self.outputFile.write('<symbol> { </symbol>\n')
        self.tokenizer.advance()
        # compile statements
        self.compileStatements()
        # write '}' symbol
        self.outputFile.write('<symbol> } </symbol>\n')
        self.tokenizer.advance()
        # compile else clause if present
        if self.tokenizer.currentToken.value == 'else':
            self.outputFile.write('<keyword> else </keyword>\n')
            self.tokenizer.advance()
            # write '{' symbol
            self.outputFile.write('<symbol> { </symbol>\n')
            self.tokenizer.advance()
            # compile statements
            self.compileStatements()
            # write '}' symbol
            self.outputFile.write('<symbol> } </symbol>\n')
            self.tokenizer.advance()
        # write </ifStatement>
        self.outputFile.write('</ifStatement>\n')

    def compileWhile(self):
        # write <whileStatement>
        self.outputFile.write('<whileStatement>\n')
        # write 'while' keyword
        self.outputFile.write('<keyword> while </keyword>\n')
        self.tokenizer.advance()
        # write '(' symbol
        self.outputFile.write('<symbol> ( </symbol>\n')
        self.tokenizer.advance()
        # compile expression
        self.compileExpression()
        # write ')' symbol
        self.outputFile.write('<symbol> ) </symbol>\n')
        self.tokenizer.advance()
        # write '{' symbol
        self.outputFile.write('<symbol> { </symbol>\n')
        self.tokenizer.advance()
        # compile statements
        self.compileStatements()
        # write '}' symbol
        self.outputFile.write('<symbol> } </symbol>\n')
        self.tokenizer.advance()
        # write </whileStatement>
        self.outputFile.write('</whileStatement>\n')

    def compileDo(self):
        # write <doStatement> 
        self.outputFile.write('<doStatement>\n')
        # write 'do' keyword 
        self.outputFile.write('<keyword> do </keyword>\n')
        self.tokenizer.advance()
        # write subroutine/class/var name 
        self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
        self.tokenizer.advance()
        # write '.' and subroutine name if method call on object
        if self.tokenizer.currentToken.value == '.':
            self.outputFile.write('<symbol> . </symbol>\n')
            self.tokenizer.advance()
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
        # write '(' symbol 
        self.outputFile.write('<symbol> ( </symbol>\n')
        self.tokenizer.advance()
        # compile expression list
        self.compileExpressionList()
        # write ')' symbol 
        self.outputFile.write('<symbol> ) </symbol>\n')
        self.tokenizer.advance()
        # write ';' symbol 
        self.outputFile.write('<symbol> ; </symbol>\n')
        self.tokenizer.advance()
        # write </doStatement> 
        self.outputFile.write('</doStatement>\n')

    def compileReturn(self):
        # write <returnStatement> 
        self.outputFile.write('<returnStatement>\n')
        # write 'return' keyword 
        self.outputFile.write('<keyword> return </keyword>\n')
        self.tokenizer.advance()
        # compile expression if not ';'
        if self.tokenizer.currentToken.value != ';':
            self.compileExpression()
        # write ';' symbol 
        self.outputFile.write('<symbol> ; </symbol>\n')
        self.tokenizer.advance()
        # write </returnStatement> 
        self.outputFile.write('</returnStatement>\n')

    def compileExpression(self):
        # write <expression> 
        self.outputFile.write('<expression>\n')
        # compile term
        self.compileTerm()
        # write (op term)* 
        while self.tokenizer.currentToken.value in ['+', '-', '*', '/', '&', '|', '<', '>', '=', '"', '~']:
            self.writeSymbol(self.tokenizer.currentToken.value)
            self.tokenizer.advance()
            self.compileTerm()
        # write </expression> 
        self.outputFile.write('</expression>\n')

    def compileTerm(self):
        # write <term> 
        self.outputFile.write('<term>\n')
        if self.tokenizer.currentToken.type == tokenType.INT_CONST:
            # write integer constant 
            self.outputFile.write('<integerConstant> ' + str(self.tokenizer.currentToken.value) + ' </integerConstant>\n')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken.type == tokenType.STRING_CONST:
            # write string constant 
            self.outputFile.write('<stringConstant> ' + self.tokenizer.currentToken.value + ' </stringConstant>\n')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken.value in ['true', 'false', 'null', 'this']:
            # write keyword constant 
            self.outputFile.write('<keyword> ' + self.tokenizer.currentToken.value + ' </keyword>\n')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken.value == '(':
            # write '(' expression ')' 
            self.outputFile.write('<symbol> ( </symbol>\n')
            self.tokenizer.advance()
            self.compileExpression()
            self.outputFile.write('<symbol> ) </symbol>\n')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken.value in ['-', '~']:
            # write unary op and term 
            self.writeSymbol(self.tokenizer.currentToken.value)
            self.tokenizer.advance()
            self.compileTerm()
        else:
            # write identifier 
            self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
            self.tokenizer.advance()
            if self.tokenizer.currentToken.value == '[':
                # write '[' expression ']' for array access
                self.outputFile.write('<symbol> [ </symbol>\n')
                self.tokenizer.advance()
                self.compileExpression()
                self.outputFile.write('<symbol> ] </symbol>\n')
                self.tokenizer.advance()
            elif self.tokenizer.currentToken.value == '.':
                # write '.' subroutineName '(' expressionList ')'
                self.outputFile.write('<symbol> . </symbol>\n')
                self.tokenizer.advance()
                self.outputFile.write('<identifier> ' + self.tokenizer.currentToken.value + ' </identifier>\n')
                self.tokenizer.advance()
                self.outputFile.write('<symbol> ( </symbol>\n')
                self.tokenizer.advance()
                self.compileExpressionList()
                self.outputFile.write('<symbol> ) </symbol>\n')
                self.tokenizer.advance()
            elif self.tokenizer.currentToken.value == '(':
                # write '(' expressionList ')' for subroutine call
                self.outputFile.write('<symbol> ( </symbol>\n')
                self.tokenizer.advance()
                self.compileExpressionList()
                self.outputFile.write('<symbol> ) </symbol>\n')
                self.tokenizer.advance()
        # write </term> 
        self.outputFile.write('</term>\n')

    def compileExpressionList(self):
        # write <expressionList> 
        self.outputFile.write('<expressionList>\n')
        # compile (expression (',' expression)*)?
        if self.tokenizer.currentToken.value != ')':
            self.compileExpression()
            while self.tokenizer.currentToken.value == ',':
                self.outputFile.write('<symbol> , </symbol>\n')
                self.tokenizer.advance()
                self.compileExpression()
        # write </expressionList> 
        self.outputFile.write('</expressionList>\n')
