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
        if self.count_errors >= 3:
            sys.exit(0)

    def retornaPonteiro(self):
        if(self.lookahead.decode('ascii') != ''):
            self.n_column -= 1
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
            self.n_column += 1

            if(estado == 1):
                if(char == ''):
                    return Token(Tag.EOF, 'EOF', self.n_line, self.n_column)
                elif(char == ' ' or char == '\r' or char == '\t'):
                    estado = 1
                elif(char == '\n'):
                    self.n_line += 1
                    self.n_column = 1
                    estado = 1
                elif(char == '/'):
                    estado = 2
                elif(char == '='):
                    estado = 3
                elif(char == '!'):
                    estado = 4
                elif(char == '<'):
                    estado = 5
                elif(char == '>'):
                    estado = 6
                elif(char == '+'):
                    estado = 7
                elif(char == '-'):
                    estado = 8
                elif(char == '*'):
                    estado = 9
                elif(char == '('):
                    estado = 10
                elif(char == ')'):
                    estado = 11
                elif(char == '{'):
                    estado = 12
                elif(char == '}'):
                    estado = 13
                elif(char == ','):
                    estado = 14
                elif(char == ';'):
                    estado = 15
                elif(char == '\"'):
                    estado = 16
                elif(char.isdigit()):
                    lexema += char
                    estado = 17
                elif(char.isalpha()):
                    lexema += char
                    estado = 18
                else:
                    self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                    return None

            elif(estado == 2):
                if((len(lexema) == 0) and char == '/'):
                    self.n_line += 1
                    self.input_file.readline()
                    estado = 1
                    lexema = ''
                    continue
                if(char == '*'):
                    lexema += char
                    estado = 20
                if(len(lexema) == 0):
                    self.retornaPonteiro()
                    return Token(Tag.OP_DIV, "/", self.n_line, self.n_column - 1)

            elif(estado == 20):
                if(char == ''):
                    self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                    self.contadorErros += 1
                    continue
                lexema += char
                if(char == '\n'):
                    self.n_column = 1
                    self.n_line += 1
                if(char == '/'):
                    if('*/' not in lexema):
                        continue
                    else:
                        estado = 1
                        lexema = ''
                        continue

            elif(estado == 3):
                if(char == '='):
                    return Token(Tag.OP_EQ, '==', self.n_line, self.n_column - 2)
                self.retornaPonteiro()
                return Token(Tag.OP_ATRIB, '=', self.n_line, self.n_column - 1)

            elif(estado == 4):
                if(char == '='):
                    return Token(Tag.OP_NE, '!=', self.n_line, self.n_column - 2)
                self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                return None

            elif(estado == 5):
                if(char == '='):
                    return Token(Tag.OP_LE, '<=', self.n_line, self.n_column - 2)
                self.retornaPonteiro()
                return Token(Tag.OP_LT, '<', self.n_line, self.n_column - 1)

            elif(estado == 6):
                if(char == '='):
                    return Token(Tag.OP_GE, '>=', self.n_line, self.n_column - 2)
                self.retornaPonteiro()
                return Token(Tag.OP_GT, '>', self.n_line, self.n_column - 1)

            elif(estado == 7):
                self.retornaPonteiro()
                return Token(Tag.OP_AD, '+', self.n_line, self.n_column - 1)

            elif(estado == 8):
                self.retornaPonteiro()
                return Token(Tag.OP_MIN, '-', self.n_line, self.n_column - 1)

            elif(estado == 9):
                self.retornaPonteiro()
                return Token(Tag.OP_MUL, '*', self.n_line, self.n_column - 1)

            elif(estado == 10):
                self.retornaPonteiro()
                return Token(Tag.SMB_OPA, '(', self.n_line, self.n_column - 1)

            elif(estado == 11):
                self.retornaPonteiro()
                return Token(Tag.SMB_CPA, ')', self.n_line, self.n_column - 1)

            elif(estado == 12):
                self.retornaPonteiro()
                return Token(Tag.SMB_OBC, '{', self.n_line, self.n_column - 1)

            elif(estado == 13):
                self.retornaPonteiro()
                return Token(Tag.SMB_CBC, '}', self.n_line, self.n_column - 1)

            elif(estado == 14):
                self.retornaPonteiro()
                return Token(Tag.SMB_COM, ',', self.n_line, self.n_column - 1)

            elif(estado == 15):
                self.retornaPonteiro()
                return Token(Tag.SMB_SEM, ';', self.n_line, self.n_column - 1)

            elif(estado == 16):
                if(char.isascii()):
                    lexema += char
                    estado = 160
                else:
                    self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                    return None

            elif(estado == 160):
                if(char == "\""):
                    return Token(Tag.CONST_CHAR, lexema, self.n_line, self.n_column - len(lexema))
                elif(char == '\n'):
                    self.sinalizaErroLexico('Erro devido a não fecha da string antes de uma quebra de linha')
                    return None
                elif(char == ''):
                    self.sinalizaErroLexico('Erro devido a não fecha da string antes de uma quebra de linha')
                    return None
                elif(char.isascii()):
                    lexema += char
                else:
                    self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                    return None

            elif(estado == 17):
                if(char.isdigit()):
                    lexema += char
                elif(char == "."):
                    lexema += char
                    estado = 170
                else:
                    self.retornaPonteiro()
                    return Token(Tag.CONST_NUM, lexema, self.n_line, self.n_column - len(lexema))

            elif(estado == 170):
                if(char.isdigit()):
                    lexema += char
                    estado = 171
                else:
                    self.sinalizaErroLexico(f'Caractere inválido [{char}] na linha {str(self.n_line)} e coluna {str(self.n_column)}')
                    return None

            elif(estado == 171):
                if(char.isdigit()):
                    lexema += char
                else:
                    self.retornaPonteiro()
                    return Token(Tag.CONST_NUM, lexema, self.n_line, self.n_column - len(lexema))

            elif(estado == 18):
                if(char.isalnum()):
                    lexema += char
                else:
                    self.retornaPonteiro()
                    token = self.symbol_table.getToken(lexema)
                    if(token is None):
                        token = Token(Tag.ID, lexema, self.n_line, self.n_column - len(lexema))
                        self.symbol_table.addToken(lexema, token)
                    return token
