from SymbolTable import SymbolTable

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTable = SymbolTable()

    def translate(self, ast):
        self.AST = ast
        # TODO add functionality here

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()