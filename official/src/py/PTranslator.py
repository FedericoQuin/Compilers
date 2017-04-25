from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.ST.SymbolTable import SymbolTable
from src.py.TypeChecker import TypeChecker
from src.py.ExistenceChecker import ExistenceChecker

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.symbolTableBuilder = None
        self.symbolTable = None
        self.typeChecker = None
        self.existenceChecker = None

    def translate(self, ast, symbolTableFileName="", printDescription=False):
        self.AST = ast
        self.symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(self.symbolTable, symbolTableFileName, printDescription)
        self.typeChecker = TypeChecker(self.symbolTable)
        self.existenceChecker = ExistenceChecker(self.symbolTable)

        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        for (node, nodeLevel) in nodes:
            self.symbolTableBuilder.processNode(node, nodeLevel)
            self.existenceChecker.checkExistence(node)
            self.typeChecker.checkType(node)

        self.symbolTableBuilder.saveSymbolTable("a")



    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()