
from src.py.AST.ASTNode import ASTNode, ASTNodeType, getStringOfArray, pointerType


class AST:
	def __init__(self, tokenStream):
		self.root = ASTNode(ASTNodeType.Program)
		self.currentPointer = self.root
		self.tokenStream = tokenStream

	def __str__(self):
		return "digraph AST {\n" + str(self.root) + "}"




	#====================================================================
	#= 							Includes								=
	#====================================================================
	def addInclude(self, ctx):
		includeName = str(ctx.INCLUDE_FILE())
		self.currentPointer.addChild(ASTNodeType.Include, self.getPosition(ctx), includeName[includeName.find('<') + 1 : len(includeName) - 1])


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
		elif (ctx.dec_type().BOOL() != None):
			_type = ASTNodeType.BoolDecl

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		self.currentPointer = self.currentPointer.addChild(pointerType(_type, ptrCount), self.getPosition(ctx), str(ctx.ID()))
		# if ctx.initialization() == None:
		# 	self.climbTree()

	
	def addArrayDeclaration(self, ctx):
		# Same as a normal declaration (the type part), with the addition of the 'array' itself

		# Add the first node (arraydecl with value ID)
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ArrayDecl, self.getPosition(ctx), str(ctx.ID()))

		# Add subsequent nodes for array decl (array type and array size)
		_type = None
		if (ctx.dec_type().INT() != None):
			_type = ASTNodeType.IntDecl
		elif (ctx.dec_type().FLOAT() != None):
			_type = ASTNodeType.FloatDecl
		elif (ctx.dec_type().CHAR() != None):
			_type = ASTNodeType.CharDecl
		elif (ctx.dec_type().BOOL() != None):
			_type = ASTNodeType.BoolDecl

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		self.currentPointer.addChild(ASTNodeType.ArrayType, self.getPosition(ctx), pointerType(_type, ptrCount))
		self.currentPointer.addChild(ASTNodeType.ArraySize, self.getPosition(ctx), int(getStringOfArray(ctx.digits().DIGIT())))

	def addInitialization(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Initialization, self.getPosition(ctx))

	#====================================================================
	#= 						Array element access						=
	#====================================================================

	def addArrayElement(self, ctx, val):
		_type = None
		if (val == "lvalue"):
			_type = ASTNodeType.LValueArrayElement
		elif (val == "rvalue"):
			_type = ASTNodeType.RValueArrayElement

		self.currentPointer = self.currentPointer.addChild(_type, self.getPosition(ctx), str(ctx.arrayelement().ID()))


	#====================================================================
	#= 						RValue handling								=
	#====================================================================

	def addNumericalValue(self, ctx):
		if (ctx.intvalue() != None):
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueInt, self.getPosition(ctx))
		elif (ctx.floatvalue() != None):
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueFloat, self.getPosition(ctx))

	def addCharValue(self, ctx):
		self.currentPointer.addChild(ASTNodeType.RValueChar, self.getPosition(ctx), ctx.CHARVALUE())

	def setIntValueNode(self, ctx):
		self.currentPointer.value = int(getStringOfArray(ctx.DIGIT()))

	def setFloatValueNode(self, ctx):
		floatString = ""
		if len(ctx.digits()) == 1:
			floatString = "0." + getStringOfArray(ctx.digits(0).DIGIT())
		elif len(ctx.digits()) == 2:
			floatString = \
				getStringOfArray(ctx.digits(0).DIGIT()) + \
				"." + \
				getStringOfArray(ctx.digits(1).DIGIT())
		
		self.currentPointer.value = float(floatString)

	def addFunctionCall(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionCall, self.getPosition(ctx), str(ctx.ID()))

	def addNegate(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Negate, self.getPosition(ctx))

	def addTrue(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueBool, self.getPosition(ctx), True)

	def addFalse(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueBool, self.getPosition(ctx), False)


	#====================================================================
	#= 					Pointers and addresses							=
	#====================================================================

	def addAddressOf(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.RValueAddress, self.getPosition(ctx))


	def addDereference(self, ctx):
		value = "*"
		if type(ctx.OPERATOR_MUL()) is list:
			value = "".join(["*" for i in range(len(ctx.OPERATOR_MUL()))])

		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Dereference, self.getPosition(ctx), value)

	#====================================================================
	#= 					Assignments and Expressions						=
	#====================================================================

	def addAssignment(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Assignment, self.getPosition(ctx))

	def enterAddSub(self, ctx):
		if ctx.OPERATOR_PLUS() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Addition, self.getPosition(ctx))
		elif ctx.OPERATOR_MINUS() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Subtraction, self.getPosition(ctx))

	def enterMulDiv(self, ctx):
		if ctx.OPERATOR_MUL() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Mul, self.getPosition(ctx))
		elif ctx.OPERATOR_DIV() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Div, self.getPosition(ctx))


	def enterID(self, ctx, val):
		if (val == "lvalue"):
			self.currentPointer.addChild(ASTNodeType.LValue, self.getPosition(ctx), str(ctx.ID()))
		elif (val == "rvalue"):
			self.currentPointer.addChild(ASTNodeType.RValueID, self.getPosition(ctx), str(ctx.ID()))


	#====================================================================
	#= 							Ifelse									=
	#====================================================================

	def addIfElse(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfElse, self.getPosition(ctx))


	def addIfTrue(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue, self.getPosition(ctx))

	def addIfFalse(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse, self.getPosition(ctx))

	def enterFirst_true_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue, self.getPosition(ctx))



	def enterFirst_true_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfTrue, self.getPosition(ctx))


	def enterFirst_false_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse, self.getPosition(ctx))


	def enterFirst_false_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.IfFalse, self.getPosition(ctx))

	def enterCondition(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Condition, self.getPosition(ctx))



	def enterCondition_or(self, ctx):
		if ctx.OPERATOR_OR() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Or, self.getPosition(ctx))
			

	def enterCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.And, self.getPosition(ctx))

	def exitCondition_and(self, ctx):
		if ctx.OPERATOR_AND() != None:
			self.climbTree()


	def enterCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Not, self.getPosition(ctx))

	def exitCondition_not(self, ctx):
		if ctx.OPERATOR_NOT() != None:
			self.climbTree()

	def enterComparison(self, ctx):
		if ctx.comparator().OPERATOR_EQ() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Equals, self.getPosition(ctx))
		elif ctx.comparator().OPERATOR_GT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Greater, self.getPosition(ctx))
		elif ctx.comparator().OPERATOR_GE() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.GreaterOrEqual, self.getPosition(ctx))
		elif ctx.comparator().OPERATOR_LT() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Less, self.getPosition(ctx))
		elif ctx.comparator().OPERATOR_LE() != None:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.LessOrEqual, self.getPosition(ctx))


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
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.Brackets, self.getPosition(ctx))
		else:
			self.currentPointer = self.currentPointer.addChild(ASTNodeType.NegateBrackets, self.getPosition(ctx))


	#====================================================================
	#= 								While								=
	#====================================================================

	def enterWhile_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.While, self.getPosition(ctx))

	def enterFirst_while_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody, self.getPosition(ctx))

	def enterFirst_while_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.WhileBody, self.getPosition(ctx))

	def enterFirst_while_condition(self, ctx):
		pass

	
	#====================================================================
	#= 							Break continue							=
	#====================================================================

	def enterBreak_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Break, self.getPosition(ctx))
	
	def enterContinue_stmt(self, ctx):
		self.currentPointer.addChild(ASTNodeType.Continue, self.getPosition(ctx))

	def returnStmt(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Return, self.getPosition(ctx))




	#====================================================================
	#= 								For									=
	#====================================================================

	def enterFor_loop(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.For, self.getPosition(ctx))


	def enterFirst_for_statements(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody, self.getPosition(ctx))


	def enterFirst_for_statement(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForBody, self.getPosition(ctx))


	def enterFirst_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt1, self.getPosition(ctx))


	def enterSecond_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt2, self.getPosition(ctx))


	def enterThird_stmt_for(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.ForStmt3, self.getPosition(ctx))



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
			elif (ctx.returntype().dec_type().Bool() != None):
				_type = ASTNodeType.BoolDecl

			nextPtr = ctx.returntype().dec_type().ptr()
			if nextPtr != None:
				nextPtr = nextPtr.ptr()
			while nextPtr != None:
				ptrCount += 1
				nextPtr = nextPtr.ptr()

			self.currentPointer = self.currentPointer.addChild(typeNode, self.getPosition(ctx), str(ctx.ID()))
		elif ctx.returntype().VOID() != None:
			self.currentPointer = self.currentPointer.addChild(typeNode, self.getPosition(ctx), str(ctx.ID()))
			_type = ASTNodeType.Void
		self.currentPointer.addChild(ASTNodeType.ReturnType, self.getPosition(ctx), pointerType(_type, ptrCount))

	def addFunctionArgumentList(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionArgs, self.getPosition(ctx))

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
			elif (ctx.dec_type().BOOL() != None):
				_type = ASTNodeType.BoolDecl

			ptrCount = 0
			nextPtr = ctx.dec_type().ptr()
			if nextPtr != None:
				nextPtr = nextPtr.ptr()
			while nextPtr != None:
				ptrCount += 1
				nextPtr = nextPtr.ptr()

			if ctx.OPERATOR_ADDROF() != None:
				self.currentPointer = self.currentPointer.addChild(ASTNodeType.ByReference, self.getPosition(ctx))
				self.currentPointer.addChild(pointerType(_type, ptrCount), self.getPosition(ctx), str(ctx.ID()))
				self.climbTree()
			else:
				self.currentPointer.addChild(pointerType(_type, ptrCount), self.getPosition(ctx), str(ctx.ID()))
			
	
	def addSignatureArgument(self, ctx):
		_type = None
		if (ctx.dec_type().INT() != None):
			_type = ASTNodeType.IntSignature
		elif (ctx.dec_type().FLOAT() != None):
			_type = ASTNodeType.FloatSignature
		elif (ctx.dec_type().CHAR() != None):
			_type = ASTNodeType.CharSignature
		elif (ctx.dec_type().BOOL() != None):
			_type = ASTNodeType.BoolSignature

		ptrCount = 0
		nextPtr = ctx.dec_type().ptr()
		if nextPtr != None:
			nextPtr = nextPtr.ptr()
		while nextPtr != None:
			ptrCount += 1
			nextPtr = nextPtr.ptr()

		self.currentPointer.addChild(pointerType(_type, ptrCount), self.getPosition(ctx), str(ctx.ID()))

	def addFunctionBody(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.FunctionBody, self.getPosition(ctx))



	#====================================================================
	#= 						Scanf and Printf							=
	#====================================================================

	def addScanf(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Scanf, self.getPosition(ctx))

	def addPrintf(self, ctx):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Printf, self.getPosition(ctx))

	def addFormatString(self, ctx):
		includeName = "".join([str(i) for i in ctx.getChildren()])
		# Don't forget to cut the quotation marks
		self.currentPointer.addChild(ASTNodeType.FormatString, self.getPosition(ctx), includeName[1:len(includeName)-1])

	
	def climbTree(self, amt = 1):
		''' 
			Name is still a WIP :p
		'''
		for i in range(amt):
			self.currentPointer = self.currentPointer.parent


	def enterBlock(self, ctx, name):
		self.currentPointer = self.currentPointer.addChild(ASTNodeType.Block, self.getPosition(ctx))
	
	def leaveBlock(self):
		self.currentPointer = self.currentPointer.parent




	def getPosition(self, ctx):
		firstToken = self.tokenStream.get(ctx.getSourceInterval()[0])
		return (firstToken.line, firstToken.column)
