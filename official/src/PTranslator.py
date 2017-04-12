from SymbolTable import SymbolTable, Scope
from AST.ASTWalker import ASTWalker
from AST.ASTNode import ASTNodeType, ASTNode

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTable = SymbolTable()

    def translate(self, ast, symbolTableFileName=""):
        self.AST = ast
        # TODO add functionality here
        self.fillSymbolTable(symbolTableFileName)

    def fillSymbolTable(self, filename):
        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()
        currentLevel = 0

        for node in nodes:
            if (node.type == ASTNodeType.Block):
                currentLevel += 1
                self.symbolTable.enterScope()
            if (node.type == ASTNodeType.Function):
                currentLevel += 1
                self.symbolTable.enterScope()
            elif (node.type == ASTNodeType.FloatDecl):
                self.symbolTable.insertEntry(str(node.value), "float", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)
            elif (node.type == ASTNodeType.IntDecl):
                self.symbolTable.insertEntry(str(node.value), "int", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)
            elif (node.type == ASTNodeType.CharDecl):
                self.symbolTable.insertEntry(str(node.value), "char", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)
            

        # save the symbol table to a text file (might be temporary)
        if (filename != ""):
            self.saveSymbolTable(filename)

    def saveSymbolTable(self, filename):
        symbolTableFile = open(filename, 'w')
        symbolTableFile.write(str(self.symbolTable))
        symbolTableFile.close()

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()