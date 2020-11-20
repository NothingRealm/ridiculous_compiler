from ply.yacc import yacc
from .lex import tokens

precedence = (
    ("left", "AND", "OR"),
    ("left", "NOT"),
    ("left", "LT", "LE", "GT", "GE", "EQ", "NE"),
    ("right", "ASSIGN"),
    ("left", "SUM", "SUB"),
    ("left", "MUL", "DIV", "MOD"),
)


def p_program(p):
    "program : declist MAIN LRB RRB block"
    print("p_program")


def p_declist(p):
    # "declist -> dec" is redundant
    """declist : declist dec
    | eps"""  # eps is equal to epsilon
    print("p_declist")


def p_dec(p):
    """dec : vardec
    | funcdec"""
    print("p_dec")


def p_vardec(p):
    "vardec : idlist COLON type"
    print("p_vardec")


def p_funcdec(p):
    """funcdec : FUNCTION ID LRB paramdecs RRB COLON type block
    | FUNCTION ID LRB paramdecs RRB block"""
    print("p_funcdec")


def p_type(p):
    """type : INTEGER
    | FLOAT
    | BOOLEAN"""
    print("p_type")


def p_iddec(p):
    """iddec : lvalue
    | ID ASSIGN exp
    """
    print("p_iddec")


def p_idlist(p):
    """idlist : iddec
    | idlist COMMA iddec
    """
    print("p_idlist")


def p_paramdecs(p):
    """paramdecs : paramdecslist
    | eps"""
    print("p_paramdecs")


def p_paramdecslist(p):
    """paramdecslist : paramdec
    | paramdecslist COMMA paramdec
    """
    print("p_paramdecslist")


def p_paramdec(p):
    """paramdec : ID COLON type
    | ID LSB RSB COLON type"""
    print("p_paramdec")


def p_block(p):
    "block : LCB stmtlist RCB"
    print("p_block")


def p_stmtlist(p):
    """stmtlist : stmtlist stmt
    | eps"""
    print("p_stmtlist")


def p_lvalue(p):
    """lvalue : ID
    | ID LSB exp RSB"""
    print("p_lvalue")


def p_case(p):
    "case : WHERE const COLON stmtlist"
    print("p_case")


def p_cases(p):
    """cases : cases case
    | eps
    """
    print("p_cases")


def p_stmt(p):
    """stmt : RETURN exp SEMICOLON
    | exp SEMICOLON
    | block
    | vardec
    | WHILE LRB exp LRB stmt
    | ON LRB exp RRB LCB cases RCB SEMICOLON
    | FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt
    | FOR LRB ID IN RRB stmt
    | IF LRB exp RRB stmt elseiflist
    | IF LRB exp RRB stmt elseiflist ELSE stmt
    | PRINT LRB ID RRB SEMICOLON"""
    print("p_stmt")


def p_elseiflist(p):
    """elseiflist : elseiflist ELSEIF LRB exp RRB stmt
    | eps"""
    print("p_elseiflist")


def p_relop(p):
    """relop : GT
    | GE
    | LT
    | LE
    | EQ
    | NE"""
    print("p_relop")


def p_exp(p):
    """exp : lvalue ASSIGN exp
    | exp operator exp
    | exp relop exp
    | const
    | lvalue
    | ID LRB explist RRB
    | LRB exp RRB
    | SUB exp
    | NOT exp"""
    print("p_operator")


def p_operator(p):
    """operator : AND
    | OR
    | SUM
    | SUB
    | MUL
    | DIV
    | MOD"""
    print("p_operator")


def p_const(p):
    """const : INTEGERNUMBER
    | FLOATNUMBER
    | TRUE
    | FALSE"""
    print("p_const")


def p_explist(p):
    """explist : exp
    | explist COMMA exp
    | eps"""
    print("p_explist")


def p_eps(p):
    "eps :"
    print("p_eps")
    # pass


def p_error(p):
    # print(p.value)
    if p:
        raise Exception("ParsingError: invalid grammar at ", p)


parser = yacc()