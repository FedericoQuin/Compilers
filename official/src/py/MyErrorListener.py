from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener( ErrorListener ):

    def __init__(self, filename):
        super(MyErrorListener, self).__init__()

        with open(filename, 'r') as myfile:
            self.data = myfile.read().split("\n")


    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()[0]

        ex_msg = str(line) + ":" + str(column) + ": " + "Error while parsing " + str(stack) + "\n"
        ex_msg += str(self.data[line - 1]) + "\n"

        tabCount = self.data[line - 1].count("\t")

        ex_msg += str(tabCount * "\t")
        ex_msg += str((column - tabCount) * " ")
        ex_msg += "^" + "\n"
        ex_msg += msg + "\n"
        raise Exception(ex_msg)