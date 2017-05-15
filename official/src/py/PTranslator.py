from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode, pointerType
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.TypeChecker import TypeChecker
from src.py.SA.ExistenceChecker import ExistenceChecker

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.fringe = []

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

        self.fringe.append(nodes[0][0])
        self.parseExpression()

        self.saveProgram("test")
        # print(self.programText)
        # print("KEKEKEKEKEK3\n")

    def parseExpression(self):
        if len(self.fringe) == 0:
            return

        node = self.fringe[0]
        nodeLevel = self.fringe[0]

        if node.type == ASTNodeType.Program:
            self.fringe += self.fringe[0].children
            del self.fringe[0]
            self.parseExpression()

        elif node.type == ASTNodeType.Function:
            # TODO
            self.fringe += self.fringe[0].children
            self.programText += "label_" + self.fringe[0].value + ":\n"
            del self.fringe[0]
            self.parseExpression()

        elif node.type == ASTNodeType.ReturnType:
            # TODO
            self.fringe += self.fringe[0].children
            del self.fringe[0]
            self.parseExpression()

        elif node.type == ASTNodeType.FunctionArgs:
            # TODO
            # self.fringe += self.fringe[0].children
            del self.fringe[0]
            self.parseExpression()

        elif node.type == ASTNodeType.FunctionBody:
            # TODO
            self.fringe += self.fringe[0].children
            del self.fringe[0]

            while len(self.fringe) != 0:
                self.parseExpression()

        #################################
        # Declarations                  #
        #################################

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.CharDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"

            if len(elf.fringe[0].children) != 0:
                self.fringe = self.fringe[0].children + self.fringe
                del self.fringe[1]
                self.parseExpression()
            else:
                del self.fringe[0]

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.FloatDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[1]
            self.parseExpression()

        elif isinstance(node.type, pointerType) and node.type.type == ASTNodeType.IntDecl:
            self.programText += "// TODO declare variable <" + str(node.value) + ">\n"
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[1]
            self.parseExpression()

        #################################
        # Operations                    #
        #################################
        elif node.type == ASTNodeType.Initialization:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[1]
            self.parseExpression()
            self.programText += "// TODO assign to variable (get to stacktop + assign)\n"

        elif node.type == ASTNodeType.Addition:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[2]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            self.programText += "add i\n"

        elif node.type == ASTNodeType.Subtraction:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[2]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            self.programText += "sub i\n"

        elif node.type == ASTNodeType.Mul:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[2]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            self.programText += "mul i\n"

        elif node.type == ASTNodeType.Div:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[2]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            self.programText += "div i\n"

        elif node.type == ASTNodeType.Assignment:
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[2]
            self.parseExpression()
            self.parseExpression()
            # TODO make not hardcoded integer
            self.programText += "// TODO assign stuff (lvalue assignment)\n"

        #################################
        # Values                        #
        #################################
        elif node.type == ASTNodeType.RValueInt:
            self.programText += "ldc i " + str(node.value) + "\n"
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
            self.fringe = self.fringe[0].children + self.fringe
            del self.fringe[1]
            self.parseExpression()

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()