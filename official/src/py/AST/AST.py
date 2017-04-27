
from src.py.AST.ASTNode import ASTNode, ASTNodeType, getStringOfArray, pointerType


class AST:
	def __init__(self):
		self.root = ASTNode(ASTNodeType.Program)
		self.currentPointer = self.root

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "}"




	#====================================================================
	#= 							Includes								=
	#====================================================================
	def addInclude(self, ctx):
		includeName = str(ctx.INCLUDE_FILE())
		self.currentPointer.addChild(ASTNodeType.Include, includeName[includeName.find('<') + 1 : len(includeName) - 1])


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

		self.currentPointer = self.currentPointer.addChild(pointerType(_type, ptrCount), str(ctx.ID()))
		# if ctx.initialization() == None:
		# 	self.climbTree()

	
	def addArrayDeclaration(self, ctx):
		# Same as a normal declaration (the type part), with the addition of the 'array' itself

		# Add the first node (arraydecl with value ID)
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ArrayDecl, str(ctx.ID()))

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

		self.currentPointer.addChild(ASTNodeType.ArrayType, pointerType(_type, ptrCount))
		self.currentPointer.addChild(ASTNodeType.ArraySize, int(getStringOfArray(ctx.digits().DIGIT())))

	def addInitialization(self):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Initialization)

	#====================================================================
	#= 						Array element access						=
	#====================================================================

	def addArrayElement(self, ctx, val):
		_type = None
		if (val == "lvalue"):
			_type = ASTNodeType.LValueArrayElement
		elif (val == "rvalue"):
			_type = ASTNodeType.RValueArrayElement

		self.currentPointer = self.currentPointer.addChild(_type, str(ctx.arrayelement().ID()))


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
		self.currentPointer.value = int(("" if ctx.OPERATOR_MINUS() == None else "-") + getStringOfArray(ctx.DIGIT()))

	def setFloatValueNode(self, ctx):
		floatString = ""
		if len(ctx.digits()) == 1:
			floatString = ("" if ctx.OPERATOR_MINUS() == None else "-") + "0." + getStringOfArray(ctx.digits(0).DIGIT())
		elif len(ctx.digits()) == 2:
			floatString = ("" if ctx.OPERATOR_MINUS() == None else "-") + \
				getStringOfArray(ctx.digits(0).DIGIT()) + \
				"." + \
				getStringOfArray(ctx.digits(1).DIGIT())
		
		self.currentPointer.value = float(floatString)

	def addFunctionCall(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionCall, str(ctx.ID()))



	#====================================================================
	#= 					Pointers and addresses							=
	#====================================================================

	def addAddressOf(self):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueAddress)


	def addDereference(self, ctx):
		# Don't add a node if this one is just adding brackets
		if ctx.dereference_bracket() != None:
			return
		
		if self.currentPointer.type == ASTNodeType.Dereference:
			self.currentPointer.value += "".join([ "*" for i in range(len(ctx.OPERATOR_MUL())) ])
		else:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Dereference, "".join(["*" for i in range(len(ctx.OPERATOR_MUL()))]))

	#====================================================================
	#= 					Assignments and Expressions						=
	#====================================================================

	def addAssignment(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Assignment)

	def enterExpression(self, ctx):
		if ctx.OPERATOR_AS() != None:
			self.addAssignment(ctx)
		elif ctx.postfix_inc() != None:
			self.currentPointer.addChild(ASTNodeType.PostfixIncr, str(ctx.ID()))
		elif ctx.prefix_inc() != None:
			self.currentPointer.addChild(ASTNodeType.PrefixIncr, str(ctx.ID()))
		elif ctx.postfix_dec() != None:
			self.currentPointer.addChild(ASTNodeType.PostfixDecr, str(ctx.ID()))
		elif ctx.prefix_dec() != None:
			self.currentPointer.addChild(ASTNodeType.PrefixDecr, str(ctx.ID()))

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
			self.currentPointer.addChild(ASTNodeType.LValue, str(ctx.ID()))
		elif (val == "rvalue"):
			self.currentPointer.addChild(ASTNodeType.RValueID, str(ctx.ID()))


	#====================================================================
	#= 							Ifelse									=
	#====================================================================

	def addIfElse(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfElse)

	def enterFirstcondition(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Condition)

	def exitFirstcondition(self, ctx):
		pass

	def enterFirst_true_statements(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue)

	def exitFirst_true_statements(self, ctx):
		pass


	def enterFirst_true_statement(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue)

	def exitFirst_true_statement(self, ctx):
		pass


	def enterFirst_false_statement(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse)

	def exitFirst_false_statement(self, ctx):
		pass


	def enterFirst_false_statements(self, ctx):
		self.climbTree()
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse)

	def enterCondition(self, ctx):
		if ctx.OPERATOR_OR() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Or)

	def exitCondition(self, ctx):
		if ctx.OPERATOR_OR() != None:
			self.climbTree()


	def enterCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.And)

	def exitCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.climbTree()


	def enterCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Not)

	def exitCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.climbTree()

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

	def makeBrackets(self, ctx, negate = False):
		if not negate:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Brackets)
		else:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.NegateBrackets)


	#====================================================================
	#= 								While								=
	#====================================================================

	def enterWhile_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.While)

	def enterFirst_while_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody)

	def enterFirst_while_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody)

	def enterFirst_while_condition(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Condition)

	
	#====================================================================
	#= 							Break continue							=
	#====================================================================

	def enterBreak_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Break)
	
	def enterContinue_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Continue)

	def returnStmt(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Return)




	#====================================================================
	#= 								For									=
	#====================================================================

	def enterFor_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.For)


	def enterFirst_for_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody)


	def enterFirst_for_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody)


	def enterFirst_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt1)


	def enterSecond_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt2)


	def enterThird_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt3)



	#====================================================================
	#= 							Functions								=
	#====================================================================

	def enterFunctiondecl(self, ctx, val):
		_type = None
		ptrCount = 0
		typeNode = ASTNodeType.Function if val == "Function" else ASTNodeType.FunctionDecl
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

			self.currentPointer = self.currentPointer.addChild(typeNode, str(ctx.ID()))
		elif ctx.returntype().VOID() != None:
			self.currentPointer = self.currentPointer.addChild(typeNode, str(ctx.ID()))
			_type = ASTNodeType.Void
		self.currentPointer.addChild(ASTNodeType.ReturnType, pointerType(_type, ptrCount))

	def addFunctionArgumentList(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionArgs)

	def addArgument(self, ctx):
		if (self.currentPointer.parent.type == ASTNodeType.FunctionDecl):
			self.addSignatureArgument(ctx)
		elif (self.currentPointer.parent.type == ASTNodeType.Function):
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

			if ctx.OPERATOR_ADDROF() != None:
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.ByReference)
				self.currentPointer.addChild(pointerType(_type, ptrCount), str(ctx.ID()))
				self.climbTree()
			else:
				self.currentPointer.addChild(pointerType(_type, ptrCount), str(ctx.ID()))
			
	
	def addSignatureArgument(self, ctx):
		_type = None
		if (ctx.dec_type().INT() != None):
			_type = ASTNodeType.IntSignature
		elif (ctx.dec_type().FLOAT() != None):
			_type = ASTNodeType.FloatSignature
		elif (ctx.dec_type().CHAR() != None):
			_type = ASTNodeType.CharSignature

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		self.currentPointer.addChild(pointerType(_type, ptrCount), str(ctx.ID()))

	def addFunctionBody(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionBody)



	#====================================================================
	#= 						Scanf and Printf							=
	#====================================================================

	def addScanf(self):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Scanf)

	def addPrintf(self):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Printf)

	def addFormatString(self, ctx):
		includeName = "".join([str(i) for i in ctx.getChildren()])
		# Don't forget to cut the quotation marks
		self.currentPointer.addChild(ASTNodeType.FormatString, includeName[1:len(includeName)-1])

	
	def climbTree(self, amt = 1):
		''' 
			Name is still a WIP :p
		'''
		for i in range(amt):
			self.currentPointer = self.currentPointer.parent


	def enterBlock(self, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block)
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent



