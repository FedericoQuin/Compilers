from SymbolTable import SymbolTable, Scope
from AST.ASTNode import ASTNodeType, ASTNode

class SymbolTableBuilder:
	def __init__(self, filename = ""):
		self.currentLevel = 0
		self.levelList = []
		self.filename = filename
		self.symbolTable = SymbolTable()

	def buildSymbolTable(self, nodes):
		self.saveSymbolTable('w')

		for (node, nodeLevel) in nodes:
			# If the node we are visiting now is on the same/higher level than the current working scope -> leave the scope/multiple scopes
			# (with the exception of the global scope)
			if (len(self.levelList) != 0) and (nodeLevel <= self.levelList[-1]):
				self.leaveScopes(nodeLevel)

			if (node.type == ASTNodeType.Block):
				self.enterScope(nodeLevel)
			elif (node.type == ASTNodeType.Function):
				self.enterScope(nodeLevel)
			elif (node.type == ASTNodeType.IfTrue):
				self.enterScope(nodeLevel)
			elif (node.type == ASTNodeType.IfFalse):
				self.enterScope(nodeLevel)
			elif (node.type == ASTNodeType.While):
				self.enterScope(nodeLevel)
			elif (node.type == ASTNodeType.For):
				self.enterScope(nodeLevel)
				
			elif (node.type == ASTNodeType.FloatDecl):
				self.symbolTable.insertEntry(str(node.value), "float", Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
			elif (node.type == ASTNodeType.IntDecl):
				self.symbolTable.insertEntry(str(node.value), "int", Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
			elif (node.type == ASTNodeType.CharDecl):
				self.symbolTable.insertEntry(str(node.value), "char", Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)

		self.saveSymbolTable('a')
		return self.symbolTable


	def leaveScopes(self, nodeLevel):
		"""
			Leaves one or more scopes according the the depth level of the current node.
		"""
		self.saveSymbolTable('a')
		currentDepth = len(self.levelList)
		indexToSlice = self.getLevelSliceIndex(nodeLevel)

		# Slice all the levels deeper and equal to the current level of the node
		# For example:  levelList = [0 1 5 6 8]
		#               nodeLevel = 5       (eg. an int declaration after a code block on level 5 in the AST)
		#
		# Result:       levelList = levelList[:2] = [0 1]   (the code block from level 5, as well as the local scopes beyond, should be dropped)
		self.levelList = self.levelList[:indexToSlice]

		# Leave the amount of scopes that are not used anymore
		for i in range(0, currentDepth - len(self.levelList)):
			self.symbolTable.leaveScope()

		# Update the currentLevel value to the updated scopes
		self.currentLevel = len(self.levelList)


	def getLevelSliceIndex(self, nodeLevel):
		"""
			Determines and returns the index needed to slice the levelList, according to the depth level of the current node.
		"""
		indexToSlice = 0
		if not(nodeLevel in self.levelList):
			# Find the nearest match in the levelList
			for level in reversed(self.levelList):
				if (level < nodeLevel):
					indexToSlice = self.levelList.index(level) + 1
		else:
			indexToSlice = self.levelList.index(nodeLevel)
		
		return indexToSlice


	def enterScope(self, nodeLevel):
		self.currentLevel += 1
		self.levelList.append(nodeLevel)
		self.symbolTable.enterScope()


	def saveSymbolTable(self, mode):
		"""
			Saves the symbol tables (if a filename was given with the constructor).
		"""
		if (self.filename == ""):
			return
		symbolTableFile = open(self.filename, mode)
		symbolTableFile.write(str(self.symbolTable) + "\n\n")
		symbolTableFile.close()
