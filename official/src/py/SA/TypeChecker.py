from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType
from src.py.ST.SymbolTable import *
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.VarTypes import *


class TypeChecker:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable

	def checkType(self, node):
		"""
			Do type checking dependent on the provided node.
		"""

		#=======================================================
		# Type checking for assignment between lvalue and rvalue
		#=======================================================
		if node.type == ASTNodeType.Assignment:
			# Exception for Dereference -> search the Symbol and dereference enough times
			leftType = None
			if node.children[0].type == ASTNodeType.Dereference:
				leftType = self.checkDereferenceValidity(node.children[0])
			else:
				leftType = self.symbolTable.lookupSymbol(node.children[0].value).type
			
			rightType = None
			if node.children[1].type == ASTNodeType.Dereference:
				rightType = self.checkDereferenceValidity(node.children[1])
			else:
				rightType = self.getRType(node.children[1])

			if rightType != None and leftType != None and leftType != rightType:
				raise Exception("Types for assignment don't match: " + leftType.getStrType() + " and " + rightType.getStrType() + ".")
		
		#=================================================================
		# Type checking left side and right side of condition (if present)
		#=================================================================
		elif node.type == ASTNodeType.Condition:
			currentNode = node.children[0]
			if len(currentNode.children) == 1 and currentNode.children[0].type == ASTNodeType.Not:
				# No checking needs to be done if it is not compared to anything
				pass
			elif len(currentNode.children) == 2:
				leftType = self.getTypeComparison(currentNode.children[0])
				rightType = self.getTypeComparison(currentNode.children[1])
				if rightType != None and leftType != None and leftType != rightType:
					raise Exception("Types for comparison don't match: " + leftType.getStrType() + " and " + rightType.getStrType() + ".")
		
		#=======================================================
		# Type checking for arguments given with a function call
		#=======================================================
		elif node.type == ASTNodeType.FunctionCall:
			self.checkCallArguments(node)
		
		#==============================
		# Type checking for return type
		#==============================
		elif node.type == ASTNodeType.Return:
			functionSymbol = self.getFirstFunctionSymbol(node)
			functionReturnType = self.symbolTable.lookupSymbol(functionSymbol).type.returnType
			returnType = self.getRType(node.children[0]) if len(node.children) == 1 else VoidType()

			if returnType != None and functionReturnType != None and functionReturnType != returnType:
				raise Exception("Return type doesn't match '" + functionSymbol + "' signature: " + functionReturnType.getStrType() + " and " + returnType.getStrType() + ".")

		#==================================
		# Type checking for initializations
		#==================================
		elif node.type == ASTNodeType.Initialization:
			# Check between the parent node and the child node
			leftType = self.symbolTable.lookupSymbol(node.parent.value).type
			rightType = self.getRType(node.children[0])

			if rightType != leftType:
				raise Exception("Types for initialization don't match: " + leftType.getStrType() + " and " + rightType.getStrType() + ".")

		#======================================
		# Type checking for array element index
		#======================================
		elif node.type == ASTNodeType.LValueArrayElement or node.type == ASTNodeType.RValueArrayElement:
			# Make sure that the index is a (positive -> TODO at runtime?) int value
			indexType = self.getRType(node.children[0])
			if indexType != IntType():
				raise Exception("Elements of array '" + str(node.value) + "' should be accessed with an integer.")

		#=========================================
		# Type checking for dereference operations
		#=========================================
		elif node.type == ASTNodeType.Dereference:
			"""
				Requires 3 forms of checking:
					* Contains at least one RValueID
					* If expressions are present, only intvalues should be allowed (array element access)
					* The pointer which is dereferenced has at least the same pointer count as dereference count
			"""
			self.checkDereferenceValidity(node)




	def checkDereferenceValidity(self, node):
		"""
			Checks the validity of dereferencing.
			Returns the type after dereferencing.
		"""
		queue = [node]
		rvalueSymbol = None
		derefCount = 0

		while len(queue) != 0:
			currentNode = queue.pop()
			[queue.append(i) for i in currentNode.children]

			if currentNode.type == ASTNodeType.Dereference:
				derefCount += len(currentNode.value)
			elif currentNode.type == ASTNodeType.RValueID:
				if rvalueSymbol != None:
					raise Exception("Error: cannot dereference more than 1 variable.")
				rvalueSymbol = currentNode.value
			else:
				# All other nodes are part of an expression
				rType = type(self.getRType(currentNode))
				if not(rType is IntType) and not(rType is PointerType):
					raise Exception("Error: cannot dereference non-int/pointer expressions.")
		
		rvalueIdType = self.symbolTable.lookupSymbol(rvalueSymbol).type
		if not(type(rvalueIdType) is PointerType):
			raise Exception("Error: cannot dereference non-pointer variable '" + str(rvalueSymbol) + "'.")
		if derefCount > rvalueIdType.ptrCount:
			if rvalueIdType.ptrCount == 0:
				raise Exception("Error: cannot dereference non-pointer variable '" + str(rvalueSymbol) + "'.")
			raise Exception("Error: cannot dereference variable '" + rvalueSymbol + "' " + str(derefCount) + " times (only " \
				+ str(rvalueIdType.ptrCount) + (" times" if rvalueIdType.ptrCount != 1 else " time") + " allowed).")

		return rvalueIdType.dereference(derefCount)


	def checkCallArguments(self, node):
		"""
			Checks the signature types of a function with the types of the given call arguments.
		"""
		arguments = node.children
		functionSignature = self.symbolTable.lookupSymbol(node.value).type

		amtArgumentsRequired = len(functionSignature.arguments)
		amtArgumentsGiven = len(arguments)
		if amtArgumentsRequired != amtArgumentsGiven:
			raise Exception("Function arguments invalid: '" + str(node.value) + "' takes " \
				+ str(amtArgumentsRequired) + " " + ("arguments" if amtArgumentsRequired != 1 else "argument") + " " + \
				"(" + str(amtArgumentsGiven) + " " + ("arguments" if amtArgumentsGiven != 1 else "argument") + " given).")
		
		for argumentRequired, argumentGiven in zip(functionSignature.arguments, arguments):
			# Check the types for every argument given
			if argumentRequired != self.getRType(argumentGiven):
				raise Exception("Argument for function call '" + str(node.value) + "' did not match the signature: " \
					+ argumentRequired.getStrType() + " and " + self.getRType(argumentGiven).getStrType() + " (argument #" + str(arguments.index(argumentGiven)+1) + ")." )


	def getTypeComparison(self, node):
		"""
			Checks and validates that both types in the comparison are equal, throws Exception otherwise.
			Returns the type if both are equal.
		"""
		if node.type == ASTNodeType.Greater or node.type == ASTNodeType.GreaterOrEqual or node.type == ASTNodeType.Or or node.type == ASTNodeType.And or node.type == ASTNodeType.Equals or node.type == ASTNodeType.NotEquals or node.type == ASTNodeType.Less or node.type == ASTNodeType.LessOrEqual:
			type1 = self.getTypeComparison(node.children[0])
			type2 = self.getTypeComparison(node.children[1])
			if type1 != type2:
				raise Exception("Types do not match: " + type1.getStrType() + " and " + type2.getStrType())
			return type1
		elif node.type == ASTNodeType.Not or node.type == ASTNodeType.NegateBrackets or node.type == ASTNodeType.Brackets:
			return self.getTypeComparison(node.children[0])
		else:
			return self.getRType(node)
		
	
	def getFirstFunctionSymbol(self, node):
		"""
			Returns the first function symbol found, starting from node and moving upwards
		"""
		if node.type == ASTNodeType.Function:
			return str(node.value)
		else:
			return self.getFirstFunctionSymbol(node.parent)



	def getRType(self, node):
		"""
			Returns the type of the (rvalue) node.
		"""
		if node.type == ASTNodeType.RValueChar:
			return CharType()
		elif node.type == ASTNodeType.RValueInt:
			return IntType()
		elif node.type == ASTNodeType.RValueFloat:
			return FloatType()
		elif node.type == ASTNodeType.RValueID:
			return self.symbolTable.lookupSymbol(node.value).type
		elif node.type == ASTNodeType.Addition:
			return self.checkTypeChildrenExpression(node.children)
		elif node.type == ASTNodeType.Subtraction:
			return self.checkTypeChildrenExpression(node.children)
		elif node.type == ASTNodeType.Mul:
			return self.checkTypeChildrenExpression(node.children)
		elif node.type == ASTNodeType.Div:
			return self.checkTypeChildrenExpression(node.children)
		elif node.type == ASTNodeType.Brackets:
			return self.getRType(node.children[0])
		elif node.type == ASTNodeType.FunctionCall:
			return self.symbolTable.lookupSymbol(node.value).type
		elif node.type == ASTNodeType.RValueArrayElement:
			return self.symbolTable.lookupSymbol(node.value).type
		elif node.type == ASTNodeType.RValueAddress:
			return self.symbolTable.lookupSymbol(node.children[0].value).type.addressOf()
		elif node.type == ASTNodeType.Dereference:
			return self.checkDereferenceValidity(node)
		else:
			raise Exception("Could not deduct type of node '" + str(node.type.name) + "'.")


	def checkTypeChildrenExpression(self, children):
		"""
			Compares the types of the children. If the types differ: throw Exception.
			Returns the type of the children if equal.
		"""
		type1 = self.getRType(children[0])
		type2 = self.getRType(children[1])
		if (type1 != type2):
			raise Exception("Types do not match: " + type1.getStrType() + " and " + type2.getStrType() + ".")
		return type1
		


