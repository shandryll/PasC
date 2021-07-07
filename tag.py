from enum import Enum

class Tag(Enum):
    # Fim de arquivo
    EOF = -1

    # Keywords
    KW_PROGRAM = 1
    KW_IF = 2
    KW_ELSE = 3
    KW_WHILE = 4
    KW_WRITE = 5
    KW_READ = 6
    KW_NUM = 7
    KW_CHAR = 8
    KW_NOT = 9
    KW_OR = 10
    KW_AND = 11

    # Operators
    OP_EQ = 12
    OP_NE = 13
    OP_GT = 14
    OP_LT = 15
    OP_GE = 16
    OP_LE = 17
    OP_AD = 18
    OP_MIN = 19
    OP_MUL = 20
    OP_DIV = 21
    OP_ATRIB = 22

    # Symbols
    SMB_OKE = 23
    SMB_CKE = 24
    SMB_OPA = 25
    SMB_CPA = 26
    SMB_COM = 27
    SMB_SEM = 28

    # Identifier
    ID = 29

    # Literal
    LIT = 30

    # Const
    CONST_NUM = 35
    CONST_CHAR = 36

    # Types
    TP_VOID = 37
    TP_NUM = 38
    TP_CHAR = 39
    TP_BOOL = 40
    TP_ERROR = 41
