import sys

from symbol_table import SymbolTable
from tag import Tag
from token import Token

class Lexer():
    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 1
            self.count_errors = 0
            self.symbol_table = SymbolTable()
        except IOError:
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)

    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)

    def sinalizaErroLexico(self, message):
        print("\n\n[Erro Lexico]: ", message, "\n")
        self.count_errors = self.count_errors + 1
        if self.count_errors >= 5:
            sys.exit(0)

    def retornaPonteiro(self):
        if(self.lookahead.decode('ascii') != ''):
            self.input_file.seek(self.input_file.tell()-1)

    def printTS(self):
        self.symbol_table.printTS()

    def proxToken(self):
        estado = 1
        lexema = ""
        char = '\u0000'

        while(True):
            self.lookahead = self.input_file.read(1)
            char = self.lookahead.decode('ascii')

            if(estado == 1):
                if(char == ''):
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
                elif(char == ' ' or char == '\r'):
                    estado = 1
                elif(char == '\t'):
                    self.n_column = self.n_column + 3
                    self.estado = 1
                elif(char == '\n'):
                    self.n_line = self.n_line + 1
                    self.n_column = 1
                    estado = 1
                elif(char == '='):
                    estado = 2
                elif(char == '!'):
                    estado = 4
                elif(char == '<'):
                    estado = 6
                elif(char == '>'):
                    estado = 9
                elif(char.isdigit()):
                    lexema += char
                    estado = 12
                elif(char.isalpha()):
                    lexema += char
                    estado = 14
                elif(char == '/'):
                    estado = 16
                elif(char == '+'):
                    return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
                elif(char == '-'):
                    return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
                elif(char == '*'):
                    return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)
                elif(char == '/'):
                    return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)
                elif(char == '{'):
                    return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)
                elif(char == '}'):
                    return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)
                elif(char == '('):
                    return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
                elif(char == ')'):
                    return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
                elif(char == ','):
                    return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
                elif(char == ';'):
                    return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + char + "] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))
                    return None

            elif(estado == 2):
                if(char == '='):
                    return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
                else:
                    self.retornaPonteiro()
                    return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)

            elif(estado == 4):
                if(char == '='):
                    return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)
                self.sinalizaErroLexico("Caractere invalido [" + char + "] na linha " + str(self.n_line) + " e coluna " + str(self.n_column))
                return None

            elif(estado == 6):
                if(char == '='):
                    return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)
                self.retornaPonteiro()
                return Token(Tag.OP_LT, "<", self.n_line, self.n_column)

            elif(estado == 9):
                if(char == '='):
                    return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)
                self.retornaPonteiro()
                return Token(Tag.OP_GT, ">", self.n_line, self.n_column)

            elif(estado == 12):
                if(char.isdigit()):
                    lexema += char
                else:
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)

            elif(estado == 14):
                if(char.isalnum()):
                    lexema += char
                else:
                    self.retornaPonteiro()
                    token = self.symbol_table.getToken(lexema)
                    if(token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                        self.symbol_table.addToken(lexema, token)
                    token.setLinha(self.n_line)
                    token.setColuna(self.n_column)
                    return token
