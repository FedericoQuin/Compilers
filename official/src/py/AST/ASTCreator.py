
from src.cGrammarListener import cGrammarListener
from src.cGrammarParser import *
from src.py.AST.AST import AST

class ASTCreator(cGrammarListener):
	def __init__(self, stream):
		self.AST = None
		self.tokenStream = stream

	def enterProgram(self, ctx:cGrammarParser.ProgramContext):
		self.AST = AST(self.tokenStream)


	#################################################
	# Includes										#
	#################################################

	def enterInclude_file(self, ctx:cGrammarParser.Include_fileContext):
		self.AST.addInclude(ctx)


	#################################################
	# Declarations									#
	#################################################

	def enterNormal_declaration(self, ctx:cGrammarParser.Normal_declarationContext):
		self.AST.addNormalDeclaration(ctx)

	def exitNormal_declaration(self, ctx:cGrammarParser.Normal_declarationContext):
		self.AST.climbTree()

	def enterArray_declaration(self, ctx:cGrammarParser.Array_declarationContext):
		self.AST.addArrayDeclaration(ctx)

	def exitArray_declaration(self, ctx:cGrammarParser.Array_declarationContext):
		self.AST.climbTree()


	def enterInitialization(self, ctx:cGrammarParser.InitializationContext):
		self.AST.addInitialization(ctx)

	def exitInitialization(self, ctx:cGrammarParser.InitializationContext):
		self.AST.climbTree()
	



	#################################################
	# Array element access							#
	#################################################

	def enterArrayelement_lvalue(self, ctx:cGrammarParser.Arrayelement_lvalueContext):
		self.AST.addArrayElement(ctx, "lvalue")

	def exitArrayelement_lvalue(self, ctx:cGrammarParser.Arrayelement_lvalueContext):
		self.AST.climbTree()

	
	def enterArrayelement_rvalue(self, ctx:cGrammarParser.Arrayelement_rvalueContext):
		self.AST.addArrayElement(ctx, "rvalue")

	def exitArrayelement_rvalue(self, ctx:cGrammarParser.Arrayelement_rvalueContext):
		self.AST.climbTree()


	


	def enterAssignment(self, ctx:cGrammarParser.AssignmentContext):
		self.AST.addAssignment(ctx)

	def exitAssignment(self, ctx:cGrammarParser.AssignmentContext):
		self.AST.climbTree()



	def enterIntvalue(self, ctx:cGrammarParser.IntvalueContext):
		self.AST.setIntValueNode(ctx)



	def enterFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
		self.AST.setFloatValueNode(ctx)



	#################################################
	# RValue handling								#
	#################################################

	# Numerical values (int, float or pointer types)
	def enterNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
		self.AST.addNumericalValue(ctx)

	def exitNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
		self.AST.climbTree()


	# Char values
	def enterCharvalue(self, ctx:cGrammarParser.CharvalueContext):
		self.AST.addCharValue(ctx)

	def exitCharvalue(self, ctx:cGrammarParser.CharvalueContext):
		# no need to climb here, the new node doesn't need to be adjusted further
		pass


	# Function calls
	def enterFunctioncall(self, ctx:cGrammarParser.FunctioncallContext):
		self.AST.addFunctionCall(ctx)

	def exitFunctioncall(self, ctx:cGrammarParser.FunctioncallContext):
		self.AST.climbTree()

	def enterRvalue(self, ctx):
		if ctx.OPERATOR_MINUS() != None:
			self.AST.addNegate(ctx)

	def exitRvalue(self, ctx):
		if ctx.OPERATOR_MINUS() != None:
			self.AST.climbTree()

	def enterTrue(self, ctx):
		self.AST.addTrue(ctx)

	def exitTrue(self, ctx):
		self.AST.climbTree()

	def enterFalse(self, ctx):
		self.AST.addFalse(ctx)

	def exitFalse(self, ctx):
		self.AST.climbTree()


	# TODO were these really necessary?
	# def enterLvalue_brackets(self, ctx:cGrammarParser.Lvalue_bracketsContext):
	# 	self.AST.makeBrackets(ctx)

	# def exitLvalue_brackets(self, ctx:cGrammarParser.Lvalue_bracketsContext):
	# 	self.AST.climbTree()



	#################################################
	# Operator stuff								#
	#################################################


	def enterMinus_expr(self, ctx):
		if ctx.OPERATOR_MINUS() != None:
			self.AST.addNegate(ctx)
		
	def exitMinus_expr(self, ctx):
		if ctx.OPERATOR_MINUS() != None:
			self.AST.climbTree()

	def enterDereference_expr(self, ctx):
		if len(ctx.OPERATOR_MUL()) != 0:
			self.AST.addDereference(ctx)

	def exitDereference_expr(self, ctx):
		if len(ctx.OPERATOR_MUL()) != 0:
			self.AST.climbTree()

	def enterAssigment(self, ctx):
		self.AST.enterAssignment(ctx)

	def exitAssignment(self, ctx):
		self.AST.climbTree()


	def enterAdd_sub(self, ctx:cGrammarParser.Add_subContext):
		self.AST.enterAddSub(ctx)

	def exitAdd_sub(self, ctx:cGrammarParser.Add_subContext):
		if ctx.OPERATOR_PLUS() != None or ctx.OPERATOR_MINUS() != None:
			self.AST.climbTree()


	def enterMul_div(self, ctx:cGrammarParser.Mul_divContext):
		self.AST.enterMulDiv(ctx)

	def exitMul_div(self, ctx:cGrammarParser.Mul_divContext):
		if ctx.OPERATOR_MUL() != None or ctx.OPERATOR_DIV() != None:
			self.AST.climbTree()

	def enterBracket_expression(self, ctx:cGrammarParser.Bracket_expressionContext):
		if ctx.LBRACKET() != None:
			self.AST.makeBrackets(ctx)

	def exitBracket_expression(self, ctx:cGrammarParser.Bracket_expressionContext):
		if ctx.LBRACKET() != None:
			self.AST.climbTree()



	def enterLvalue_identifier(self, ctx:cGrammarParser.Lvalue_identifierContext):
		self.AST.enterID(ctx, "lvalue")

	def enterRvalue_identifier(self, ctx:cGrammarParser.Rvalue_identifierContext):
		self.AST.enterID(ctx, "rvalue")



	#################################################
	# Ifelse stuff									#
	#################################################

	def enterIfelse(self, ctx:cGrammarParser.IfelseContext):
		self.AST.addIfElse(ctx)

	def exitIfelse(self, ctx:cGrammarParser.IfelseContext):
		# twice because you have to return from the self-made node but also from the IfTrue-IfFalse nodes
		# because one of them has to jump back as well, but they can't know whether the other one already jumped back or not
		self.AST.climbTree(2)

	def enterFirstcondition(self, ctx:cGrammarParser.FirstconditionContext):
		self.AST.enterFirstcondition(ctx)

	def enterFirst_true_statements(self, ctx:cGrammarParser.First_true_statementsContext):
		self.AST.enterFirst_true_statements(ctx)



	def enterFirst_true_statement(self, ctx:cGrammarParser.First_true_statementContext):
		self.AST.enterFirst_true_statement(ctx)


	def enterFirst_false_statement(self, ctx:cGrammarParser.First_false_statementContext):
		self.AST.enterFirst_false_statement(ctx)


	def enterFirst_false_statements(self, ctx:cGrammarParser.First_false_statementsContext):
		self.AST.enterFirst_false_statements(ctx)




	#################################################
	# Condition stuff								#
	#################################################

	def enterCondition(self, ctx:cGrammarParser.ConditionContext):
		self.AST.enterCondition(ctx)

	def exitCondition(self, ctx:cGrammarParser.ConditionContext):
		self.AST.exitCondition(ctx)


	def enterCondition_and(self, ctx:cGrammarParser.Condition_andContext):
		self.AST.enterCondition_and(ctx)

	def exitCondition_and(self, ctx:cGrammarParser.Condition_andContext):
		self.AST.exitCondition_and(ctx)


	def enterCondition_not(self, ctx:cGrammarParser.Condition_notContext):
		self.AST.enterCondition_not(ctx)

	def exitCondition_not(self, ctx:cGrammarParser.Condition_notContext):
		self.AST.exitCondition_not(ctx)


	def enterComparison(self, ctx:cGrammarParser.ComparisonContext):
		self.AST.enterComparison(ctx)


	def exitComparison(self, ctx:cGrammarParser.ComparisonContext):
		self.AST.exitComparison(ctx)

	def enterBracket_condition(self, ctx:cGrammarParser.Bracket_conditionContext):
		if ctx.OPERATOR_NOT() != None:
			self.AST.makeBrackets(ctx, True)
		else:
			self.AST.makeBrackets(ctx, False)

	def exitBracket_condition(self, ctx:cGrammarParser.Bracket_conditionContext):
		self.AST.climbTree()



	#################################################
	# While stuff									#
	#################################################

	def enterWhile_loop(self, ctx:cGrammarParser.While_loopContext):
		self.AST.enterWhile_loop(ctx)

	def exitWhile_loop(self, ctx:cGrammarParser.While_loopContext):
		self.AST.climbTree()


	def enterFirst_while_statements(self, ctx:cGrammarParser.First_while_statementsContext):
		self.AST.enterFirst_while_statements(ctx)

	def exitFirst_while_statements(self, ctx:cGrammarParser.First_while_statementsContext):
		self.AST.climbTree()


	def enterFirst_while_statement(self, ctx:cGrammarParser.First_while_statementContext):
		self.AST.enterFirst_while_statement(ctx)

	def exitFirst_while_statement(self, ctx:cGrammarParser.First_while_statementContext):
		self.AST.climbTree()

	def enterFirst_while_condition(self, ctx:cGrammarParser.First_while_conditionContext):
		self.AST.enterFirst_while_condition(ctx)

	def exitFirst_while_condition(self, ctx:cGrammarParser.First_while_conditionContext):
		self.AST.climbTree()

	def enterBreak_stmt(self, ctx:cGrammarParser.Break_stmtContext):
		self.AST.enterBreak_stmt(ctx)

	def enterContinue_stmt(self, ctx:cGrammarParser.Continue_stmtContext):
		self.AST.enterContinue_stmt(ctx)

	def enterReturn_stmt(self, ctx:cGrammarParser.Return_stmtContext):
		self.AST.returnStmt(ctx)

	def exitReturn_stmt(self, ctx:cGrammarParser.Return_stmtContext):
		self.AST.climbTree()


	#################################################
	# For stuff										#
	#################################################

	def enterFor_loop(self, ctx:cGrammarParser.For_loopContext):
		self.AST.enterFor_loop(ctx)

	def exitFor_loop(self, ctx:cGrammarParser.For_loopContext):
		self.AST.climbTree()


	def enterFirst_for_statements(self, ctx:cGrammarParser.First_for_statementsContext):
		self.AST.enterFirst_for_statements(ctx)

	def exitFirst_for_statements(self, ctx:cGrammarParser.First_for_statementsContext):
		self.AST.climbTree()


	def enterFirst_for_statement(self, ctx:cGrammarParser.First_for_statementContext):
		self.AST.enterFirst_for_statement(ctx)

	def exitFirst_for_statement(self, ctx:cGrammarParser.First_for_statementContext):
		self.AST.climbTree()


	def enterFirst_stmt_for(self, ctx:cGrammarParser.First_stmt_forContext):
		self.AST.enterFirst_stmt_for(ctx)

	def exitFirst_stmt_for(self, ctx:cGrammarParser.First_stmt_forContext):
		self.AST.climbTree()


	def enterSecond_stmt_for(self, ctx:cGrammarParser.Second_stmt_forContext):
		self.AST.enterSecond_stmt_for(ctx)

	def exitSecond_stmt_for(self, ctx:cGrammarParser.Second_stmt_forContext):
		self.AST.climbTree()


	def enterThird_stmt_for(self, ctx:cGrammarParser.Third_stmt_forContext):
		self.AST.enterThird_stmt_for(ctx)

	def exitThird_stmt_for(self, ctx:cGrammarParser.Third_stmt_forContext):
		self.AST.climbTree()



	#################################################
	# Function stuff								#
	#################################################

	def enterFunctiondecl(self, ctx:cGrammarParser.FunctiondeclContext):
		self.AST.enterFunctiondecl(ctx, "FunctionDecl")

	def exitFunctiondecl(self, ctx:cGrammarParser.FunctiondeclContext):
		self.AST.climbTree()

	def enterInitialfunctionargument(self, ctx:cGrammarParser.InitialfunctionargumentContext):
		self.AST.addFunctionArgumentList(ctx)

	def exitInitialfunctionargument(self, ctx:cGrammarParser.InitialfunctionargumentContext):
		self.AST.climbTree()

	def enterType_argument(self, ctx:cGrammarParser.Type_argumentContext):
		self.AST.addArgument(ctx)

	def enterFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		self.AST.addFunctionBody(ctx)

	def exitFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		self.AST.climbTree()

	def enterFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.enterFunctiondecl(ctx, "Function")

	def exitFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.climbTree()



	#################################################
	# Pointers and addresses						#
	#################################################


	def enterAddress_value(self, ctx:cGrammarParser.Address_valueContext):
		self.AST.addAddressOf(ctx)

	def exitAddress_value(self, ctx:cGrammarParser.Address_valueContext):
		self.AST.climbTree()

	def enterPointer_dereference(self, ctx:cGrammarParser.Pointer_dereferenceContext):
		# Don't add a node if this one is just adding brackets
		if len(ctx.OPERATOR_MUL()) != 0:
			self.AST.addDereference(ctx)

	def exitPointer_dereference(self, ctx:cGrammarParser.Pointer_dereferenceContext):
		if len(ctx.OPERATOR_MUL()) != 0:
			self.AST.climbTree()






	#################################################
	# Scanf and Printf								#
	#################################################

	def enterScanf(self, ctx:cGrammarParser.ScanfContext):
		self.AST.addScanf(ctx)

	def exitScanf(self, ctx:cGrammarParser.ScanfContext):
		self.AST.climbTree()


	def enterPrintf(self, ctx:cGrammarParser.PrintfContext):
		self.AST.addPrintf(ctx)

	def exitPrintf(self, ctx:cGrammarParser.PrintfContext):
		self.AST.climbTree()


	def enterFormat_string(self, ctx:cGrammarParser.Format_stringContext):
		self.AST.addFormatString(ctx)





	def printAST(self):
		return str(self.AST)

	def toDot(self, filename):
		dotFile = open(filename, 'w')
		dotFile.write(str(self.AST))
		dotFile.close()

	
	def getAST(self):
		return self.AST

