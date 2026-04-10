"""
Basically this takes raw Jack code and breaks it down into tokens
so the compiler can actually understand what's going on.
"""

import re
from enum import Enum
from typing import List, Optional


class TokenType(Enum):
    # Different types of tokens we can run into
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class Token:
    # Just a simple container for a token
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


class Tokenizer:
    """
    This is where everything happens.
    Takes in Jack source code and turns it into a list of tokens.
    """

    # All the keywords in Jack
    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return'
    }

    # All valid symbols
    SYMBOLS = set('{}()[].,;=+-*/<>&|~')

    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens: List[Token] = []
        self._current_pos = 0

        # start tokenizing immediately
        self._tokenize()

    def _skip_whitespace(self):
        """
        Skips spaces, new lines, and comments
        (basically anything we don't care about)
        """
        while self._current_pos < len(self.source):
            char = self.source[self._current_pos]

            # whitespace
            if char in ' \t\n\r':
                self._current_pos += 1
                continue

            # line comments //
            if self._current_pos + 1 < len(self.source) and \
               self.source[self._current_pos:self._current_pos + 2] == '//':

                while self._current_pos < len(self.source) and \
                      self.source[self._current_pos] != '\n':
                    self._current_pos += 1
                continue

            # block comments /* */
            if self._current_pos + 1 < len(self.source) and \
               self.source[self._current_pos:self._current_pos + 2] == '/*':

                self._current_pos += 2
                while self._current_pos + 1 < len(self.source):
                    if self.source[self._current_pos:self._current_pos + 2] == '*/':
                        self._current_pos += 2
                        break
                    self._current_pos += 1
                continue

            break

    def _tokenize_string(self) -> Optional[Token]:
        # handles stuff inside "quotes"
        if self.source[self._current_pos] != '"':
            return None

        self._current_pos += 1
        string_value = ""

        while self._current_pos < len(self.source):
            char = self.source[self._current_pos]

            if char == '"':
                self._current_pos += 1
                return Token(TokenType.STRING_CONST, string_value)

            string_value += char
            self._current_pos += 1

        raise SyntaxError("String never got closed...")

    def _tokenize_number(self) -> Optional[Token]:
        # integers only
        if not self.source[self._current_pos].isdigit():
            return None

        number = ""

        while self._current_pos < len(self.source) and \
              self.source[self._current_pos].isdigit():
            number += self.source[self._current_pos]
            self._current_pos += 1

        int_val = int(number)

        if int_val > 32767:
            raise ValueError(f"{int_val} is too big (max is 32767)")

        return Token(TokenType.INT_CONST, number)

    def _tokenize_identifier_or_keyword(self) -> Optional[Token]:
        # variable names OR keywords
        if not (self.source[self._current_pos].isalpha() or
                self.source[self._current_pos] == '_'):
            return None

        identifier = ""

        while self._current_pos < len(self.source) and \
              (self.source[self._current_pos].isalnum() or
               self.source[self._current_pos] == '_'):

            identifier += self.source[self._current_pos]
            self._current_pos += 1

        if identifier in self.KEYWORDS:
            return Token(TokenType.KEYWORD, identifier)

        return Token(TokenType.IDENTIFIER, identifier)

    def _tokenize_symbol(self) -> Optional[Token]:
        # single character symbols
        if self.source[self._current_pos] not in self.SYMBOLS:
            return None

        symbol = self.source[self._current_pos]
        self._current_pos += 1

        return Token(TokenType.SYMBOL, symbol)

    def _tokenize(self):
        # main loop, keeps going until we finish the file
        while self._current_pos < len(self.source):
            self._skip_whitespace()

            if self._current_pos >= len(self.source):
                break

            token = (
                self._tokenize_string() or
                self._tokenize_number() or
                self._tokenize_identifier_or_keyword() or
                self._tokenize_symbol()
            )

            if token:
                self.tokens.append(token)
            else:
                raise SyntaxError(
                    f"Something weird popped up: {self.source[self._current_pos]}"
                )

    def get_tokens(self) -> List[Token]:
        # returns everything we parsed
        return self.tokens

    def peek_token(self, offset: int = 0) -> Optional[Token]:
        """
        lets you look ahead without actually using the token yet
        """
        pos = len([t for t in self.tokens if hasattr(self, '_consumed_count')]) + offset

        if 0 <= pos < len(self.tokens):
            return self.tokens[pos]

        return None
