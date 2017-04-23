from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode
from src.SymbolTableBuilder import SymbolTableBuilder
from src.SymbolTable import SymbolTable
from src.py.TypeChecker import TypeChecker

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTableBuilder = None
        self.symbolTable = None
        self.typeChecker = None

    def translate(self, ast, symbolTableFileName="", printDescription=False):
        self.AST = ast
        self.symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(self.symbolTable, symbolTableFileName, printDescription)
        self.typeChecker = TypeChecker(self.symbolTable)

        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        for (node, nodeLevel) in nodes:
            self.symbolTableBuilder.processNode(node, nodeLevel)
            # self.typeChecker.checkType(node, nodeLevel)

        self.symbolTableBuilder.saveSymbolTable("a")


        # TODO add functionality here
        # self.fillSymbolTable(symbolTableFileName, printDescription)

    def fillSymbolTable(self, filename, printDescription):
        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        # TODO symbol table currently doesn't save different 'stages', deletes tables when creating new local scopes on used levels -> change that
        self.symbolTable = SymbolTableBuilder(filename, printDescription).buildSymbolTable(nodes)
        

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()