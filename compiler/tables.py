#### Symbol Table ####

class SymbolRow:
    def __init__(self, p_type=None, arrayIndex=None):
        self.p_type = p_type
        self.arrayIndex = arrayIndex


symbol_table = {}
output_table = {}


def explicit_type(p):
    try:
        return symbol_table.get(p.value).p_type
    except Exception:
        return None


def update_symbols(item, p_type, arrayIndex=None):
    symbol_table.update({item: SymbolRow(p_type, arrayIndex)})
    if not arrayIndex:
        update_output_table(item, p_type)

def update_output_table(item, p_type):
    output_table.update({item: p_type})

def list_variables():
    variables = []
    for key, value in output_table.items():
        variables.append(key)
    return variables


##### Array Table #####

arrayIndex = 0
array_table = {}


def new_array(name, size):
    global arrayIndex
    array_table.update({name: [arrayIndex, size]})
    arrayIndex += size


def get_array_index(name):
    row = array_table.get(name)
    if row:
        return row[0]
    return -1

def get_array_size(name):
    row = array_table.get(name)
    if row:
        row[1]
    return 0

def index_name_from_str(string):
    start = string.find("[") + 1
    finish = string.find("]")
    result = string[start:finish]
    if result.isdigit():
        result = int(result)
    return result, string[0 : start - 1]

##### Assign Table ####
assign_table = {}

assignCount = -1

def new_assign_label():
    global assignCount
    assignCount += 1
    return "assign" + str(assignCount)

def new_assign(p):
    label = new_assign_label()
    assign_table.update({
        label : p
    })
    return label

def assign_table_keys():
    return assign_table.keys()

def assign_table_val(key):
    return assign_table.get(key)
    # return assign_table.get(key)

def assign_table_pop(key):
    assign_table.pop(key)