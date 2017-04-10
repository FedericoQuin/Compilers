from antlr4.error.ErrorListener import ErrorListener

toHumanLanguage = {
    "program" : "program",
    "functiondecl" : "function declaration",
    "initialargument" : "function argument",
    "argument" : "function argument",
    "arguments" : "function argument",
    "function_body" : "function body",
    "statements" : "statement",
    "statement" : "statement",
    "expression" : "expression",
    "ifelse" : "if-else-statement",
    "declaration" : "declaration",
    "while_loop" : "while loop",
    "for_loop" : "for loop",
    "break_stmt" : "break statement",
    "continue_stmt" : "continue statement",
    "return_stmt" : "return statement",
    "add_sub" : "expression",
    "mul_div" : "expression",
    "bracket_expression" : "expression",
    "lvalue_identifier" : "lvalue",
    "rvalue_identifier" : "rvalue",
    "else_statement" : "else statement",
    "firstcondition" : "condition",
    "first_true_statements" : "statement",
    "first_true_statement" : "statement",
    "first_false_statement" : "statement",
    "first_false_statements" : "statement",
    "condition" : "condition",
    "condition_and" : "condition",
    "condition_not" : "condition",
    "bracket_condition" : "condition",
    "comparison" : "comparison",
    "comparator" : "comparator",
    "first_while_statements" : "statement",
    "first_while_statement" : "statement",
    "first_while_condition" : "condition",
    "first_for_statements" : "statement",
    "first_stmt_for" : "first for statement",
    "second_stmt_for" : "second for statement",
    "third_stmt_for" : "third for statement",
    "lvalue" : "lvalue",
    "rvalue" : "rvalue",
    "numericalvalue" : "integer / floating point number",
    "intvalue" : "integer",
    "floatvalue" : "floating point number",
    "digits" : "integer / floating point number",
    "returntype" : "type",
    "dec_type" : "type",
    "ptr" : "pointer",
    "function" : "function"
    }

class MyErrorListener( ErrorListener ):

    def __init__(self, filename):
        super(MyErrorListener, self).__init__()

        with open(filename, 'r') as myfile:
            self.data = myfile.read().split("\n")


    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()[0]

        ex_msg = str(line) + ":" + str(column) + ": " + "Error while/after parsing " + toHumanLanguage[str(stack)] + "\n"
        ex_msg += str(self.data[line - 1]) + "\n"

        tabCount = self.data[line - 1].count("\t")

        ex_msg += str(tabCount * "\t")
        ex_msg += str((column - tabCount) * " ")
        ex_msg += "^" + "\n"

        if msg[-len("\'<EOF>\'"):] == "\'<EOF>\'":
            allData = "\n".join(self.data)
            if matching_braces(allData, "(", ")") and matching_braces(allData, "{", "}"):
                ex_msg += msg
            else:
                ex_msg += "Braces don't match"
        elif msg[0:len("no viable")] == "no viable":
            if matching_braces(str(self.data[line - 1]), "(", ")") and matching_braces(str(self.data[line - 1]), "{", "}"):
                ex_msg += msg
            else:
                ex_msg += "Braces don't match"
        else:
            ex_msg += msg + "\n"


        

        

        raise Exception(ex_msg)

def matching_braces(string, lbracket, rbracket):
    left_bracket = string.find(lbracket)
    right_bracket = string.find(rbracket)

    if left_bracket != -1 and right_bracket != -1:
        if left_bracket >= right_bracket:
            return False
        else:
             string = string[:right_bracket] + string[(right_bracket + 1):]
             string = string[:left_bracket] + string[(left_bracket + 1):]
             return matching_braces(string, lbracket, rbracket)
    elif (left_bracket != -1) != (right_bracket != -1):
        return False
    else:
        return True