from src.py.ST.SymbolTable import *
from src.py.AST.ASTNode import ASTNodeType, ASTNode, pointerType
from src.py.UTIL.VarTypes import *
from src.py.UTIL.MapToVarType import *
from src.py.SA.ErrorMsgHandler import ErrorMsgHandler

class SymbolTableBuilder:
	def __init__(self, symbolTable):
		self.currentLevel = 0
		self.levelList = []
		self.symbolTable = symbolTable


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
				self.addFunctionSignature(node, True)

				# Add the used variables in the function body to the function type
				self.addUsedVariablesFunction(self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL).type, node)

			elif type(self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL).type) is FunctionType:
				if self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL).type.initialized == False:
					self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL).type.initialized = True
					# Add the used variables in the function body to the function type
					self.addUsedVariablesFunction(self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL).type, node)
				else:
					ErrorMsgHandler.functionAlreadyInitialised(node)
			else:
				ErrorMsgHandler.symbolAlreadyDeclared(node)

		self.checkForDeclarations(node, nodeLevel)


	def buildSymbolTable(self, nodes):
		for (node, nodeLevel) in nodes:
			self.processNode(node, nodeLevel)
			
		return self.symbolTable

	
	def addFunctionSignature(self, node, initialized = False):
		children = node.children
		returnType = PointerType(mapNodeToVarType(children[0].value), children[0].value.ptrCount)
		
		# Iterate over the function arguments and add their types to the signature
		# NOTE: The type attribute of the function arguments nodes are objects of the class pointerType.
		#		The actual type has to be accessed by getting the type attribute from that class.
		functionSignature = []
		for i in children[1].children:
			if i.type == ASTNodeType.ByReference:
				functionSignature.append(ReferenceType(PointerType(mapNodeToVarType(i.children[0].type), i.children[0].type.ptrCount)))
			else:
				functionSignature.append(PointerType(mapNodeToVarType(i.type), i.type.ptrCount))

		self.symbolTable.insertEntry(str(node.value), FunctionType(returnType, functionSignature, initialized) , Scope.GLOBAL)


	def addPrimitiveType(self, node, _type, reference):
		self.checkDuplicateDeclaration(node)
		if reference == True:
			_type = ReferenceType(_type)
		self.symbolTable.insertEntry(str(node.value), _type, Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)

	def checkDuplicateDeclaration(self, node):
		if self.symbolTable.lookupSymbol(str(node.value), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL, len(self.levelList)-1) != None:
			ErrorMsgHandler.symbolAlreadyDeclared(node)
		

	def checkForDeclarations(self, node, nodeLevel):
		# Check to see if the declaration is a reference
		isReferenceDecl = False
		if nodeLevel != 0 and node.parent.type == ASTNodeType.ByReference:
			isReferenceDecl = True


		if node.type == ASTNodeType.FloatDecl:
			self.addPrimitiveType(node, FloatType(), isReferenceDecl)
		elif node.type == ASTNodeType.IntDecl:
			self.addPrimitiveType(node, IntType(), isReferenceDecl)
		elif node.type == ASTNodeType.CharDecl:
			self.addPrimitiveType(node, CharType(), isReferenceDecl)
		elif node.type == ASTNodeType.BoolDecl:
			self.addPrimitiveType(node, BoolType(), isReferenceDecl)			
		elif node.type == ASTNodeType.FunctionDecl:
			self.checkDuplicateDeclaration(node)
			self.addFunctionSignature(node)
		elif node.type == ASTNodeType.ArrayDecl:
			self.checkDuplicateDeclaration(node)
			arrayType = PointerType(mapNodeToVarType(node.children[0].value), node.children[0].value.ptrCount)
			size = node.children[1].value
			self.symbolTable.insertEntry(str(node.value), ArrayType(arrayType, size), Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)
		elif type(node.type) is pointerType:
			# Exception for functionDecls -> do not add the 'declared' symbols to the table
			if self.isSignatureType(node.type.type):
				return
			
			self.checkDuplicateDeclaration(node)			
			# Type consists of the primitive type + optionally pointer operators
			symbolType = PointerType(mapNodeToVarType(node.type), node.type.ptrCount)
			if isReferenceDecl:
				symbolType = ReferenceType(symbolType)

			self.symbolTable.insertEntry(str(node.value), symbolType, Scope.GLOBAL if self.currentLevel == 0 else Scope.LOCAL)

	def getTypeDecl(self, node):
		if node.type == ASTNodeType.FloatDecl or \
				node.type == ASTNodeType.IntDecl or \
				node.type == ASTNodeType.CharDecl or \
				node.type == ASTNodeType.BoolDecl:
			return mapTypeToVarType(node.type)
		elif node.type == ASTNodeType.ArrayDecl:
			arrayType = PointerType(mapNodeToVarType(node.children[0].value), node.children[0].value.ptrCount)
			size = node.children[1].value
			return ArrayType(arrayType, size)
		elif type(node.type) is pointerType:
			return PointerType(mapNodeToVarType(node.type), node.type.ptrCount)

		return None

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
		elif _type == ASTNodeType.BoolSignature:
			return True
		return False

	def leaveScopes(self, nodeLevel):
		"""
			Leaves one or more scopes according the the depth level of the current node.
		"""
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


	def addUsedVariablesFunction(self, functionType, rootNode):
		queue = [rootNode]

		while len(queue) != 0:
			node = queue.pop(0)
			for child in node.children:
				queue.append(child)
		
			possibleDecl = self.getTypeDecl(node)
			if possibleDecl != None:
				functionType.addDeclaredVariable(possibleDecl)
		


def mapNodeToVarType(node):
	if node.type == ASTNodeType.ByReference:
		return mapNodeToVarType(node.children[0])

	return mapTypeToVarType(node.type)




