from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType
from src.py.ST.SymbolTable import *
from src.py.ST.SymbolTableBuilder import SymbolTableBuilder
from src.py.UTIL.VarTypes import *
from src.py.UTIL.TypeDeductor import TypeDeductor


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
				leftType = TypeDeductor.checkDereferenceValidity(node.children[0], self.symbolTable)
			else:
				leftType = self.symbolTable.lookupSymbol(node.children[0].value).type
			
			rightType = None
			if node.children[1].type == ASTNodeType.Dereference:
				rightType = TypeDeductor.checkDereferenceValidity(node.children[1], self.symbolTable)
			else:
				rightType = TypeDeductor.deductType(node.children[1], self.symbolTable)

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
				leftType = TypeDeductor.deductType(currentNode.children[0], self.symbolTable)
				rightType = TypeDeductor.deductType(currentNode.children[1], self.symbolTable)
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
			returnType = TypeDeductor.deductType(node.children[0], self.symbolTable) if len(node.children) == 1 else VoidType()

			if returnType != None and functionReturnType != None and functionReturnType != returnType:
				raise Exception("Return type doesn't match '" + functionSymbol + "' signature: " + functionReturnType.getStrType() + " and " + returnType.getStrType() + ".")

		#==================================
		# Type checking for initializations
		#==================================
		elif node.type == ASTNodeType.Initialization:
			# Check between the parent node and the child node
			leftType = self.symbolTable.lookupSymbol(node.parent.value).type
			rightType = TypeDeductor.deductType(node.children[0], self.symbolTable)

			if rightType != leftType:
				raise Exception("Types for initialization don't match: " + leftType.getStrType() + " and " + rightType.getStrType() + ".")

		#======================================
		# Type checking for array element index
		#======================================
		elif node.type == ASTNodeType.LValueArrayElement or node.type == ASTNodeType.RValueArrayElement:
			# Make sure that the index is a (positive -> TODO at runtime?) int value
			indexType = TypeDeductor.deductType(node.children[0], self.symbolTable)
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
			TypeDeductor.checkDereferenceValidity(node, self.symbolTable)




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
			if argumentRequired != TypeDeductor.deductType(argumentGiven, self.symbolTable):
				raise Exception("Argument for function call '" + str(node.value) + "' did not match the signature: " \
					+ argumentRequired.getStrType() + " and " + TypeDeductor.deductType(argumentGiven, self.symbolTable).getStrType() + " (argument #" + str(arguments.index(argumentGiven)+1) + ")." )

		
	
	def getFirstFunctionSymbol(self, node):
		"""
			Returns the first function symbol found, starting from node and moving upwards
		"""
		if node.type == ASTNodeType.Function:
			return str(node.value)
		else:
			return self.getFirstFunctionSymbol(node.parent)


