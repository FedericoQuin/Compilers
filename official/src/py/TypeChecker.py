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

			self.leftType = self.getLType(node.children[0])
			self.rightType = self.getRType(node.children[1])

			if self.rightType != None and self.leftType != None and self.leftType != self.rightType:
				raise Exception("Types for assignment don't match: " + str(self.leftType) + " and " + str(self.rightType))

		elif node.type == ASTNodeType.Greater or node.type == ASTNodeType.GreaterOrEqual or node.type == ASTNodeType.Or or node.type == ASTNodeType.And or node.type == ASTNodeType.Equals or node.type == ASTNodeType.NotEquals or node.type == ASTNodeType.Less or node.type == ASTNodeType.LessOrEqual:
			self.leftType, self.rightType = self.getTypesComparison(node.children)
			if self.rightType != None and self.leftType != None and self.leftType != self.rightType:
				raise Exception("Types for comparison don't match: " + str(self.leftType) + " and " + str(self.rightType))


	def getTypesComparison(self, nodes):
		if (type(nodes) is ASTNode or type(nodes) is pointerType):
			node = nodes
			if node.type == ASTNodeType.Not or node.type == ASTNodeType.Greater or node.type == ASTNodeType.GreaterOrEqual or node.type == ASTNodeType.Or or node.type == ASTNodeType.And or node.type == ASTNodeType.Equals or node.type == ASTNodeType.NotEquals or node.type == ASTNodeType.Less or node.type == ASTNodeType.LessOrEqual:
				return self.getTypesComparison(node.children)
			else:
				return self.getRType(node)
		elif (len(nodes) == 2):
			return (self.getTypesComparison(nodes[0]), self.getTypesComparison(nodes[1]))
		

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


	def checkTypeChildrenExpression(self, children):
		type1 = self.getRType(children[0])
		type2 = self.getRType(children[1])
		if (type1 != type2):
			raise Exception("Types do not match: " + str(type1) + " and " + str(type2))
		return type1
		
		return None



