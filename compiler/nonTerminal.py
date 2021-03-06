from collections import OrderedDict

tempCount = -1
labelCount = -1

def new_temp():
    global tempCount
    tempCount += 1
    return "T" + str(tempCount)

def new_label():
    global labelCount
    labelCount += 1
    return "L" + str(labelCount)




class NonTerminal:
    def __init__(self):
        self.value = ""
        self.code = ""
        self.in_place = ""
        self.is_array = False
        self.relop_parts = []
        self.iddec_assigns = {}
        self.bool_gen = False

    def replacement(self):
        return str(self.value) if self.value != "" else self.in_place

    def bool_replacement(self):
        return str(self.value).split()[-1] if self.value else self.in_place