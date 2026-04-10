"""jack compilation engine (recursive descent parser)"""

from typing import List, Optional
from tokenizer import Token, TokenType
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class CompilationEngine:
    
    def __init__(self, toks: List[Token]):
        # tokens + pointer (where we are in the list)
        self.toks = toks
        self.i = 0
        
        # root xml node
        self.root = Element("class")
    
    def cur(self) -> Optional[Token]:
        # current token or None if we ran out
        return self.toks[self.i] if self.i < len(self.toks) else None
    
    def adv(self) -> Token:
        # move forward + return token
        tok = self.cur()
        if not tok:
            raise IndexError("ran outta tokens fr")
        self.i += 1
        return tok
    
    def eat(self, val: str) -> Token:
        # make sure token matches what we expect
        tok = self.cur()
        if not tok or tok.value != val:
            raise SyntaxError(f"expected '{val}' but got '{tok.value if tok else 'EOF'}'")
        return self.adv()
    
    def eat_kw(self, kw: str) -> Token:
        # same but for keywords
        tok = self.cur()
        if not tok or tok.type != TokenType.KEYWORD or tok.value != kw:
            raise SyntaxError(f"expected keyword '{kw}'")
        return self.adv()
    
    def add_tok(self, parent: Element, tok: Token):
        # add token into xml
        e = SubElement(parent, tok.type.value.lower())
        e.text = f" {tok.value} "
    
    def eat_add(self, parent: Element, val: str):
        # expect + add in one line
        self.add_tok(parent, self.eat(val))
    
    def eat_kw_add(self, parent: Element, kw: str):
        self.add_tok(parent, self.eat_kw(kw))
    
    # ---------------- core compile ----------------
    
    def compile_class(self) -> Element:
        self.eat_kw_add(self.root, 'class')
        self.add_tok(self.root, self.adv())  # class name
        self.eat_add(self.root, '{')
        
        # class vars
        while self.cur() and self.cur().value in ['static', 'field']:
            self.compile_class_var(self.root)
        
        # funcs / methods
        while self.cur() and self.cur().value in ['constructor', 'function', 'method']:
            self.compile_subroutine(self.root)
        
        self.eat_add(self.root, '}')
        return self.root
    
    def compile_class_var(self, parent: Element):
        e = SubElement(parent, "classVarDec")
        
        self.add_tok(e, self.adv())  # static/field
        self._type(e)
        self.add_tok(e, self.adv())  # var name
        
        # more vars
        while self.cur() and self.cur().value == ',':
            self.add_tok(e, self.adv())
            self.add_tok(e, self.adv())
        
        self.eat_add(e, ';')
    
    def compile_subroutine(self, parent: Element):
        e = SubElement(parent, "subroutineDec")
        
        self.add_tok(e, self.adv())  # constructor/function/method
        
        # return type
        if self.cur() and self.cur().value == 'void':
            self.add_tok(e, self.adv())
        else:
            self._type(e)
        
        self.add_tok(e, self.adv())  # name
        self.eat_add(e, '(')
        
        self.compile_params(e)
        self.eat_add(e, ')')
        
        self.compile_body(e)
    
    def compile_params(self, parent: Element):
        e = SubElement(parent, "parameterList")
        
        # empty params
        if self.cur() and self.cur().value == ')':
            return
        
        self._type(e)
        self.add_tok(e, self.adv())
        
        while self.cur() and self.cur().value == ',':
            self.add_tok(e, self.adv())
            self._type(e)
            self.add_tok(e, self.adv())
    
    def compile_body(self, parent: Element):
        e = SubElement(parent, "subroutineBody")
        self.eat_add(e, '{')
        
        # local vars
        while self.cur() and self.cur().value == 'var':
            self.compile_var(e)
        
        self.compile_stmts(e)
        self.eat_add(e, '}')
    
    def compile_var(self, parent: Element):
        e = SubElement(parent, "varDec")
        
        self.eat_kw_add(e, 'var')
        self._type(e)
        self.add_tok(e, self.adv())
        
        while self.cur() and self.cur().value == ',':
            self.add_tok(e, self.adv())
            self.add_tok(e, self.adv())
        
        self.eat_add(e, ';')
    
    def compile_stmts(self, parent: Element):
        e = SubElement(parent, "statements")
        
        # loop through statements till something else shows up
        while self.cur():
            fn = {
                'let': self.compile_let,
                'if': self.compile_if,
                'while': self.compile_while,
                'do': self.compile_do,
                'return': self.compile_return
            }.get(self.cur().value)
            
            if not fn:
                break
            fn(e)
    
    # ---------------- statements ----------------
    
    def compile_let(self, parent: Element):
        e = SubElement(parent, "letStatement")
        
        self.eat_kw_add(e, 'let')
        self.add_tok(e, self.adv())
        
        # array access
        if self.cur() and self.cur().value == '[':
            self.eat_add(e, '[')
            self._expr(e)
            self.eat_add(e, ']')
        
        self.eat_add(e, '=')
        self._expr(e)
        self.eat_add(e, ';')
    
    def compile_if(self, parent: Element):
        e = SubElement(parent, "ifStatement")
        
        self.eat_kw_add(e, 'if')
        self.eat_add(e, '(')
        self._expr(e)
        self.eat_add(e, ')')
        
        self.eat_add(e, '{')
        self.compile_stmts(e)
        self.eat_add(e, '}')
        
        # optional else
        if self.cur() and self.cur().value == 'else':
            self.eat_kw_add(e, 'else')
            self.eat_add(e, '{')
            self.compile_stmts(e)
            self.eat_add(e, '}')
    
    def compile_while(self, parent: Element):
        e = SubElement(parent, "whileStatement")
        
        self.eat_kw_add(e, 'while')
        self.eat_add(e, '(')
        self._expr(e)
        self.eat_add(e, ')')
        
        self.eat_add(e, '{')
        self.compile_stmts(e)
        self.eat_add(e, '}')
    
    def compile_do(self, parent: Element):
        e = SubElement(parent, "doStatement")
        
        self.eat_kw_add(e, 'do')
        self._call(e)
        self.eat_add(e, ';')
    
    def compile_return(self, parent: Element):
        e = SubElement(parent, "returnStatement")
        
        self.eat_kw_add(e, 'return')
        
        if self.cur() and self.cur().value != ';':
            self._expr(e)
        
        self.eat_add(e, ';')
    
    # ---------------- helpers ----------------
    
    def _type(self, parent: Element):
        # we just move along and add it in either case
        self.add_tok(parent, self.adv())
    
    def _expr(self, parent: Element):
        e = SubElement(parent, "expression")
        
        # not a full parser, just enough to get the right tokens in the right places
        while self.cur() and self.cur().value not in [';', ')', ',', ']', '}']:
            if self.cur().value not in ['{', '(', '[']:
                self.add_tok(e, self.adv())
            else:
                break
    
    def _call(self, parent: Element):
        e = SubElement(parent, "subroutineCall")
        
        while self.cur() and self.cur().value != ';':
            self.add_tok(e, self.adv())
    
    def to_xml(self) -> str:
        # make it readable 
        raw = tostring(self.root, encoding='unicode')
        dom = minidom.parseString(raw)
        return dom.toprettyxml(indent="  ")
