from src.py.AST.ASTNode import ASTNode, ASTNodeType, pointerType


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
			self.leftType = self.symbolTable.lookupSymbol(node.children[0].value)
			# Right type on the other hand, not entirely
			self.rightType = self.getRType(node)

	def getRType(self, node):
		pass
