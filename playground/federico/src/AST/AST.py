
from AST.ASTNode import ASTNode, ASTNodeType, getStringOfArray


class AST:
	def __init__(self):
		self.root = ASTNode(ASTNodeType.Program)
		self.currentPointer = self.root

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "}"

	def addDeclaration(self, ctx):
		_type = None
		if (str(ctx.TYPE()) == "int"):
			_type = ASTNodeType.IntDecl
		elif (str(ctx.TYPE()) == "float"):
			_type = ASTNodeType.FloatDecl
		elif (str(ctx.TYPE()) == "char"):
			_type = ASTNodeType.CharDecl

		self.currentPointer.addChild(_type, ctx.ID())

	def addRvalue(self, ctx):
		if (ctx.CHARVALUE() != None):
			self.currentPointer.addChild(ASTNodeType.RValueChar, ctx.CHARVALUE())
		elif (ctx.numericalvalue() != None):
			if (ctx.numericalvalue().intvalue() != None):
				self.currentPointer.addChild( \
					ASTNodeType.RValueInt, \
					getStringOfArray(ctx.numericalvalue().intvalue().DIGIT()) )

			elif (ctx.numericalvalue().floatvalue() != None and len(ctx.numericalvalue().floatvalue().digits()) == 2 ):
				self.currentPointer.addChild( \
					ASTNodeType.RValueFloat, \
					getStringOfArray(ctx.numericalvalue().floatvalue().digits(0).DIGIT())
					+ "." \
					+ getStringOfArray(ctx.numericalvalue().floatvalue().digits(1).DIGIT()) )

			elif (ctx.numericalvalue().floatvalue() != None and len(ctx.numericalvalue().floatvalue().digits()) == 1 ):
				self.currentPointer.addChild( \
					ASTNodeType.RValueFloat, \
					"." \
					+ getStringOfArray(ctx.numericalvalue().floatvalue().digits(0).DIGIT()) )

	def addAssignment(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Assignment)
		if (ctx.lvalue().ID() != None):
			self.currentPointer.addChild(ASTNodeType.LValue, ctx.lvalue().ID())
		else:
			pass

	def endAssignment(self):
		self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent



