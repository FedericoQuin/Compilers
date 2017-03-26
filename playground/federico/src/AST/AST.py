
from AST.ASTNode import ASTNode

class AST:
	def __init__(self):
		self.root = ASTNode("Program")
		self.currentPointer = self.root

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "root -> " + str(self.root.uniqueID) + ";\n" + "}"

	def addStatement(self, ctx):
		newNode = self.currentPointer.addChild("Statement")
		newNode.addChild("Type", ctx.TYPE())
		newNode.addChild("ID", ctx.ID())

	def addDeclaration(self, ctx):
		self.currentPointer.addChild(str(ctx.TYPE()) + "dcl", ctx.ID())


