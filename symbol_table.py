from token import Token
from tag import Tag

class SymbolTable:
    def __init__(self):
        self.dict_symbol = {}
        self.dict_symbol['program'] = Token(Tag.KW_PROGRAM, 'program', 0, 0)
        self.dict_symbol['if'] = Token(Tag.KW_IF, 'if', 0, 0)
        self.dict_symbol['else'] = Token(Tag.KW_ELSE, 'else', 0, 0)
        self.dict_symbol['while'] = Token(Tag.KW_WHILE, 'while', 0, 0)
        self.dict_symbol['write'] = Token(Tag.KW_WRITE, 'write', 0, 0)
        self.dict_symbol['read'] = Token(Tag.KW_READ, 'read', 0, 0)
        self.dict_symbol['num'] = Token(Tag.KW_NUM, 'num', 0, 0)
        self.dict_symbol['char'] = Token(Tag.KW_CHAR, 'char', 0, 0)
        self.dict_symbol['not'] = Token(Tag.KW_NOT, 'not', 0, 0)
        self.dict_symbol['or'] = Token(Tag.KW_OR, 'or', 0, 0)
        self.dict_symbol['and'] = Token(Tag.KW_AND, 'and', 0, 0)

    def getToken(self, lexema):
      token = self.dict_symbol.get(lexema)
      return token

    def addToken(self, lexema, token):
        self.dict_symbol[lexema] = token

    def printTS(self):
        for k, t in (self.dict_symbol.items()):
            print(k, ":", t.toString())
