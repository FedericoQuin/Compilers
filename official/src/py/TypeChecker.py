from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType
from src.SymbolTable import *
from src.SymbolTableBuilder import *


class TypeChecker:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable

	def checkType(self, node):

		# Type checking for assignment between lvalue and rvalue
		if (node.type == ASTNodeType.Assignment):
			leftType = self.getLType(node.children[0])
			rightType = self.getRType(node.children[1])

			if rightType != None and leftType != None and leftType != rightType:
				raise Exception("Types for assignment don't match: " + leftType.getStrType() + " and " + rightType.getStrType() + ".")
		
		# Type checking left side and right side of condition (if present)
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
		
		# Type checking for arguments given with a function call
		elif node.type == ASTNodeType.FunctionCall:
			self.checkCallArguments(node)



	def checkCallArguments(self, node):
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
		if node.type == ASTNodeType.Greater or node.type == ASTNodeType.GreaterOrEqual or node.type == ASTNodeType.Or or node.type == ASTNodeType.And or node.type == ASTNodeType.Equals or node.type == ASTNodeType.NotEquals or node.type == ASTNodeType.Less or node.type == ASTNodeType.LessOrEqual:
			type1 = self.getTypeComparison(node.children[0])
			type2 = self.getTypeComparison(node.children[1])
			if (type1 != type2):
				raise Exception("Types do not match: " + type1.getStrType() + " and " + type2.getStrType())
			return type1
		elif node.type == ASTNodeType.Not:
			return self.getTypeComparison(node.children[0])
		else:
			return self.getRType(node)
		

	def getLType(self, node):
		if (node.type == ASTNodeType.LValue):
			return self.symbolTable.lookupSymbol(node.value).type
		elif (node.type == ASTNodeType.LValueArrayElement):
			return self.symbolTable.lookupSymbol(node.value).type
		elif (node.type == ASTNodeType.ArrayDecl):
			arrayType = PointerType(mapToPrimitiveType(node.children[0].value.type), node.children[0].value.ptrCount)
			size = node.children[1].value
			return ArrayType(arrayType, size)
		elif (node.type == ASTNodeType.IntDecl):
			return IntType()
		elif (node.type == ASTNodeType.CharDecl):
			return CharType()
		elif (node.type == ASTNodeType.FloatDecl):
			return FloatType()
		elif (type(node.type) is pointerType):
			return PointerType(self.getLType(node.type), node.type.ptrCount)

		return None

	def getRType(self, node):
		if (node.type == ASTNodeType.RValueChar):
			return CharType()
		elif (node.type == ASTNodeType.RValueInt):
			return IntType()
		elif (node.type == ASTNodeType.RValueFloat):
			return FloatType()
		elif (node.type == ASTNodeType.RValueID):
			return self.symbolTable.lookupSymbol(node.value).type
		elif (node.type == ASTNodeType.Addition):
			return self.checkTypeChildrenExpression(node.children)
		elif (node.type == ASTNodeType.Subtraction):
			return self.checkTypeChildrenExpression(node.children)
		elif (node.type == ASTNodeType.Mul):
			return self.checkTypeChildrenExpression(node.children)
		elif (node.type == ASTNodeType.Div):
			return self.checkTypeChildrenExpression(node.children)
		elif (node.type == ASTNodeType.Brackets):
			return self.getRType(node.children[0])
		elif (node.type == ASTNodeType.FunctionCall):
			return self.symbolTable.lookupSymbol(node.value).type
		elif (node.type == ASTNodeType.RValueArrayElement):
			return self.symbolTable.lookupSymbol(node.value).type


	def checkTypeChildrenExpression(self, children):
		type1 = self.getRType(children[0])
		type2 = self.getRType(children[1])
		if (type1 != type2):
			raise Exception("Types do not match: " + type1.getStrType() + " and " + type2.getStrType() + ".")
		return type1
		
		return None



