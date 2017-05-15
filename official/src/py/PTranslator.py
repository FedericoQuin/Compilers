from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode, pointerType
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.TypeChecker import TypeChecker
from src.py.SA.ExistenceChecker import ExistenceChecker
from src.py.UTIL.TypeDeductor import TypeDeductor
from src.py.UTIL.VarTypes import *

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.fringe = []

    def translate(self, ast, symbolTableFileName="", printDescription=False):
        self.AST = ast
        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable)
        existenceChecker = ExistenceChecker(symbolTable)

        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        # Existence checking
        for (node, nodeLevel) in nodes:
            #TODO symbol table unnecessary?
            self.symbolTableBuilder.processNode(node, nodeLevel)
            existenceChecker.checkExistence(node)

        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable, symbolTableFileName, printDescription)
        typeChecker = TypeChecker(symbolTable)

        # Type checking and actual translation
        for (node, nodeLevel) in nodes:
            #TODO symbol table unnecessary?
            self.symbolTableBuilder.processNode(node, nodeLevel)
            typeChecker.checkType(node)

        self.symbolTableBuilder.saveSymbolTable("a")

        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable)

        self.fringe.append(nodes[0])
        self.parseExpression()

        self.saveProgram("test")

    def parseExpression(self):
        if len(self.fringe) == 0:
            return

        node = self.fringe[0][0]
        nodeLevel = self.fringe[0][1]
        self.symbolTableBuilder.processNode(node, nodeLevel)

        if node.type == ASTNodeType.Program:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

        elif node.type == ASTNodeType.Function:
            # TODO
            self.programText += "label_" + node.value + ":\n"
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

        elif node.type == ASTNodeType.ReturnType:
            # TODO
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

        elif node.type == ASTNodeType.FunctionArgs:
            # TODO
            # self.fringe += node.children
            del self.fringe[0]
            self.parseExpression()

        elif node.type == ASTNodeType.FunctionBody:
            # TODO
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]

            while len(self.fringe) != 0:
                self.parseExpression()

        #################################
        # Declarations                  #
        #################################

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.CharDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"

            if len(elf.fringe[0].children) != 0:
                child_amount = len(node.children)
                self.addChildrenToFringe(node, nodeLevel)
                del self.fringe[child_amount]
                self.parseExpression()
            else:
                del self.fringe[0]

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.FloatDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.IntDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

        #################################
        # Operations                    #
        #################################
        elif node.type == ASTNodeType.Initialization:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.programText += "// TODO assign to variable (get to stacktop + assign)\n"

        elif node.type == ASTNodeType.Addition:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "add " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Subtraction:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "sub " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Mul:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "mul " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Div:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "div " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Assignment:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()
            self.parseExpression()
            self.programText += "// TODO assign stuff (lvalue assignment)\n"

        #################################
        # Values                        #
        #################################
        elif node.type == ASTNodeType.RValueInt:
            self.programText += "ldc i " + str(node.value) + "\n"
            del self.fringe[0]

        elif node.type == ASTNodeType.RValueChar:
            self.programText += "ldc c " + str(node.value) + "\n"
            del self.fringe[0]

        elif node.type == ASTNodeType.RValueFloat:
            self.programText += "ldc r " + str(node.value) + "\n"
            del self.fringe[0]

        elif node.type == ASTNodeType.RValueID:
            self.programText += "//TODO load <" + node.value + "> on stack\n"
            del self.fringe[0]

        elif node.type == ASTNodeType.LValue:
            self.programText += "//TODO load lvalue <" + node.value + "> on stack\n"
            del self.fringe[0]

        #################################
        # Other                         #
        #################################
        elif node.type == ASTNodeType.Brackets:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]
            self.parseExpression()

    def addChildrenToFringe(self, node, nodeLevel):
        for child in reversed(node.children):
            self.fringe = [(child, nodeLevel + 1)] + self.fringe

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()