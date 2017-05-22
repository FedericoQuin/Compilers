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

        # These arrays contain  tuple of begin and end labels of the loops
        # This is needed for break and continue statements (they must know where to jump to)
        self.currentWhileLoops = []
        self.currentForloops = []
        self.currentIfElses = []
        self.mostRecentLoop = None

        self.nextLabelNumber = 0

        # For readability, include this in the label of while loops, for loops, ifelse,...
        self.currentFunction = ""

    def translate(self, ast, symbolTableFileName="", printDescription=False, translate = True):
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
                self.parseExpression()

        #################################
        # Functions                     #
        #################################
        elif node.type == ASTNodeType.Function:
            # Set the current function name
            self.currentFunction = node.value

            # Process the arguments
            self.processFunctionArgs(node.children[1], nodeLevel + 2)

            # calculate the amout of space needed
            declarations = self.getAmoutOfDeclarations(node)

            self.programText += "label_" + node.value + ":\n"
            self.programText += "ssp " + str(declarations * 4) + "\n"
            # TODO copy arrays?
            self.programText += "sep wat? hoe moet ik dit nu weten?\n"
            # Local procedure declarations are not possible in C so some things can be skipped

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
            self.setFunctionArguments(node)

            # Jump to the function
            self.programText += "cup " + str(arguments * 4) + " " + node.value + "\n"

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

        #################################
        # Operations                    #
        #################################
        elif node.type == ASTNodeType.Initialization:
            # TODO check?
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.parent.value)
            followLinkCount = self.getFollowLinkCount(node.parent.value)
            self.programText += "str " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"

        elif node.type == ASTNodeType.Addition:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

            # If the other operand is a pointer, multiply this operand by the size of the type
            if isinstance(node.children[1], pointerType) and node.children[1].type.ptrCount != 0:
                myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
                self.programText += "ldc i 4\n"
                self.programText += "mul " + myType.getPString() + "\n"

            self.parseExpression()

            # If the other operand is a pointer, multiply this operand by the size of the type
            if isinstance(node.children[0], pointerType) and node.children[0].type.ptrCount != 0:
                myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
                self.programText += "ldc i 4\n"
                self.programText += "mul " + myType.getPString() + "\n"

            
            myType = TypeDeductor.deductType(node, self.symbolTableBuilder.symbolTable)
            self.programText += "add " + myType.getPString() + "\n"

        elif node.type == ASTNodeType.Subtraction:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
            self.parseExpression()

            # If the other operand is a pointer, multiply this operand by the size of the type
            if isinstance(node.children[1], pointerType) and node.children[1].type.ptrCount != 0:
                myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
                self.programText += "ldc i 4\n"
                self.programText += "mul " + myType.getPString() + "\n"

            self.parseExpression()

            # If the other operand is a pointer, multiply this operand by the size of the type
            if isinstance(node.children[0], pointerType) and node.children[0].type.ptrCount != 0:
                myType = TypeDeductor.deductType(node.children[0], self.symbolTableBuilder.symbolTable)
                self.programText += "ldc i 4\n"
                self.programText += "mul " + myType.getPString() + "\n"

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

            if node.children[0].type != ASTNodeType.Dereference and not isinstance(myType, ReferenceType):
                self.parseChildrenFirst(node, nodeLevel)

                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
                followLinkCount = self.getFollowLinkCount(node.children[0].value)
                self.programText += "str " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"

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
                self.programText += "lod " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"

                # evaluate the lhs
                self.parseExpression()

                self.programText += "sto " + myType.getPString() + "\n"



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
            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.value)
            followLinkCount = self.getFollowLinkCount(node.value)
            self.programText += "lod " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"
            del self.fringe[0]

        elif node.type == ASTNodeType.RValueAddress:
            self.addChildrenToFringe(node, nodeLevel, deleteFront=True)

            # The argument should be (and will be because of error detection) an lvalue
            mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(node.children[0].value)
            followLinkCount = self.getFollowLinkCount(node.children[0].value)
            self.programText += "lda " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"

        elif node.type == ASTNodeType.LValue:
            # TODO remove?
            del self.fringe[0]

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
                self.programText += "ldc b true\n"

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

    def addChildrenToFringe(self, node, nodeLevel, deleteFront=False):
        childAmount = len(node.children)
        for child in reversed(node.children):
            self.fringe = [(child, nodeLevel + 1)] + self.fringe

        if deleteFront:
            del self.fringe[childAmount]

    def parseChildrenFirst(self, node, nodeLevel):
        child_amount = len(node.children)
        self.addChildrenToFringe(node, nodeLevel, deleteFront=True)
        self.parseMultipleExpressions(child_amount)

    def parseMultipleExpressions(self, count):
        for i in range(count):
            self.parseExpression()

    def getAmoutOfDeclarations(self, functionNode):
        declarations = 0
        for node in functionNode.children:
            if isinstance(node.type, pointerType) and \
                (node.type.type == ASTNodeType.FloatDecl or node.type.type == ASTNodeType.IntDecl or node.type.type == ASTNodeType.CharDecl):
                declarations += 1
            elif node.type == ASTNodeType.ArrayDecl:
                # The identifier of the array aka the pointer to the first element
                declarations += 1
                # The values held by the array
                declarations += node.children[1].value
            else:
                declarations += self.getAmoutOfDeclarations(node)
        return declarations

    def setFunctionArguments(self, functionNode):

        arguments = self.symbolTableBuilder.symbolTable.lookupSymbol(functionNode.value).type.arguments

        for argument, argumentType in zip(functionNode.children, arguments):
            # TODO include references and array elements and stuff
            if isinstance(argumentType, ReferenceType):
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(argument.value)
                followLinkCount = self.getFollowLinkCount(argument.value)
                self.programText += "lda " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"
            elif argument.type == ASTNodeType.RValueFloat:
                self.programText += "ldc r " + str(argument.value) + "\n"
            elif argument.type == ASTNodeType.RValueInt:
                self.programText += "ldc i " + str(argument.value) + "\n"
            elif argument.type == ASTNodeType.RValueChar:
                self.programText += "ldc c " + str(argument.value) + "\n"
            elif argument.type == ASTNodeType.RValueID:
                mapping = self.symbolTableBuilder.symbolTable.lookupSymbol(argument.value)
                followLinkCount = self.getFollowLinkCount(argument.value)
                self.programText += "lod " + mapping.type.getPString() + " " + str(followLinkCount) + " " + str(mapping.address + 8) + "\n"

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

            if definingOccurrence == 0:
                # The scope is global
                return 1
            else:
                # Look for the symbol in this function, thank you C for being this easy
                return 0

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()