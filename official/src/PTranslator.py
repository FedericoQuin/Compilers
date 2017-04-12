from SymbolTable import SymbolTable, Scope
from AST.ASTWalker import ASTWalker
from AST.ASTNode import ASTNodeType, ASTNode

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTable = SymbolTable()

    def translate(self, ast):
        self.AST = ast
        # TODO add functionality here
        self.fillSymbolTable()

    def fillSymbolTable(self):
        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        for node in nodes:
            if (node.type == ASTNodeType.Block):
                self.symbolTable.enterScope()
            if (node.type == ASTNodeType.Function):
                self.symbolTable.enterScope()
            elif (node.type == ASTNodeType.FloatDecl):
                self.symbolTable.insertEntry(str(node.value), "float")
            elif (node.type == ASTNodeType.IntDecl):
                self.symbolTable.insertEntry(str(node.value), "int")
            elif (node.type == ASTNodeType.CharDecl):
                self.symbolTable.insertEntry(str(node.value), "char")
            

        # save the symbol table to a text file (might be temporary)
        self.saveSymbolTable("data/symbolTable.txt")

    def saveSymbolTable(self, filename):
        symbolTableFile = open(filename, 'w')
        symbolTableFile.write(str(self.symbolTable))
        symbolTableFile.close()

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()