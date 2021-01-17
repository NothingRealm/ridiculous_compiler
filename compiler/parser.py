from ply.yacc import yacc
from .lex import tokens
from .nonTerminal import NonTerminal
from .codeGenerator import CodeGenerator
from .tables import explicit_type, update_symbols, get_array_index, index_name_from_str
from .code import code


precedence = (
    ("left", "AND", "OR"),
    ("left", "NOT"),
    ("left", "LT", "LE", "GT", "GE", "EQ", "NE"),
    ("right", "ASSIGN"),
    ("left", "SUM", "SUB"),
    ("left", "MUL", "DIV", "MOD"),
)

tempCount = -1


def new_temp():
    global tempCount
    tempCount += 1
    return "T" + str(tempCount)


############# Parser Methods ################


def p_program(p):
    "program : declist MAIN LRB RRB block"
    pass


def p_declist(p):
    """declist : declist dec
    | eps"""  # eps is equal to epsilon
    pass


def p_dec(p):
    """dec : vardec
    | funcdec"""
    pass


def p_vardec(p):
    "vardec : idlist COLON type SEMICOLON"
    p[0] = NonTerminal()
    p_type = p[3]
    for symbol in p[1].replacement().split(","):
        update_symbols(symbol, p_type)
    p[0].code = p_type + " " + p[1].replacement() + p[4]
    print(p[0].code)


def p_funcdec(p):
    """funcdec : FUNCTION ID LRB paramdecs RRB COLON type block
    | FUNCTION ID LRB paramdecs RRB block"""
    pass


def p_type(p):
    """type : INTEGER
    | FLOAT
    | BOOLEAN"""
    p[0] = p[1]


def p_iddec(p):
    """iddec : lvalue ASSIGN exp"""
    if not p[1].is_array:
        CodeGenerator.assign_lvalue(p)
    p[0].is_array = p[1].is_array


def p_iddec_single(p):
    "iddec : lvalue"
    p[0] = p[1]


def p_idlist(p):
    """idlist : idlist COMMA iddec"""
    p[0] = NonTerminal()
    p[0].in_place = p[1].replacement()
    if not p[3].is_array:
        p[0].in_place += p[2] + p[3].replacement()
    pass


def p_idlist_single(p):
    "idlist : iddec"
    p[0] = p[1]


def p_paramdecs(p):
    """paramdecs : paramdecslist
    | eps"""
    pass


def p_paramdecslist(p):
    """paramdecslist : paramdec
    | paramdecslist COMMA paramdec
    """
    pass


def p_paramdec(p):
    """paramdec : ID LSB RSB COLON type"""
    pass


def p_paramdec_single(p):
    "paramdec : ID COLON type"
    pass


def p_block(p):
    "block : LCB stmtlist RCB"
    p[0] = NonTerminal()
    p[0].code = p[1].code


def p_stmtlist(p):
    "stmtlist : stmtlist stmt"
    p[0] = NonTerminal()
    p[0].code = p[1].code + " " + p[2].code


def p_stmtlist_eps(p):
    "stmtlist : eps"
    p[0] = NonTerminal()


def p_lvalue(p):
    """lvalue : ID LRB explist RRB"""
    pass


def p_lvalue_single(p):
    "lvalue : ID"
    p[0] = NonTerminal()
    p[0].value = p[1]


def p_lvalue_array(p):
    "lvalue : ID LSB exp RSB"
    p[0] = NonTerminal()
    p[0].value = p[1] + p[2] + p[3].replacement() + p[4]
    p[0].is_array = True


def p_case(p):
    "case : WHERE const COLON stmtlist"
    pass


def p_cases(p):
    """cases : cases case
    | eps
    """
    pass


def p_stmt(p):
    """stmt : ostmt
    | cstmt"""
    p[0] = p[1]


def p_ostmt_while(p):
    "ostmt : WHILE LRB exp RRB ostmt"
    CodeGenerator._while(p)

def p_ostmt_pfor(p):
    "ostmt : FOR LRB ID IN ID RRB ostmt"
    CodeGenerator.python_type_for(p)


def p_ostmt_cfor(p):
    "ostmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB ostmt"
    CodeGenerator.c_type_for(p)



def p_ostmt_ifelse(p):
    "ostmt : IF LRB exp RRB cstmt elseiflist ELSE ostmt"
    CodeGenerator.if_with_else(p)


