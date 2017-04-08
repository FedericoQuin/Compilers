
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


	#################################################
	# Ifelse stuff									#
	#################################################
	def addIfElse(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfElse)

	# Enter a parse tree produced by cGrammarParser#firstcondition.
	def enterFirstcondition(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfCondition)

	# Exit a parse tree produced by cGrammarParser#firstcondition.
	def exitFirstcondition(self, ctx):
		pass

	# Enter a parse tree produced by cGrammarParser#first_true_statements.
	def enterFirst_true_statements(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue)

	# Exit a parse tree produced by cGrammarParser#first_true_statements.
	def exitFirst_true_statements(self, ctx):
		pass


	# Enter a parse tree produced by cGrammarParser#first_true_statement.
	def enterFirst_true_statement(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue)

	# Exit a parse tree produced by cGrammarParser#first_true_statement.
	def exitFirst_true_statement(self, ctx):
		pass


	# Enter a parse tree produced by cGrammarParser#first_false_statement.
	def enterFirst_false_statement(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse)

	# Exit a parse tree produced by cGrammarParser#first_false_statement.
	def exitFirst_false_statement(self, ctx):
		pass


	# Enter a parse tree produced by cGrammarParser#first_false_statements.
	def enterFirst_false_statements(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse)

	# Enter a parse tree produced by cGrammarParser#condition.
	def enterCondition(self, ctx):
		if ctx.OPERATOR_OR() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Or)

	# Exit a parse tree produced by cGrammarParser#condition.
	def exitCondition(self, ctx):
		if ctx.OPERATOR_OR() != None:
			self.climbTree()


	# Enter a parse tree produced by cGrammarParser#condition_and.
	def enterCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.And)

	# Exit a parse tree produced by cGrammarParser#condition_and.
	def exitCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.climbTree()


	# Enter a parse tree produced by cGrammarParser#condition_not.
	def enterCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Not)

	# Exit a parse tree produced by cGrammarParser#condition_not.
	def exitCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.climbTree()

	# Enter a parse tree produced by cGrammarParser#comparison.
	def enterComparison(self, ctx):
		if ctx.comparator().OPERATOR_EQ() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Equals)
		elif ctx.comparator().OPERATOR_GT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Greater)
		elif ctx.comparator().OPERATOR_GE() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.GreaterOrEqual)
		elif ctx.comparator().OPERATOR_LT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Less)
		elif ctx.comparator().OPERATOR_LE() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.LessOrEqual)

		if ctx.ID() != None:
			if len(ctx.ID()) == 1:
				self.currentPointer.addChild(ASTNodeType.LValue, ctx.ID()[0])
			else:
				self.currentPointer.addChild(ASTNodeType.LValue, ctx.ID()[0])
				self.currentPointer.addChild(ASTNodeType.LValue, ctx.ID()[1])


	# Exit a parse tree produced by cGrammarParser#comparison.
	def exitComparison(self, ctx):
		if ctx.comparator().OPERATOR_EQ() != None:
			self.climbTree()
		elif ctx.comparator().OPERATOR_GT() != None:
			self.climbTree()
		elif ctx.comparator().OPERATOR_GE() != None:
			self.climbTree()
		elif ctx.comparator().OPERATOR_LT() != None:
			self.climbTree()
		elif ctx.comparator().OPERATOR_LE() != None:
			self.climbTree()


	#################################################
	# While stuff									#
	#################################################
	# Enter a parse tree produced by cGrammarParser#while_loop.
	def enterWhile_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.While)

	# Enter a parse tree produced by cGrammarParser#first_while_statements.
	def enterFirst_while_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody)

	# Enter a parse tree produced by cGrammarParser#first_while_statement.
	def enterFirst_while_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody)

	def enterFirst_while_condition(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileCondition)


	
	def climbTree(self):
		''' 
			Name is still a WIP :p
		'''
		self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent



