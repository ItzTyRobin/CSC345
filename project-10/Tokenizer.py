"""
Ignores all comments and white space in the input stream
and enable accessing the input one token at a time. 

Also parses and provides the type of each token, as defined by the jack grammar.
"""

class tokenType:
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

    def tokenTypeConstants(t):
        if t in ['class', 'method', 'function', 'constructor', 'int', 'boolean', 'char', 'void', 'var', 'static', 'field',
                 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']:
            return tokenType.KEYWORD
        elif t in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '"']:
            return tokenType.SYMBOL
        elif t.isdigit():
            return tokenType.INT_CONST
        elif t.startswith('"') and t.endswith('"'):
            return tokenType.STRING_CONST
        else:
            return tokenType.IDENTIFIER
        
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

""" 
takes in jack source code and breaks it into tokens
"""
class tokenizer:
    
    def init (self, input):
        self.input = input
        self.tokens = []
        self.currentTokenIndex = 0
        self.tokenize()

    # helper function to skip whitespace and comments
    def isWhitespace(self, t):
        return t.isspace()

    def skipWhiteSpaceAndComments(self):
        while self.currentTokenIndex < len(self.input):
            if self.isWhitespace(self.input[self.currentTokenIndex]):
                self.currentTokenIndex += 1
            elif self.input[self.currentTokenIndex:self.currentTokenIndex+2] == '//':
                self.currentTokenIndex += 2
                while self.currentTokenIndex < len(self.input) and self.input[self.currentTokenIndex] != '\n':
                    self.currentTokenIndex += 1
            elif self.input[self.currentTokenIndex:self.currentTokenIndex+2] == '/*':
                self.currentTokenIndex += 2
                while self.currentTokenIndex < len(self.input) and self.input[self.currentTokenIndex:self.currentTokenIndex+2] != '*/':
                    self.currentTokenIndex += 1
                self.currentTokenIndex += 2
            else:
                break

    # helper function to tokenize keyword or identifier
    def tokenizeKeywordOrIdentifier(self):
        word = ''
        while self.currentTokenIndex < len(self.input) and (self.input[self.currentTokenIndex].isalnum() or self.input[self.currentTokenIndex] == '_'):
            word += self.input[self.currentTokenIndex]
            self.currentTokenIndex += 1
        return token(tokenType.tokenTypeConstants(word), word)
    
    # helper function to determine if symbol
    def isSymbol(self, t):
        return t.isprintable() and not t.isalnum() and not t.isspace()

    def tokenizeSymbol(self):
        symbol = self.input[self.currentTokenIndex]
        self.currentTokenIndex += 1
        return token(tokenType.SYMBOL, symbol)
    
    # helper function to determine if number
    def isDigit(self, t):
        return t.isdigit()

    def tokenizeNumber(self):
        number = ''
        while self.currentTokenIndex < len(self.input) and self.isDigit(self.input[self.currentTokenIndex]):
            number += self.input[self.currentTokenIndex]
            self.currentTokenIndex += 1
        return token(tokenType.INT_CONST, int(number))

    # helper function to determine if string
    def isString(self, t):
        return t.startswith('"') and t.endswith('"')


    def tokenizeString(self):
        string = ''
        self.currentTokenIndex += 1  # skip opening "
        while self.currentTokenIndex < len(self.input) and self.input[self.currentTokenIndex] != '"':
            string += self.input[self.currentTokenIndex]
            self.currentTokenIndex += 1
        self.currentTokenIndex += 1  # skip closing "
        return token(tokenType.STRING_CONST, string)
    
    def hasMoreTokens(self):
        return self.currentTokenIndex < len(self.tokens) - 1 ### !!!!!!!
        #### did not have the -1 here before, which caused it to skip the last token in the list.
    
    def advance(self):
        if self.hasMoreTokens():
            self.currentTokenIndex += 1
            return self.tokens[self.currentTokenIndex - 1]
        else:
            return False
    
    def tokenize(self):
        while self.currentTokenIndex < len(self.input):
            self.skipWhiteSpaceAndComments()
            if self.currentTokenIndex >= len(self.input):
                break
            if self.input[self.currentTokenIndex].isalpha() or self.input[self.currentTokenIndex] == '_':
                self.tokens.append(self.tokenizeKeywordOrIdentifier())
            elif self.input[self.currentTokenIndex] == '"':
                self.tokens.append(self.tokenizeString())
            elif self.isSymbol(self.input[self.currentTokenIndex]):
                self.tokens.append(self.tokenizeSymbol())
            elif self.isDigit(self.input[self.currentTokenIndex]):
                self.tokens.append(self.tokenizeNumber())


class Tokenizer(tokenizer):
    def __init__(self, inputFile):
        # Accept either a file path or an already opened file object.
        if hasattr(inputFile, 'read'):
            source = inputFile.read()
        else:
            with open(inputFile, 'r') as f:
                source = f.read()

        self.input = source
        self.tokens = []
        self.currentTokenIndex = 0
        self.currentToken = None
        self.tokenize()
        # reset to 0 so advance() indexes into the tokens list, not the input string
        self.currentTokenIndex = 0

        if self.tokens:
            self.currentToken = self.tokens[0]

    def hasMoreTokens(self):
        return self.currentTokenIndex < len(self.tokens) - 1

    def advance(self):
        if self.hasMoreTokens():
            self.currentTokenIndex += 1
            self.currentToken = self.tokens[self.currentTokenIndex]
            return self.currentToken
        return False


    
    
    









        