def p_ostmt_if(p):
    """ostmt : IF LRB exp RRB cstmt
    | IF LRB exp RRB ostmt"""
    p[0] = NonTerminal()
    p[0].code = "if (" + p[3].value + ") " + p[5].code


def p_cstmt_while(p):
    "cstmt : WHILE LRB exp RRB cstmt"
    CodeGenerator._while(p)


def p_cstmt_pfor(p):
    " cstmt : FOR LRB ID IN ID RRB cstmt"
    CodeGenerator.python_type_for(p)


def p_cstmt_cfor(p):
    "cstmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB cstmt"
    CodeGenerator.c_type_for(p)


def p_cstmt_ifelse(p):
    "cstmt : IF LRB exp RRB cstmt elseiflist ELSE cstmt"
    CodeGenerator.if_with_else(p)


def p_cstmt_simple(p):
    "cstmt : simple"
    p[0] = p[1]


def p_elseiflist(p):
    "elseiflist : elseiflist ELSEIF LRB exp RRB cstmt"
    p[0] = NonTerminal()
    p[0].code = p[1].code + " else (" + p[4].value + ")" + p[5].code


def p_elseiflist_eps(p):
    "elseiflist : eps"
    p[0] = NonTerminal()


def p_simple(p):
    """simple : block
    | vardec"""
    pass


def p_simple_switch(p):
    "simple :  ON LRB exp RRB LCB cases RCB SEMICOLON"
    p[0] = NonTerminal()
    p[0].code = "switch (" + p[3].value + ") {" + p[6].code + "}"


def p_simple_return(p):
    "simple : RETURN exp SEMICOLON"
    CodeGenerator.simple_simple(p, p[1])


def p_simple_semicolon(p):
    "simple : exp SEMICOLON"
    pass


def p_print(p):
    "simple : PRINT LRB ID RRB SEMICOLON"
    p[0] = NonTerminal()
    p[0].code = """printf("%d", {});""".format(p[3])
    print(p[0].code)


def p_relop(p):
    """relop : GT
    | GE
    | LT
    | LE
    | EQ
    | NE"""
    p[0] = p[1]


def p_exp(p):
    """exp : exp relop exp %prec LT"""
    CodeGenerator.arithmetic_code(p, new_temp())


def p_exp_lvalue(p):
    "exp : lvalue %prec OR"
    p[0] = p[1]


def p_exp_minus(p):
    "exp : SUB exp"
    p[0] = NonTerminal()
    p[0].value = "-" + p[2].replacement()


def p_exp_not(p):
    "exp : NOT exp"
    p[0] = NonTerminal()
    p[0].value = "!" + p[2].replacement()


def p_exp_rbracket(p):
    "exp : LRB exp RRB"
    # TODO: This if is only for unseen circumstances, should such events lack to present themselves, remove it.
    if " " in p[2].replacement():
        p[0] = NonTerminal()
        p[0].in_place = p[1] + p[2].replacement() + p[3]
    else:
        p[0] = p[2]


def p_exp_lvalue_assign(p):
    "exp : lvalue ASSIGN exp"
    if p[1].is_array:
        index, name = index_name_from_str(p[1].value)
        init_index = get_array_index(name)
        index += init_index
        p[1].value = "array[" + str(index) + "]"
    CodeGenerator.assign_lvalue(p)


def p_exp_const(p):
    "exp : const"
    p[0] = p[1]


def p_exp_binop(p):
    "exp : exp operator exp %prec MUL"
    CodeGenerator.arithmetic_code(p, new_temp())


def p_operator(p):
    """operator : AND
    | OR
    | SUM
    | SUB
    | MUL
    | DIV
    | MOD"""
    p[0] = p[1]


def p_const(p):
    """const : INTEGERNUMBER
    | FLOATNUMBER
    | TRUE
    | FALSE"""
    p[0] = NonTerminal()
    p[0].value = p[1]
    if p[1] == True:
        p[0].value = 1
    elif p[1] == False:
        p[0].value = 0
    if p.slice[1].type == "INTEGERNUMBER":
        p[0].implicit_type = "int"
    elif p.slice[1].type == "FLOATNUMBER":
        p[0].implicit_type = "float"
    else:
        p[0].implicit_type = "bool"


def p_explist(p):
    """explist : exp
    | explist COMMA exp
    | eps"""
    pass


def p_eps(p):
    "eps :"
    pass


def p_error(p):
    if p:
        raise Exception("ParsingError: invalid grammar at ", p)


parser = yacc()
