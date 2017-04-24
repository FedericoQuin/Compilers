from src.SymbolTable import *
from src.py.AST.ASTNode import ASTNodeType, ASTNode, pointerType

class SymbolTableBuilder:
	def __init__(self, symbolTable, filename, printDescription):
		self.currentLevel = 0
		self.levelList = []
		self.filename = filename
		self.symbolTable = symbolTable

		if (self.filename != ""):
			symbolTableFile = open(self.filename, 'w')
			symbolTableFile.write("\n")
			# Add a general description of the output to the filename
			if (printDescription == True):
				symbolTableFile.write("The output of the SymbolTable is as follows:\n")
				symbolTableFile.write(""""Scope_of_SymbolTable {entry, entry, ...}" with\n""")
				symbolTableFile.write("\t* Scope_of_SymbolTable = The scope that is shown at that line (either GLOBAL or some LOCAL scope).\n")
				symbolTableFile.write("\t* entry = A mapping of a symbol to a tuple consisting of the type and the starting address of the symbol in question.\n")
				symbolTableFile.write("\t\tFor example: 'someInt' -> ('int', 0)\n")
				symbolTableFile.write("\tNote: Functions don't have a starting address in memory, so their address is None.\n\n")
				symbolTableFile.write("The SymbolTable is saved at the initial construction (when still empty), at every point just before some local tables are deleted, and at the end of the AST walkthrough.\n")
				symbolTableFile.write("\n\n")
			symbolTableFile.write(str(self.symbolTable) + "\n\n")
			symbolTableFile.close()

	def processNode(self, node, nodeLevel):
		# If the node we are visiting now is on the same/higher level than the current working scope -> leave the scope/multiple scopes
		# (with the exception of the global scope)
		if (len(self.levelList) != 0) and (nodeLevel <= self.levelList[-1]):
			self.leaveScopes(nodeLevel)

		if (node.type == ASTNodeType.Block):
			self.enterScope(nodeLevel)
		elif (node.type == ASTNodeType.IfTrue):
			self.enterScope(nodeLevel)
		elif (node.type == ASTNodeType.IfFalse):
			self.enterScope(nodeLevel)
		elif (node.type == ASTNodeType.WhileBody):
			self.enterScope(nodeLevel)
		elif (node.type == ASTNodeType.For):
			self.enterScope(nodeLevel)
		elif (node.type == ASTNodeType.Function):
			self.enterScope(nodeLevel)
			if (self.symbolTable.symbolExists(str(node.value), Scope.GLOBAL) == False):
				self.addFunctionSignature(node)

		self.checkForDeclarations(node, nodeLevel)


	def buildSymbolTable(self, nodes):
		self.saveSymbolTable('a')

		for (node, nodeLevel) in nodes:
			self.processNode(node, nodeLevel)
			

		self.saveSymbolTable('a')
		return self.symbolTable

	
	def addFunctionSignature(self, node):
		children = node.children
		# TODO Func is a placeholder until subclassed
		returnType = PointerType(mapToPrimitiveType(children[0].value.type), children[0].value.ptrCount)
		
		# Iterate over the function arguments and add their types to the signature
		# NOTE: The type attribute of the function arguments nodes are objects of the class PointerType.
		#		The actual type has to be accessed by getting the type attribute from that class.
		functionSignature = [PointerType(mapToPrimitiveType(i.type.type), i.type.ptrCount) for i in children[1].children]
		# functionSignature += ",".join([ mapToPrimitiveName(child.type.type) for child in children[1].children ]) + ")"
		self.symbolTable.insertEntry(str(node.value), FunctionType(returnType, functionSignature) , Scope.GLOBAL)


	def checkForDeclarations(self, node, nodeLevel):
		if (node.type == ASTNodeType.FloatDecl):
			self.symbolTable.insertEntry(str(node.value), FloatType(), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
		elif (node.type == ASTNodeType.IntDecl):
			self.symbolTable.insertEntry(str(node.value), IntType(), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
		elif (node.type == ASTNodeType.CharDecl):
			self.symbolTable.insertEntry(str(node.value), CharType(), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
		elif (node.type == ASTNodeType.FunctionDecl):
			self.addFunctionSignature(node)
		elif (node.type == ASTNodeType.ArrayDecl):
			# The type part of the symbol (for example: int****)
			arrayType = PointerType(mapToPrimitiveType(node.children[0].value.type), node.children[0].value.ptrCount)
			size = node.children[1].value
			self.symbolTable.insertEntry(str(node.value), ArrayType(arrayType, size), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
		elif (type(node.type) is pointerType):
			# Exception for functionDecls -> do not add the 'declared' symbols to the table
			if self.isSignatureType(node.type.type):
				return
			
			# Type consists of the primitive type + optionally pointer operators
			symbolType = PointerType(mapToPrimitiveType(node.type.type), node.type.ptrCount)
			self.symbolTable.insertEntry(str(node.value), symbolType, Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)


	def isSignatureType(self, _type):
		"""
			Method that checks is given type is a signature type (signature type being a type that is used in function signatures/declarations)
		"""
		if _type == ASTNodeType.IntSignature:
			return True
		elif _type == ASTNodeType.FloatSignature:
			return True
		elif _type == ASTNodeType.CharSignature: 
			return True
		elif _type == ASTNodeType.ArraySignature:
			return True
		return False

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
					break
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


def mapToPrimitiveType(nodeType):
	if (nodeType == ASTNodeType.IntDecl):
		return IntType()
	elif (nodeType == ASTNodeType.FloatDecl):
		return FloatType()
	elif (nodeType == ASTNodeType.CharDecl):
		return CharType()
	if (nodeType == ASTNodeType.IntSignature):
		return IntType()
	elif (nodeType == ASTNodeType.FloatSignature):
		return FloatType()
	elif (nodeType == ASTNodeType.CharSignature):
		return CharType()
	elif (nodeType == ASTNodeType.Void):
		return VoidType()
		
	return None