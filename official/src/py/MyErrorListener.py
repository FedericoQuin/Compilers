from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener( ErrorListener ):

    def __init__(self, filename):
        super(MyErrorListener, self).__init__()

        with open(filename, 'r') as myfile:
            self.data = myfile.read().split("\n")


    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()[0]

        print(line, ":", column, ": ", "Error while parsing", str(stack))
        print(self.data[line - 1])
        tabCount = self.data[line - 1].count("\t")
        print(tabCount * "\t", end = "")
        print((column - tabCount) * " ", end = "")
        print("^")
        print(msg)
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)