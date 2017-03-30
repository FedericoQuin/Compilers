
from AST.ASTNode import ASTNode

class AST:
	def __init__(self):
		self.root = ASTNode("Program")
		self.currentPointer = self.root

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "}"

	def addStatement(self, ctx):
		newNode = self.currentPointer.addChild("Statement")
		newNode.addChild("Type", ctx.TYPE())
		newNode.addChild("ID", ctx.ID())

	def addDeclaration(self, ctx):
		self.currentPointer.addChild(str(ctx.TYPE()) + "dcl", ctx.ID())

	def addRvalue(self, ctx):
		if (ctx.CHARVALUE() != None):
			self.currentPointer.addChild("rvalue char", ctx.CHARVALUE())
		elif (ctx.numericalvalue() != None):
			if (ctx.numericalvalue().intvalue() != None):
				self.currentPointer.addChild( \
					"rvalue int", \
					''.join([str(digit) for digit in ctx.numericalvalue().intvalue().DIGIT()]) )
			elif (ctx.numericalvalue().floatvalue() != None and len(ctx.numericalvalue().floatvalue().digits()) == 2 ):
				self.currentPointer.addChild( \
					"rvalue float", \
					''.join([str(digit) for digit in ctx.numericalvalue().floatvalue().digits(0).DIGIT()]) \
					+ "." \
					+ ''.join([str(digit) for digit in ctx.numericalvalue().floatvalue().digits(1).DIGIT()]) )
			elif (ctx.numericalvalue().floatvalue() != None and len(ctx.numericalvalue().floatvalue().digits()) == 1 ):
				self.currentPointer.addChild( \
					"rvalue float", \
					"." \
					+ ''.join([str(digit) for digit in ctx.numericalvalue().floatvalue().digits(0).DIGIT()]) )

	def addAssignment(self, ctx):
		self.currentPointer = self.currentPointer.addChild("assignment")
		if (ctx.lvalue().ID() != None):
			self.currentPointer.addChild("lvalue", ctx.lvalue().ID())
		else:
			pass

	def endAssignment(self):
		self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(name)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent




