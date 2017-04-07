
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
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueChar, ctx.CHARVALUE())
		elif (ctx.numericalvalue() != None):
			if (ctx.numericalvalue().intvalue() != None):
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueInt)
			elif (ctx.numericalvalue().floatvalue() != None):
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueFloat)

	def setIntValueNode(self, ctx):
		self.currentPointer.value = int(getStringOfArray(ctx.DIGIT()))

	def setFloatValueNode(self, ctx):
		floatString = ""
		if (len(ctx.digits()) == 1):
			floatString = "0." + getStringOfArray(ctx.digits(0).DIGIT())
		elif (len(ctx.digits()) == 2):
			floatString = \
				getStringOfArray(ctx.digits(0).DIGIT()) + \
				"." + \
				getStringOfArray(ctx.digits(1).DIGIT())
		
		self.currentPointer.value = float(floatString)

	def addAssignment(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Assignment)
		if (ctx.lvalue().ID() != None):
			self.currentPointer.addChild(ASTNodeType.LValue, ctx.lvalue().ID())
		else:
			# TODO throw exception maybe?
			pass

	def enterExpression(self, ctx):
		if ctx.OPERATOR_AS() != None:
			self.addAssignment(ctx)
		elif ctx.POST_OPERATOR_INCR() != None:
			self.currentPointer.addChild(ASTNodeType.PostfixIncr, ctx.ID())
		elif ctx.PRE_OPERATOR_INCR() != None:
			self.currentPointer.addChild(ASTNodeType.PrefixIncr, ctx.ID())
		elif ctx.POST_OPERATOR_DECR() != None:
			self.currentPointer.addChild(ASTNodeType.PostfixDecr, ctx.ID())
		elif ctx.PRE_OPERATOR_DECR() != None:
			self.currentPointer.addChild(ASTNodeType.PrefixDecr, ctx.ID())

	def enterAddSub(self, ctx):
		if ctx.OPERATOR_PLUS() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Addition)
		elif ctx.OPERATOR_MINUS() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Subtraction)

	def enterMulDiv(self, ctx):
		if ctx.OPERATOR_MUL() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Mul)
		elif ctx.OPERATOR_DIV() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Div)


	def enterID(self, ctx):
		self.currentPointer.addChild(ASTNodeType.LValue, ctx.ID())


	
	def climbTree(self):
		''' 
			Name is still a WIP :p
		'''
		self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent



