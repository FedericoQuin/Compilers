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
        levelList = []

        if (filename != ""):
            self.saveSymbolTable(filename, 'w')


        for (node, nodeLevel) in nodes:
            # If the node we are visiting now is on the same/higher level than the current working scope -> leave the scope/multiple scopes
            # (with the exception of the global scope)
            if (len(levelList) != 0) and (nodeLevel <= levelList[-1]):
                if (filename != ""):
                    self.saveSymbolTable(filename, 'a')
                currentDepth = len(levelList)

                indexToSlice = 0
                if not(nodeLevel in levelList):
                    # Find the nearest match in the levelList
                    for level in reversed(levelList):
                        if (level < nodeLevel):
                            indexToSlice = levelList.index(level) + 1
                else:
                    indexToSlice = levelList.index(nodeLevel)

                # Slice all the levels deeper and equal to the current level of the node
                # For example:  levelList = [0 1 5 6 8]
                #               nodeLevel = 5       (eg. an int declaration after a code block on level 5 in the AST)
                #
                # Result:       levelList = levelList[:2] = [0 1]   (the code block from level 5, as well as the local scopes beyond, should be dropped)
                levelList = levelList[:indexToSlice]

                # Leave the amount of scopes that are not used anymore
                for i in range(0, currentDepth - len(levelList)):
                    self.symbolTable.leaveScope()
                # Update the currentLevel value to the updated scopes
                currentLevel = len(levelList)

            def enterScope():
                # little helper function, quite repetitive otherwise
                nonlocal currentLevel
                nonlocal levelList

                currentLevel += 1
                levelList.append(nodeLevel)
                self.symbolTable.enterScope()

            if (node.type == ASTNodeType.Block):
                enterScope()
            elif (node.type == ASTNodeType.Function):
                enterScope()
            elif (node.type == ASTNodeType.IfTrue):
                enterScope()
            elif (node.type == ASTNodeType.IfFalse):
                enterScope()
            elif (node.type == ASTNodeType.While):
                enterScope()
            elif (node.type == ASTNodeType.For):
                enterScope()
                
            elif (node.type == ASTNodeType.FloatDecl):
                self.symbolTable.insertEntry(str(node.value), "float", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)
            elif (node.type == ASTNodeType.IntDecl):
                self.symbolTable.insertEntry(str(node.value), "int", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)
            elif (node.type == ASTNodeType.CharDecl):
                self.symbolTable.insertEntry(str(node.value), "char", Scope.GLOBAL if currentLevel == 0 else Scope.LOCAL)

        # save the symbol table to a text file (might be temporary)
        if (filename != ""):
            self.saveSymbolTable(filename, 'a')

    def saveSymbolTable(self, filename, mode):
        symbolTableFile = open(filename, mode)
        symbolTableFile.write(str(self.symbolTable) + "\n\n")
        symbolTableFile.close()

    def saveProgram(self, filename):
        programFile = open(filename, 'w')
        programFile.write(self.programText)
        programFile.close()