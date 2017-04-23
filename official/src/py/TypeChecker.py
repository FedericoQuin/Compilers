from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType
from src.SymbolTable import *
from src.SymbolTableBuilder import *


class TypeChecker:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable
		self.leftType = None
		self.rightType = None
		self.nodeLevel = 0

	def checkType(self, node, nodeLevel):
		# nodeLevel might be temporary, not sure yet
		if (self.nodeLevel >= nodeLevel):
			self.leftType = None
			self.rightType = None
		

		if (node.type == ASTNodeType.Assignment):
			self.nodeLevel = nodeLevel
			# Left type is always present directly
			self.leftType = self.getLType(node.children[0])
			# Right type on the other hand, not entirely
			self.rightType = self.getRType(node.children[1])
			# print(str(self.leftType) + " - " + str(self.rightType))

			if self.rightType != None and self.leftType != None and self.leftType != self.rightType:
				raise Exception("Types for assignments don't match: " + str(type(self.leftType)) + " - " + str(type(self.rightType)))

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
		elif (type(node) is pointerType):
			return PointerType(self.getLType(node.type), node.ptrCount)

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


	def checkTypeChildrenExpression(self, children):
		type1 = self.getRType(children[0])
		type2 = self.getRType(children[1])
		if (type1 != type2):
			raise Exception("Types do not match: " + str(type1) + " and " + str(type2))
		return type1
		
		return None



