from AST.ASTWalker import ASTWalker
from AST.ASTNode import ASTNodeType, ASTNode
from SymbolTableBuilder import SymbolTableBuilder

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTable = None

    def translate(self, ast, symbolTableFileName="", printDescription=False):
        self.AST = ast
        # TODO add functionality here
        self.fillSymbolTable(symbolTableFileName, printDescription)

    def fillSymbolTable(self, filename, printDescription):
        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        # TODO symbol table currently doesn't save different 'stages', deletes tables when creating new local scopes on used levels -> change that
        self.symbolTable = SymbolTableBuilder(filename, printDescription).buildSymbolTable(nodes)
        

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()