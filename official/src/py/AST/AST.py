
from AST.ASTNode import ASTNode, ASTNodeType, getStringOfArray, pointerType


class AST:
	def __init__(self):
		self.root = ASTNode(ASTNodeType.Program)
		self.currentPointer = self.root

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "}"

	#====================================================================
	#= 							Declarations							=
	#====================================================================
	def addNormalDeclaration(self, ctx):
		_type = None
		if (ctx.dec_type().INT() != None):
			_type = ASTNodeType.IntDecl
		elif (ctx.dec_type().FLOAT() != None):
			_type = ASTNodeType.FloatDecl
		elif (ctx.dec_type().CHAR() != None):
			_type = ASTNodeType.CharDecl

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		self.currentPointer.addChild(pointerType(_type, ptrCount), ctx.ID())
	
	def addArrayDeclaration(self, ctx):
		# Same as a normal declaration (the type part), with the addition of the 'array' itself

		# Add the first node (arraydecl with value ID)
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ArrayDecl, ctx.ID())

		# Add subsequent nodes for array decl (array type and array size)
		_type = None
		if (ctx.dec_type().INT() != None):
			_type = ASTNodeType.IntDecl
		elif (ctx.dec_type().FLOAT() != None):
			_type = ASTNodeType.FloatDecl
		elif (ctx.dec_type().CHAR() != None):
			_type = ASTNodeType.CharDecl

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		if (ptrCount > 0):
			self.currentPointer.addChild(ASTNodeType.ArrayType, pointerType(_type, ptrCount))
		else:
			self.currentPointer.addChild(ASTNodeType.ArrayType, _type.name)
	
		self.currentPointer.addChild(ASTNodeType.ArraySize, int(getStringOfArray(ctx.digits().DIGIT())))
		self.climbTree()


	#====================================================================
	#= 						Array element access						=
	#====================================================================

	def addArrayElement(self, ctx, val):
		_type = None
		if (val == "lvalue"):
			_type = ASTNodeType.LValueArrayElement
		elif (val == "rvalue"):
			_type = ASTNodeType.RValueArrayElement

		if (ctx.arrayelement().digits() != None):
			self.currentPointer = self.currentPointer.addChild(_type, ctx.arrayelement().ID(0))
			self.currentPointer.addChild(ASTNodeType.ArrayElementIndex, int(getStringOfArray(ctx.arrayelement().digits().DIGIT())))
			self.climbTree()
		elif (len(ctx.arrayelement().ID()) == 2):
			self.currentPointer = self.currentPointer.addChild(_type, ctx.arrayelement().ID(0))
			self.currentPointer.addChild(ASTNodeType.ArrayElementIndex, str(ctx.arrayelement().ID(1)))
			self.climbTree()

	#====================================================================
	#= 						RValue handling								=
	#====================================================================

	def addNumericalValue(self, ctx):
		if (ctx.intvalue() != None):
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueInt)
		elif (ctx.floatvalue() != None):
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueFloat)

	def addCharValue(self, ctx):
		self.currentPointer.addChild(ASTNodeType.RValueChar, ctx.CHARVALUE())

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

	def addFunctionCall(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionCall, ctx.ID())

	#====================================================================



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


	def enterID(self, ctx, val):
		if (val == "lvalue"):
			self.currentPointer.addChild(ASTNodeType.LValue, ctx.ID())
		elif (val == "rvalue"):
			self.currentPointer.addChild(ASTNodeType.RValueID, ctx.ID())


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

	# Enter a parse tree produced by cGrammarParser#bracket_condition.
	def makeBrackets(self, ctx, negate = False):
		if not negate:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Brackets)
		else:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.NegateBrackets)

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

	
	#################################################
	# Break-continue stuff							#
	#################################################
	# Enter a parse tree produced by cGrammarParser#break_stmt.
	def enterBreak_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Break)
	
	# Enter a parse tree produced by cGrammarParser#continue_stmt.
	def enterContinue_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Continue)

	# Enter a parse tree produced by cGrammarParser#return_stmt.
	def returnStmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Return)




	#################################################
	# For stuff										#
	#################################################
	# Enter a parse tree produced by cGrammarParser#for_loop.
	def enterFor_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.For)


	# Enter a parse tree produced by cGrammarParser#first_for_statements.
	def enterFirst_for_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody)


	# Enter a parse tree produced by cGrammarParser#first_for_statement.
	def enterFirst_for_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody)


	# Enter a parse tree produced by cGrammarParser#first_stmt_for.
	def enterFirst_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt1)


	# Enter a parse tree produced by cGrammarParser#second_stmt_for.
	def enterSecond_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt2)


	# Enter a parse tree produced by cGrammarParser#third_stmt_for.
	def enterThird_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt3)


	#################################################
	# Function stuff								#
	#################################################
	# Enter a parse tree produced by cGrammarParser#functiondecl.
	def enterFunctiondecl(self, ctx):
		_type = None
		ptrCount = 0
		if ctx.returntype().dec_type() != None:

			if (ctx.returntype().dec_type().INT() != None):
				_type = ASTNodeType.IntDecl
			elif (ctx.returntype().dec_type().FLOAT() != None):
				_type = ASTNodeType.FloatDecl
			elif (ctx.returntype().dec_type().CHAR() != None):
				_type = ASTNodeType.CharDecl

			nextPtr = ctx.returntype().dec_type().ptr()
			if nextPtr != None:
				nextPtr = nextPtr.ptr()
			while nextPtr != None:
				ptrCount += 1
				nextPtr = nextPtr.ptr()

			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Function, ctx.ID())
		elif ctx.returntype().VOID() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Function, ctx.ID())
			_type = ASTNodeType.Void
		self.currentPointer.addChild(pointerType(_type, ptrCount))

	# Enter a parse tree produced by cGrammarParser#initialargument.
	def addArgumentList(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionArgs)

	# Enter a parse tree produced by cGrammarParser#argument.
	def addArgument(self, ctx):
		self.addNormalDeclaration(ctx)

	def addFunctionBody(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionBody)




	
	def climbTree(self):
		''' 
			Name is still a WIP :p
		'''
		self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent



