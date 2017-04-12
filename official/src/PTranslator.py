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
        # Here comes the fun part :D
        levelList = []
        

        for entry in nodes:
            node = entry[0]
            nodeLevel = entry[1]

            # If the node we are visiting now is on the same/higher level than the current working scope -> leave the scope/multiple scopes
            # (with the exception of the global scope)
            if (len(levelList) != 0) and (nodeLevel <= levelList[-1]):
                currentDepth = len(levelList)

                # Slice all the levels deeper and equal to the current level of the node
                # For example:  levelList = [0 1 5 6 8]
                #               nodeLevel = 5       (eg. an int declaration after a code block on level 5 in the AST)
                #
                # Result:       levelList = levelList[:2] = [0 1]   (the code block from level 5, as well as the local scopes beyond, should be dropped)
                levelList = levelList[:levelList.index(nodeLevel)]

                # Leave the amount of scopes that are not used anymore
                for i in range(0, currentDepth - len(levelList)):
                    self.symbolTable.leaveScope()
                # Update the currentLevel value to the updated scopes
                currentLevel = len(levelList)

            if (node.type == ASTNodeType.Block):
                currentLevel += 1
                levelList.append(nodeLevel)
                self.symbolTable.enterScope()
            elif (node.type == ASTNodeType.Function):
                currentLevel += 1
                levelList.append(nodeLevel)
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