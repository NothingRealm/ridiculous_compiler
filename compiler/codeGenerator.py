from .nonTerminal import NonTerminal
from .tables import explicit_type, update_output_table


class CodeGenerator:
    @staticmethod
    def infer_type(p1, p3):
        return (
            explicit_type(p1)
            or explicit_type(p3)
            or p1.implicit_type
            or p3.implicit_type
            or "int"
        )

    @staticmethod
    def arithmetic_code(p, temp):
        p[0] = NonTerminal()
        p[0].in_place = temp
        update_output_table(temp, "int")
        # p[0].implicit_type = CodeGenerator.infer_type(p[1], p[3])
        p[0].code = p[0].in_place + " = "
        p[0].code += p[1].replacement() + " " + p[2] + " " + p[3].replacement() + ";"
        print(p[0].code)

    @staticmethod
    def assign_explicit_type(p):
        pass

    @staticmethod
    def assign_lvalue(p):
        p[0] = NonTerminal()
        p_type = str(explicit_type(p[1])) + " "
        if p_type:
            p_type = ""
        else:
            p_type = p[1].implicit_type + " "
        p[0].code = p_type + p[1].value + p[2] + p[3].replacement() + ";"
        p[0].value = p[1].value
        print(p[0].code)

    @staticmethod
    def simple_simple(p, ret=""):
        p[0] = NonTerminal()
        if p[2].value:
            p[0].code = p[1] + " " + str(p[2].value) + p[3]
        else:
            p[0].code = p[1] + " 0" + p[3]
        print(p[0].code)

    @staticmethod
    def if_with_else(p):
        p[0] = NonTerminal()
        p[0].code = (
            "if ("
            + p[3].value
            + ") "
            + p[5].code
            + " "
            + p[6].code
            + " else "
            + p[8].code
        )

    @staticmethod
    def c_type_for(p):
        p[0] = NonTerminal()
        p[0].code = (
            "for (" + p[3].value + ";" + p[5].value + ";" + p[7].value + ") " + p[9].code
        )
    
    @staticmethod
    def python_type_for(p):
        p[0] = NonTerminal()
        p[0].code = "for (" + p[3] + " in " + p[5] + ") " + p[7].code

    @staticmethod
    def _while(p):
        p[0] = NonTerminal()
        p[0].code = "while (" + p[3].value + ") " + p[5].code