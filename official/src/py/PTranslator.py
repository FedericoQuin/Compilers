from src.py.AST.ASTWalker import ASTWalker
from src.py.AST.ASTNode import ASTNodeType, ASTNode, pointerType
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.TypeChecker import TypeChecker
from src.py.SA.ExistenceChecker import ExistenceChecker
from src.py.UTIL.TypeDeductor import TypeDeductor
from src.py.UTIL.VarTypes import *
from src.py.SA.UselessDecorator import UselessDecorator
from copy import deepcopy

class PTranslator:
    def __init__(self):
        self.AST = None
        self.programText = ""
        self.fringe = []

        # These arrays contain  tuple of begin and end labels of the loops
        # This is needed for break and continue statements (they must know where to jump to)
        self.currentWhileLoops = []
        self.currentForloops = []
        self.currentIfElses = []
        self.mostRecentLoop = None
        self.nextArrayAddress = 0

        self.nextLabelNumber = 0

        # For readability, include this in the label of while loops, for loops, ifelse,...
        self.currentFunction = ""
        self.functionSSPMap = {}

    def translate(self, ast, symbolTableFileName="", printDescription=False, translate = True):
        self.AST = ast
        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable)
        existenceChecker = ExistenceChecker(symbolTable)

        astwalker = ASTWalker(self.AST)
        nodes = astwalker.getNodesDepthFirst()

        # Existence checking
        for (node, nodeLevel) in nodes:
            self.symbolTableBuilder.processNode(node, nodeLevel)
            existenceChecker.checkExistence(node)

        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable, symbolTableFileName, printDescription)
        typeChecker = TypeChecker(symbolTable)
        uselessDecorator = UselessDecorator()

        # Type checking and actual translation
        for (node, nodeLevel) in nodes:
            self.symbolTableBuilder.processNode(node, nodeLevel)
            typeChecker.checkType(node)
            # Decorate nodes for uselessness
            uselessDecorator.checkUselessness(node, nodeLevel)

        self.symbolTableBuilder.saveSymbolTable("a")

        symbolTable = SymbolTable()
        self.symbolTableBuilder = SymbolTableBuilder(symbolTable)

        self.fringe.append(nodes[0])

        # TODO remove
        if translate:
            self.parseExpression()

        self.saveProgram("test")

    def parseExpression(self):
        if len(self.fringe) == 0:
            return

        node = self.fringe[0][0]
        nodeLevel = self.fringe[0][1]
        self.symbolTableBuilder.processNode(node, nodeLevel)

        if node.type == ASTNodeType.Program:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            while (len(self.fringe) != 0):
                if not isinstance(self.fringe[0][0].type, pointerType) and self.fringe[0][0].type != ASTNodeType.ArrayDecl:
                    self.parseExpression()
                else:
                    self.symbolTableBuilder.processNode(self.fringe[0][0], nodeLevel + 1)
                    del self.fringe[0]


            self.setGlobalDeclarations(node, nodeLevel)

        #################################
        # Functions                     #
        #################################
        elif node.type == ASTNodeType.Function:
            # Set the current function name
            self.currentFunction = node.value

            # Process the arguments
            self.processFunctionArgs(node.children[1], nodeLevel + 2)

            # calculate the amout of space needed
            declarations, declarationsWithArrays = self.getAmoutOfDeclarations(node)

            if node.value == "main":
                self.setMain()

            self.programText += "label_" + node.value + ":\n"
            # We know that according to the slides, this only includes the static part, but we saw no other way to do this with arrays
            self.programText += "ssp " + str(declarationsWithArrays + 5) + "\n"

            self.functionSSPMap[node.value] = declarationsWithArrays + 5

            self.programText += "sep " + str(max(self.calculateEP(node), 1)) + "\n"
            # Local procedure declarations are not possible in C so some things can be skipped

            # Set default return value
            returnType = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value).type.returnType
            if isinstance(returnType, PointerType):
                if isinstance(returnType.type, CharType) and returnType.ptrCount == 0:
                    self.programText += "ldc c 'a'\n"
                    self.programText += "str c 0 0\n"
                elif isinstance(returnType.type, IntType) and returnType.ptrCount == 0:
                    self.programText += "ldc i 0\n"
                    self.programText += "str i 0 0\n"
                elif isinstance(returnType.type, FloatType) and returnType.ptrCount == 0:
                    self.programText += "ldc r 0.0\n"
                    self.programText += "str r 0 0\n"
                elif returnType.ptrCount != 0:
                    self.programText += "ldc a 0\n"
                    self.programText += "str a 0 0\n"

            self.nextArrayAddress = declarations + 5

            self.currentFunction = node.value
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

        elif node.type == ASTNodeType.FunctionCall:
            del self.fringe[0]

            # calculate the amout of space needed
            arguments = len(self.symbolTableBuilder.symbolTable.lookupSymbol(node.value).type.arguments)

            # Get defining occurence difference from symbol table
            definingOccurrence = self.symbolTableBuilder.symbolTable.getDefOcc(node.value)

            # Get applied occurrence
            appliedOccurrence = self.symbolTableBuilder.symbolTable.getAppOcc()


            self.programText += "mst " + str(appliedOccurrence - definingOccurrence) + "\n"

            # Set the arguments:
            self.setFunctionArguments(node, nodeLevel)

            # Jump to the function
            self.programText += "cup " + str(arguments) + " label_" + node.value + "\n"

        elif node.type == ASTNodeType.ReturnType:
            self.parseChildrenFirst(node, nodeLevel)

        elif node.type == ASTNodeType.FunctionBody:
            self.parseChildrenFirst(node, nodeLevel)

            if node.parent.children[0].value.type == ASTNodeType.Void:
                self.programText += "retp\n"
            else:
                self.programText += "retf\n"

        elif node.type == ASTNodeType.Return:
            # TODO
            self.parseChildrenFirst(node, nodeLevel)

            if len(node.children) != 0:
                myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
                self.programText += "str " + myType.getPString() + " 0 0\nretf\n"
            else:
                returnType = self.symbolTableBuilder.symbolTable.lookupSymbol(self.currentFunction).type.returnType

                if isinstance(returnType, PointerType) and isinstance(returnType.type, VoidType):
                    self.programText += "retp\n"
                else:
                    self.programText += "retf\n"

        #################################
        # Declarations                  #
        #################################
        elif isinstance(node.type, pointerType) and \
            (node.type.type == ASTNodeType.FloatDecl or node.type.type == ASTNodeType.IntDecl or node.type.type == ASTNodeType.CharDecl):
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            if child_amount != 0:
                self.parseExpression()
            else:
                # Give a default value
                if node.type.type == ASTNodeType.FloatDecl:
                    self.programText += "ldc r 0.0\n"

                    mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
                    followLinkCount = self.getFollowLinkCount(node.value)
                    self.programText += "str r " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"
                elif node.type.type == ASTNodeType.CharDecl:
                    self.programText += "ldc c 'a'\n"

                    mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
                    followLinkCount = self.getFollowLinkCount(node.value)
                    self.programText += "str c " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"
                elif node.type.type == ASTNodeType.IntDecl:
                    self.programText += "ldc i 0\n"

                    mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
                    followLinkCount = self.getFollowLinkCount(node.value)
                    self.programText += "str i " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"



        #################################
        # Operations                    #
        #################################
        elif node.type == ASTNodeType.Initialization:
            # Set the rhs
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.parent.value)
            followLinkCount = self.getFollowLinkCount(node.parent.value)
            self.programText += "str " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

        elif node.type == ASTNodeType.Addition:
            myType0 = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
            myType1 = TypeDeductor.deductType(node.children[1], self.symbolTableBuilder.symbolTable)

            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            if isinstance(myType0, PointerType) and myType0.ptrCount != 0:
                self.parseMultipleExpressions(2)
                self.programText += "ixa 1\n"

            elif isinstance(myType1, PointerType) and myType1.ptrCount != 0:
                self.fringe[0], self.fringe[1] = self.fringe[1], self.fringe[0]

                self.parseMultipleExpressions(2)
                self.programText += "ixa 1\n"

            else:
                self.parseMultipleExpressions(2)
                myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
                self.programText += "add " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Subtraction:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()
            self.parseExpression()

            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "sub " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Mul:
            self.parseChildrenFirst(node, nodeLevel)

            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "mul " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Div:
            self.parseChildrenFirst(node, nodeLevel)

            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "div " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Assignment:
            myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)

            if node.children[0].type == ASTNodeType.LValueArrayElement:
                self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.children[0].value)

                # Set the value of the lhs
                self.parseExpression()

                # Set the value of the rhs
                self.parseExpression()

                self.programText += "sto " + myType.type.getPString() + "\n"

            elif node.children[0].type == ASTNodeType.Dereference:
                derefNode = node.children[0]

                self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

                # The dereference node must be done manually, it's children can be parsed by themselves
                self.addChildrenToFringe(derefNode, nodeLevel + 1, deleteFront=True)

                # Set the lhs address
                self.parseExpression()
                # Dereference (not all! we need the address)
                for i in range(len(derefNode.value) - 1):
                    self.programText += "ind a\n"

                # Set the value of the rhs
                self.parseExpression()

                self.programText += "sto " + myType.type.getPString() + "\n"

            elif isinstance(myType, ReferenceType):
                self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
                # delete the reference node, we don't need to evaluate it
                del self.fringe[0]

                # Set address of the reference on the stack
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.value)
                self.programText += "lod a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

                # evaluate the lhs
                self.parseExpression()

                self.programText += "sto " + myType.getPString() + "\n"

            elif node.children[0].type != ASTNodeType.Dereference and not isinstance(myType, ReferenceType):
                self.parseChildrenFirst(node, nodeLevel)

                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.children[0].value)
                self.programText += "str " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"



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
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
            followLinkCount = self.getFollowLinkCount(node.value)

            if isinstance(myType, ReferenceType):
                # delete the reference node, we don't need to evaluate it
                del self.fringe[0]

                # Set address of the reference on the stack
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
                followLinkCount = self.getFollowLinkCount(node.value)
                self.programText += "lod a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

                # Get its value
                self.programText += "ind " + myType.getPString() + "\n"
            else:
                self.programText += "lod " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"
                del self.fringe[0]

        elif node.type == ASTNodeType.RValueAddress:
            if node.children[0].type != ASTNodeType.LValueArrayElement:
                del self.fringe[0]

                # The argument should be (and will be because of error detection) an lvalue
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.children[0].value)
                self.programText += "lda " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

            else:
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.children[0].value)
                self.programText += "lod a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

                self.parseChildrenFirst(node.children[0], nodeLevel + 1, deleteFirst=True)
                self.programText += "ixa 1\n"


        elif node.type == ASTNodeType.LValue:
            # When here, we expect
            del self.fringe[0]

        elif node.type == ASTNodeType.RValueArrayElement:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
            followLinkCount = self.getFollowLinkCount(node.value)
            self.programText += "lod a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"
            self.parseExpression()
            self.programText += "ixa 1\n"
            self.programText += "ind " + mapping.type.type.getPString() + "\n"

        elif node.type == ASTNodeType.LValueArrayElement:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
            followLinkCount = self.getFollowLinkCount(node.value)
            self.programText += "lod a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

            self.parseExpression()

            self.programText += "ixa 1\n"

        ##################################
        # Pointers and arrays#
        ##################################
        elif node.type == ASTNodeType.Dereference:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            for i in range(len(node.value) - 1):
                self.programText += "ind a\n"

            self.programText += "ind " + myType.type.getPString() + "\n"

        elif node.type == ASTNodeType.ArrayDecl:
            del self.fringe[0]

            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
            followLinkCount = self.getFollowLinkCount(node.parent.value)
            self.programText += "lda " + str(followLinkCount) + " " + str(self.nextArrayAddress) + "\n"
            self.programText += "str a " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"

            line = ""
            if isinstance(node.children[0].value, pointerType):
                if node.children[0].value.ptrCount != 0:
                    # pointer
                    line = "ldc a 0\nstr a " + str(followLinkCount) + " "
                elif node.children[0].value.type == ASTNodeType.IntDecl:
                    # int
                    line = "ldc i 0\nstr i " + str(followLinkCount) + " "
                elif node.children[0].value.type == ASTNodeType.FloatDecl:
                    # float
                    line = "ldc r 0.0\nstr r " + str(followLinkCount) + " "
                elif node.children[0].value.type == ASTNodeType.CharDecl:
                    # char
                    line = "ldc c 'a'\nstr c " + str(followLinkCount) + " "

                for i in range(int(node.children[1].value)):
                    self.programText += line + str(self.nextArrayAddress) + "\n"
                    self.nextArrayAddress += 1

        #################################
        # While Loops                   #
        #################################
        elif node.type == ASTNodeType.While:
            self.mostRecentLoop = "while"

            loopBegin = self.currentFunction + "_while_" + str(self.nextLabelNumber)
            skipLoopLabel = self.currentFunction + "_while_" + str(self.nextLabelNumber) + "_false"

            self.currentWhileLoops.append((loopBegin, skipLoopLabel))
            self.nextLabelNumber += 1

            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            self.programText += loopBegin + ":\n"
            self.parseExpression()
            self.programText += "fjp " + skipLoopLabel + "\n"
            self.parseExpression()

            del self.currentWhileLoops[-1]

        elif node.type == ASTNodeType.WhileBody:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

            self.programText += "ujp " + self.currentWhileLoops[-1][0] + "\n"
            self.programText += self.currentWhileLoops[-1][1] + ":\n"


        #################################
        # For Loops                     #
        #################################
        elif node.type == ASTNodeType.For:
            self.mostRecentLoop = "for"

            loopBegin = self.currentFunction + "_for_" + str(self.nextLabelNumber)
            skipLoopLabel = self.currentFunction + "_for_" + str(self.nextLabelNumber) + "_false"

            self.currentForloops.append((loopBegin, skipLoopLabel))

            self.nextLabelNumber += 1

            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            self.parseExpression()
            self.programText += loopBegin + ":\n"
            self.parseExpression()
            self.programText += "fjp " + skipLoopLabel + "\n"

            # swap the body with the third for statement, as the third for statement has to be executed AFTER the body
            self.fringe[0], self.fringe[1] = self.fringe[1], self.fringe[0]
            self.parseExpression()
            self.parseExpression()

            self.programText += "ujp " + self.currentForloops[-1][0] + "\n"
            self.programText += self.currentForloops[-1][1] + ":\n"

            del self.currentForloops[-1]

        elif node.type == ASTNodeType.ForStmt1 or node.type == ASTNodeType.ForStmt2 or node.type == ASTNodeType.ForStmt3:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            if child_amount != 0:
                self.parseExpression()
            elif node.type == ASTNodeType.ForStmt2:
                self.programText += "ldc b t\n"

        elif node.type == ASTNodeType.ForBody:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

        #################################
        # Break and continue            #
        #################################
        elif node.type == ASTNodeType.Break:
            del self.fringe[0]

            self.programText += "ujp "
            if self.mostRecentLoop == "for":
                self.programText += self.currentForloops[-1][1] + "\n"
            else:
                self.programText += self.currentWhileLoops[-1][1] + "\n"

        elif node.type == ASTNodeType.Continue:
            del self.fringe[0]

            self.programText += "ujp "
            if self.mostRecentLoop == "for":
                self.programText += self.currentForloops[-1][0] + "\n"
            else:
                self.programText += self.currentWhileLoops[-1][0] + "\n"

        #################################
        # If-else                       #
        #################################
        elif node.type == ASTNodeType.IfElse:
            ifElseFalse = self.currentFunction + "_ifelse_" + str(self.nextLabelNumber) + "_false"
            ifElseEnd = self.currentFunction + "_ifelse_" + str(self.nextLabelNumber) + "_end"

            self.currentIfElses.append((ifElseFalse, ifElseEnd))

            self.nextLabelNumber += 1

            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel)
            del self.fringe[child_amount]

            self.parseExpression()
            self.programText += "fjp " + ifElseFalse + "\n"
            self.parseExpression()
            self.programText += "ujp " + ifElseEnd + "\n"
            self.programText += ifElseFalse + ":\n"
            if child_amount == 3:
                self.parseExpression()
            self.programText += ifElseEnd + ":\n"

        elif node.type == ASTNodeType.IfTrue or node.type == ASTNodeType.IfFalse:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

        #################################
        # Booleans and conditions       #
        #################################
        elif node.type == ASTNodeType.Condition:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

        elif node.type == ASTNodeType.Not or node.type == ASTNodeType.NegateBrackets or node.type == ASTNodeType.And or node.type == ASTNodeType.Or:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

            operators = {ASTNodeType.Not: "not\n", ASTNodeType.NegateBrackets: "not\n", ASTNodeType.And: "and\n", ASTNodeType.Or: "or\n"}
            self.programText += operators[node.type]
        
        elif node.type == ASTNodeType.Equals or node.type == ASTNodeType.NotEquals or node.type == ASTNodeType.Greater or \
            node.type == ASTNodeType.GreaterOrEqual or node.type == ASTNodeType.Less or node.type == ASTNodeType.LessOrEqual:

            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

            operators = {ASTNodeType.Equals: "equ ", ASTNodeType.NotEquals: "neq ", ASTNodeType.Greater: "grt ", ASTNodeType.GreaterOrEqual: "geq ",
                ASTNodeType.Less: "les ", ASTNodeType.LessOrEqual: "leq "}

            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += operators[node.type] + myType.getPString() + "\n"

        #################################
        # Other                         #
        #################################
        elif node.type == ASTNodeType.Brackets:
            child_amount = len(node.children)
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseMultipleExpressions(child_amount)

        else:
            del self.fringe[0]

        if node.useless:
            #TODO remove
            print("DID USELESS THING! ", self.currentFunction, " ", node.value)
            self.programText += "ssp " + str(self.functionSSPMap[self.currentFunction]) + "\n"

    def addChildrenToFringe(self, node, nodeLevel, deleteFront=False):
        childAmount = len(node.children)
        for child in reversed(node.children):
            self.fringe = [(child, nodeLevel + 1)] + self.fringe

        if deleteFront:
            del self.fringe[childAmount]

    def parseChildrenFirst(self, node, nodeLevel, deleteFirst=True):
        child_amount = len(node.children)
        self.addChildrenToFringe(node, nodeLevel, deleteFront=deleteFirst)
        self.parseMultipleExpressions(child_amount)

    def parseMultipleExpressions(self, count):
        for i in range(count):
            self.parseExpression()

    def getAmoutOfDeclarations(self, functionNode):
        declarations = 0
        declarationsWithArrays = 0
        for node in functionNode.children:
            if isinstance(node.type, pointerType) and \
                (node.type.type == ASTNodeType.FloatDecl or node.type.type == ASTNodeType.IntDecl or node.type.type == ASTNodeType.CharDecl):
                declarations += 1
                declarationsWithArrays += 1
            elif node.type == ASTNodeType.ArrayDecl:
                # The identifier of the array aka the pointer to the first element
                declarations += 1
                declarationsWithArrays += 1
                # The values held by the array
                declarationsWithArrays += node.children[1].value
            else:
                retVal = self.getAmoutOfDeclarations(node)
                declarations += retVal[0]
                declarationsWithArrays += retVal[1]
        return declarations, declarationsWithArrays

    def setFunctionArguments(self, functionNode, nodeLevel):

        arguments = self.symbolTableBuilder.symbolTable.lookupSymbol(functionNode.value).type.arguments

        for argument, argumentType in zip(functionNode.children, arguments):
            # TODO include references and array elements and stuff
            if isinstance(argumentType, ReferenceType):
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(argument.value)
                followLinkCount = self.getFollowLinkCount(argument.value)
                self.programText += "lda " + str(followLinkCount) + " " + str(mapping.address + 5) + "\n"
            else:
                self.fringe = [(argument, nodeLevel + 1)] +  self.fringe
                self.parseExpression()

    def processFunctionArgs(self, functionNode, nodeLevel):
        for arg in functionNode.children:
            if arg.type == ASTNodeType.ByReference:
                self.processFunctionArgs(arg, nodeLevel + 1)
            self.symbolTableBuilder.processNode(arg, nodeLevel)

    def getFollowLinkCount(self, variableName):
        # Get defining occurence difference from symbol table
            definingOccurrence = self.symbolTableBuilder.symbolTable.getDefOcc(variableName)

            # Get defining occurence difference from symbol table
            appliedOccurrence = self.symbolTableBuilder.symbolTable.getAppOcc()

            if definingOccurrence == 0 and appliedOccurrence != 0:
                # The scope is global
                return 1
            else:
                # Look for the symbol locally, thank you C for being this easy
                return 0

    def setMain(self):
        # calculate the amout of space needed
        args = self.symbolTableBuilder.symbolTable.lookupSymbol("main").type.arguments
        arguments = len(args)

        # Get defining occurence difference from symbol table
        definingOccurrence = self.symbolTableBuilder.symbolTable.getDefOcc("main")

        # Get applied occurrence
        appliedOccurrence = self.symbolTableBuilder.symbolTable.getAppOcc()

        self.programText += "main:\n"

        self.programText += "mst 0\n"

        # Set the arguments:
        for arg in reversed(args):
            # TODO, do not allow references and ptrs/arrays in main
            if isinstance(arg.type, FloatType):
                self.programText += "ldc r 0.0\n"
            elif isinstance(arg.type, IntType):
                self.programText += "ldc i 0\n"
            elif isinstance(arg.type, CharType):
                self.programText += "ldc c 'a'\n"

        # Jump to the function
        self.programText += "cup " + str(arguments) + " label_main\n"

        # Stop
        self.programText += "hlt\n"

    def setGlobalDeclarations(self, node, nodeLevel):
        globalDataSize = 0
        for child in node.children:
            if isinstance(child.type, pointerType):
                globalDataSize += 1
            elif child.type == ASTNodeType.ArrayDecl:
                globalDataSize += child.children[1].value
                globalDataSize += 1

        text = "ssp " + str(5 + globalDataSize) + "\n"

        # Dirty things here
        programText = deepcopy(self.programText)
        self.programText = ""

        # initialize them
        offset = 5
        for child in node.children:
            if isinstance(child.type, pointerType) and child.type.type == ASTNodeType.IntDecl:
                if child.children != []:
                    # Set the rhs
                    self.addChildrenToFringe(child.children[0], nodeLevel + 1, deleteFront=False)
                    self.parseExpression()
                    text += self.programText
                    self.programText = ""

                    text += "str i 0 " + str(offset) + "\n"

                    offset += 1
                else:
                    text += "ldc i 0\n"
                    text += "str i 0 " + str(offset) + "\n"
                    offset += 1


            elif isinstance(child.type, pointerType) and child.type.type == ASTNodeType.CharDecl:
                if child.children != []:
                    # Set the rhs
                    self.addChildrenToFringe(child.children[0], nodeLevel + 1, deleteFront=False)
                    self.parseExpression()
                    text += self.programText
                    self.programText = ""

                    text += "str c 0 " + str(offset) + "\n"

                    offset += 1
                else:
                    text += "ldc c 'a\n"
                    text += "str c 0 " + str(offset) + "\n"
                    offset += 1
            elif isinstance(child.type, pointerType) and child.type.type == ASTNodeType.FloatDecl:
                if child.children != []:
                    # Set the rhs
                    self.addChildrenToFringe(child.children[0], nodeLevel + 1, deleteFront=False)
                    self.parseExpression()
                    text += self.programText
                    self.programText = ""

                    text += "str r 0 " + str(offset) + "\n"

                    offset += 1
                else:
                    text += "ldc r 0.0\n"
                    text += "str r 0 " + str(offset) + "\n"
                    offset += 1
            elif child.type == ASTNodeType.ArrayDecl:
                # TODO
                pass

        text += "ujp main\n"
        self.programText = text + programText

    def calculateEP(self, node, level = 0):
        maximum = 0

        if node.type == ASTNodeType.ArrayDecl:
            maximum = 3

        elif node.type == ASTNodeType.RValueArrayElement or node.type == ASTNodeType.LValueArrayElement or node.type == ASTNodeType.FunctionCall:
            maximum = 1
            for child in node.children:
                maximum += self.calculateEP(child, level + 1)

        elif self.isSimpleRValue(node.type):
            maximum = 1

        elif self.isSimpleDeclaration(node.type):
            for child in node.children:
                maximum = max(self.calculateEP(child, level + 1), maximum)
            maximum = max(1, maximum)

        elif self.isRelationalOperator(node.type) or self.isMathematicalOperator(node.type) or node.type == ASTNodeType.Assignment or \
            node.type == ASTNodeType.Initialization or node.type == ASTNodeType.Condition or node.type == ASTNodeType.Brackets:

            for child in node.children:
                maximum += self.calculateEP(child, level + 1)

        elif node.type == ASTNodeType.For or node.type == ASTNodeType.ForBody or node.type == ASTNodeType.IfElse or \
            node.type == ASTNodeType.IfTrue or node.type == ASTNodeType.IfFalse or node.type == ASTNodeType.FunctionBody or \
            node.type == ASTNodeType.ForStmt1 or node.type == ASTNodeType.ForStmt2 or node.type == ASTNodeType.ForStmt3 or \
            node.type == ASTNodeType.WhileBody or node.type == ASTNodeType.While or node.type == ASTNodeType.Program:

            for child in node.children:
                maximum = max(self.calculateEP(child, level + 1), maximum)

        elif node.type == ASTNodeType.Function:
            maximum = self.calculateEP(node.children[2], level + 1)

        return maximum

    def isRelationalOperator(self, nodeType):
        if nodeType == ASTNodeType.Less or nodeType == ASTNodeType.LessOrEqual or nodeType == ASTNodeType.Equals or \
            nodeType == ASTNodeType.NotEquals or nodeType == ASTNodeType.Not or nodeType == ASTNodeType.Greater or \
            nodeType == ASTNodeType.GreaterOrEqual or nodeType == ASTNodeType.And or nodeType == ASTNodeType.Or:

            return True
        else:
            return False

    def isMathematicalOperator(self, nodeType):
        if nodeType == ASTNodeType.Addition or nodeType == ASTNodeType.Subtraction or nodeType == ASTNodeType.Mul or \
            nodeType == ASTNodeType.Div:
            return True
        else:
            return False

    def isSimpleDeclaration(self, nodeType):
        # TODO ptr?
        if nodeType == ASTNodeType.IntDecl or nodeType == ASTNodeType.FloatDecl or nodeType == ASTNodeType.CharDecl:
            return True
        elif isinstance(nodeType, pointerType) and (nodeType.type == ASTNodeType.IntDecl or nodeType.type == ASTNodeType.FloatDecl or nodeType.type == ASTNodeType.CharDecl):
            return True
        else:
            return False

    def isSimpleRValue(self, nodeType):
        # TODO ptr?
        if nodeType == ASTNodeType.RValueInt or nodeType == ASTNodeType.RValueID or nodeType == ASTNodeType.RValueFloat or \
            nodeType == ASTNodeType.RValueChar or nodeType == ASTNodeType.RValueAddress:
            return True
        else:
            return False
                

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()