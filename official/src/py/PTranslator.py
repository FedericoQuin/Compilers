from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.TypeChecker import TypeChecker
from src.py.SA.ExistenceChecker import ExistenceChecker

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""

    def translate(self, ast, symbolTableFileName="", printDescription=False):
        self.AST = ast
        symbolTable = SymbolTable()
        symbolTableBuilder = SymbolTableBuilder(symbolTable)
        existenceChecker = ExistenceChecker(symbolTable)

        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        # Existence checking
        for (node, nodeLevel) in nodes:
            symbolTableBuilder.processNode(node, nodeLevel)
            existenceChecker.checkExistence(node)

        symbolTable = SymbolTable()
        symbolTableBuilder = SymbolTableBuilder(symbolTable, symbolTableFileName, printDescription)
        typeChecker = TypeChecker(symbolTable)

        # Type checking and actual translation
        for (node, nodeLevel) in nodes:
            symbolTableBuilder.processNode(node, nodeLevel)
            typeChecker.checkType(node)

        symbolTableBuilder.saveSymbolTable("a")



    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()