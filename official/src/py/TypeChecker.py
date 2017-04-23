from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType
from src.SymbolTable import *


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

			if self.rightType != None and self.leftType != None and self.leftType != self.rightType:
				print("Should maybe happen, not sure, with value: " + str(self.leftType) + " - " + str(self.rightType))

	def getLType(self, node):
		if (node.type == ASTNodeType.LValue):
			return self.symbolTable.lookupSymbol(node.value)
		return None

	def getRType(self, node, _type=None):
		if (node.type == ASTNodeType.RValueChar):
			return CharType()
		elif (node.type == ASTNodeType.RValueInt):
			return IntType()
		elif (node.type == ASTNodeType.RValueFloat):
			return FloatType()
		elif (node.type == ASTNodeType.RValueID):
			return self.symbolTable.lookupSymbol(node.value)
		
		return None



