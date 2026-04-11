


class tokenType:
    keyWord = 1
    symbol = 2
    identifier = 3
    intConst = 4
    stringConst = 5

class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    
    keyWords = ['class', 'method', 'function', 'constructor', 'int', 'boolean', 
                'char', 'void', 'var', 'static', 'field', 'let', 'do', 'if', 
                'else', 'while', 'return', 'true', 'false', 'null', 'this']
    
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', 
               '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, inputFile):
        if hasattr(inputFile, 'read'):
            self.input = inputFile.read()
        else:
            with open(inputFile, 'r') as f:
                self.input = f.read()

        self.tokens = []
        self.pos = 0
        self.currentToken = None
        self.tokenize()
        self.pos = 0
        if self.tokens:
            self.currentToken = self.tokens[0]

    def hasMoreTokens(self):
        return self.pos < len(self.tokens) - 1

    def advance(self):
        if self.hasMoreTokens():
            self.pos += 1
            self.currentToken = self.tokens[self.pos]
        return self.currentToken

    def skipWhitespaceAndComments(self):
        while self.pos < len(self.input):
            # skip whitespace
            if self.input[self.pos].isspace():
                self.pos += 1
            # skip single line comment
            elif self.input[self.pos:self.pos+2] == '//':
                while self.pos < len(self.input) and self.input[self.pos] != '\n':
                    self.pos += 1
            # skip block comment
            elif self.input[self.pos:self.pos+2] == '/*':
                self.pos += 2
                while self.pos < len(self.input) and self.input[self.pos:self.pos+2] != '*/':
                    self.pos += 1
                self.pos += 2
            else:
                break

    def tokenizeWord(self):
        word = ''
        while self.pos < len(self.input) and (self.input[self.pos].isalnum() or self.input[self.pos] == '_'):
            word += self.input[self.pos]
            self.pos += 1
        if word in self.keyWords:
            return token(tokenType.keyWord, word)
        return token(tokenType.identifier, word)

    def tokenizeNumber(self):
        number = ''
        while self.pos < len(self.input) and self.input[self.pos].isdigit():
            number += self.input[self.pos]
            self.pos += 1
        return token(tokenType.intConst, int(number))

    def tokenizeString(self):
        self.pos += 1  # skip opening "
        string = ''
        while self.pos < len(self.input) and self.input[self.pos] != '"':
            string += self.input[self.pos]
            self.pos += 1
        self.pos += 1  # skip closing "
        return token(tokenType.stringConst, string)

    def tokenize(self):
        while self.pos < len(self.input):
            self.skipWhitespaceAndComments()
            if self.pos >= len(self.input):
                break
            c = self.input[self.pos]
            if c.isalpha() or c == '_':
                self.tokens.append(self.tokenizeWord())
            elif c == '"':
                self.tokens.append(self.tokenizeString())
            elif c in self.symbols:
                self.tokens.append(token(tokenType.symbol, c))
                self.pos += 1
            elif c.isdigit():
                self.tokens.append(self.tokenizeNumber())