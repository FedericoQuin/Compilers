# To import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from cGrammarListener import cGrammarListener
from cGrammarParser import *
from AST.AST import AST

class ASTCreator(cGrammarListener):
	def __init__(self):
		self.AST = None

	def enterProgram(self, ctx:cGrammarParser.ProgramContext):
		self.AST = AST()

	def exitProgram(self, ctx:cGrammarParser.ProgramContext):
		pass

	def enterStatements(self, ctx:cGrammarParser.StatementsContext):
		pass

	def exitStatements(self, ctx:cGrammarParser.StatementsContext):
		pass


	def enterStatement(self, ctx:cGrammarParser.StatementContext):
		pass

	def exitStatement(self, ctx:cGrammarParser.StatementContext):
		pass


	#################################################
	# Includes										#
	#################################################

	def enterInclude_file(self, ctx:cGrammarParser.Include_fileContext):
		self.AST.addInclude(ctx)

	def exitInclude_file(self, ctx:cGrammarParser.Include_fileContext):
		pass



	#################################################
	# Declarations									#
	#################################################

	def enterNormal_declaration(self, ctx:cGrammarParser.Normal_declarationContext):
		self.AST.addNormalDeclaration(ctx)

	def exitNormal_declaration(self, ctx:cGrammarParser.Normal_declarationContext):
		pass


	def enterArray_declaration(self, ctx:cGrammarParser.Array_declarationContext):
		self.AST.addArrayDeclaration(ctx)

	def exitArray_declaration(self, ctx:cGrammarParser.Array_declarationContext):
		pass




	#################################################
	# Array element access							#
	#################################################

	def enterArrayelement_lvalue(self, ctx:cGrammarParser.Arrayelement_lvalueContext):
		self.AST.addArrayElement(ctx, "lvalue")

	def exitArrayelement_lvalue(self, ctx:cGrammarParser.Arrayelement_lvalueContext):
		pass
	
	def enterArrayelement_rvalue(self, ctx:cGrammarParser.Arrayelement_rvalueContext):
		self.AST.addArrayElement(ctx, "rvalue")

	def exitArrayelement_rvalue(self, ctx:cGrammarParser.Arrayelement_rvalueContext):
		pass


	

	def enterReturntype(self, ctx:cGrammarParser.ReturntypeContext):
		pass

	def exitReturntype(self, ctx:cGrammarParser.ReturntypeContext):
		pass


	def enterAssignment(self, ctx:cGrammarParser.AssignmentContext):
		self.AST.addAssignment(ctx)

	def exitAssignment(self, ctx:cGrammarParser.AssignmentContext):
		self.AST.climbTree()


	def enterLvalue(self, ctx:cGrammarParser.LvalueContext):
		pass

	def exitLvalue(self, ctx:cGrammarParser.LvalueContext):
		pass





	def enterIntvalue(self, ctx:cGrammarParser.IntvalueContext):
		self.AST.setIntValueNode(ctx)

	def exitIntvalue(self, ctx:cGrammarParser.IntvalueContext):
		pass


	def enterFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
		self.AST.setFloatValueNode(ctx)

	def exitFloatvalue(self, ctx:cGrammarParser.FloatvalueContext):
		pass


	def enterDigits(self, ctx:cGrammarParser.DigitsContext):
		pass

	def exitDigits(self, ctx:cGrammarParser.DigitsContext):
		pass

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



	#################################################
	# Operator stuff								#
	#################################################
	def enterExpression(self, ctx:cGrammarParser.ExpressionContext):
		self.AST.enterExpression(ctx)

	# Exit a parse tree produced by cGrammarParser#expression.
	def exitExpression(self, ctx:cGrammarParser.ExpressionContext):
		if ctx.OPERATOR_AS() != None:
			self.AST.climbTree()



	# Enter a parse tree produced by cGrammarParser#add_sub.
	def enterAdd_sub(self, ctx:cGrammarParser.Add_subContext):
		self.AST.enterAddSub(ctx)

	# Exit a parse tree produced by cGrammarParser#add_sub.
	def exitAdd_sub(self, ctx:cGrammarParser.Add_subContext):
		if ctx.OPERATOR_PLUS() != None or ctx.OPERATOR_MINUS() != None:
			self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#mul_div.
	def enterMul_div(self, ctx:cGrammarParser.Mul_divContext):
		self.AST.enterMulDiv(ctx)

	# Exit a parse tree produced by cGrammarParser#mul_div.
	def exitMul_div(self, ctx:cGrammarParser.Mul_divContext):
		if ctx.OPERATOR_MUL() != None or ctx.OPERATOR_DIV() != None:
			self.AST.climbTree()

	# Enter a parse tree produced by cGrammarParser#bracket_expression.
	def enterBracket_expression(self, ctx:cGrammarParser.Bracket_expressionContext):
		self.AST.makeBrackets(ctx)

	# Exit a parse tree produced by cGrammarParser#bracket_expression.
	def exitBracket_expression(self, ctx:cGrammarParser.Bracket_expressionContext):
		self.AST.climbTree()



	# Enter a parse tree produced by cGrammarParser#identifier.
	def enterLvalue_identifier(self, ctx:cGrammarParser.Lvalue_identifierContext):
		self.AST.enterID(ctx, "lvalue")

	# Exit a parse tree produced by cGrammarParser#identifier.
	def exitLvalue_identifier(self, ctx:cGrammarParser.Lvalue_identifierContext):
		pass

	def enterRvalue_identifier(self, ctx:cGrammarParser.Rvalue_identifierContext):
		self.AST.enterID(ctx, "rvalue")

	def exitRvalue_identifier(self, ctx:cGrammarParser.Rvalue_identifierContext):
		pass


	#################################################
	# Ifelse stuff									#
	#################################################
	def enterIfelse(self, ctx:cGrammarParser.IfelseContext):
		self.AST.addIfElse(ctx)

	# Exit a parse tree produced by cGrammarParser#ifelse.
	def exitIfelse(self, ctx:cGrammarParser.IfelseContext):
		# twice because you have to return from the self-made node but also from the IfTrue-IfFalse nodes
		# because one of them has to jump back as well, but they can't know whether the other one already jumped back or not
		self.AST.climbTree()
		self.AST.climbTree()

	# Enter a parse tree produced by cGrammarParser#firstcondition.
	def enterFirstcondition(self, ctx:cGrammarParser.FirstconditionContext):
		self.AST.enterFirstcondition(ctx)

	# Exit a parse tree produced by cGrammarParser#firstcondition.
	def exitFirstcondition(self, ctx:cGrammarParser.FirstconditionContext):
		pass

	# Enter a parse tree produced by cGrammarParser#first_true_statements.
	def enterFirst_true_statements(self, ctx:cGrammarParser.First_true_statementsContext):
		self.AST.enterFirst_true_statements(ctx)

	# Exit a parse tree produced by cGrammarParser#first_true_statements.
	def exitFirst_true_statements(self, ctx:cGrammarParser.First_true_statementsContext):
		pass


	# Enter a parse tree produced by cGrammarParser#first_true_statement.
	def enterFirst_true_statement(self, ctx:cGrammarParser.First_true_statementContext):
		self.AST.enterFirst_true_statement(ctx)

	# Exit a parse tree produced by cGrammarParser#first_true_statement.
	def exitFirst_true_statement(self, ctx:cGrammarParser.First_true_statementContext):
		pass


	# Enter a parse tree produced by cGrammarParser#first_false_statement.
	def enterFirst_false_statement(self, ctx:cGrammarParser.First_false_statementContext):
		self.AST.enterFirst_false_statement(ctx)

	# Exit a parse tree produced by cGrammarParser#first_false_statement.
	def exitFirst_false_statement(self, ctx:cGrammarParser.First_false_statementContext):
		pass


	# Enter a parse tree produced by cGrammarParser#first_false_statements.
	def enterFirst_false_statements(self, ctx:cGrammarParser.First_false_statementsContext):
		self.AST.enterFirst_false_statements(ctx)

	# Exit a parse tree produced by cGrammarParser#first_false_statements.
	def exitFirst_false_statements(self, ctx:cGrammarParser.First_false_statementsContext):
		pass

	# Enter a parse tree produced by cGrammarParser#else_statement.
	def enterElse_statement(self, ctx:cGrammarParser.Else_statementContext):
		pass

	# Exit a parse tree produced by cGrammarParser#else_statement.
	def exitElse_statement(self, ctx:cGrammarParser.Else_statementContext):
		pass



	#################################################
	# Condition stuff								#
	#################################################
	# Enter a parse tree produced by cGrammarParser#condition.
	def enterCondition(self, ctx:cGrammarParser.ConditionContext):
		self.AST.enterCondition(ctx)

	# Exit a parse tree produced by cGrammarParser#condition.
	def exitCondition(self, ctx:cGrammarParser.ConditionContext):
		self.AST.exitCondition(ctx)


	# Enter a parse tree produced by cGrammarParser#condition_and.
	def enterCondition_and(self, ctx:cGrammarParser.Condition_andContext):
		self.AST.enterCondition_and(ctx)

	# Exit a parse tree produced by cGrammarParser#condition_and.
	def exitCondition_and(self, ctx:cGrammarParser.Condition_andContext):
		self.AST.exitCondition_and(ctx)


	# Enter a parse tree produced by cGrammarParser#condition_not.
	def enterCondition_not(self, ctx:cGrammarParser.Condition_notContext):
		self.AST.enterCondition_not(ctx)

	# Exit a parse tree produced by cGrammarParser#condition_not.
	def exitCondition_not(self, ctx:cGrammarParser.Condition_notContext):
		self.AST.exitCondition_not(ctx)


	# Enter a parse tree produced by cGrammarParser#comparison.
	def enterComparison(self, ctx:cGrammarParser.ComparisonContext):
		self.AST.enterComparison(ctx)


	# Exit a parse tree produced by cGrammarParser#comparison.
	def exitComparison(self, ctx:cGrammarParser.ComparisonContext):
		self.AST.exitComparison(ctx)

	# Enter a parse tree produced by cGrammarParser#bracket_condition.
	def enterBracket_condition(self, ctx:cGrammarParser.Bracket_conditionContext):
		if ctx.OPERATOR_NOT() != None:
			self.AST.makeBrackets(ctx, True)
		else:
			self.AST.makeBrackets(ctx, False)

	# Exit a parse tree produced by cGrammarParser#bracket_condition.
	def exitBracket_condition(self, ctx:cGrammarParser.Bracket_conditionContext):
		self.AST.climbTree()



	#################################################
	# While stuff									#
	#################################################
	# Enter a parse tree produced by cGrammarParser#while_loop.
	def enterWhile_loop(self, ctx:cGrammarParser.While_loopContext):
		self.AST.enterWhile_loop(ctx)

	# Exit a parse tree produced by cGrammarParser#while_loop.
	def exitWhile_loop(self, ctx:cGrammarParser.While_loopContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#first_while_statements.
	def enterFirst_while_statements(self, ctx:cGrammarParser.First_while_statementsContext):
		self.AST.enterFirst_while_statements(ctx)

	# Exit a parse tree produced by cGrammarParser#first_while_statements.
	def exitFirst_while_statements(self, ctx:cGrammarParser.First_while_statementsContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#first_while_statement.
	def enterFirst_while_statement(self, ctx:cGrammarParser.First_while_statementContext):
		self.AST.enterFirst_while_statement(ctx)

	# Exit a parse tree produced by cGrammarParser#first_while_statement.
	def exitFirst_while_statement(self, ctx:cGrammarParser.First_while_statementContext):
		self.AST.climbTree()

	# Enter a parse tree produced by cGrammarParser#first_while_condition.
	def enterFirst_while_condition(self, ctx:cGrammarParser.First_while_conditionContext):
		self.AST.enterFirst_while_condition(ctx)

	# Exit a parse tree produced by cGrammarParser#first_while_condition.
	def exitFirst_while_condition(self, ctx:cGrammarParser.First_while_conditionContext):
		self.AST.climbTree()

	# Enter a parse tree produced by cGrammarParser#break_stmt.
	def enterBreak_stmt(self, ctx:cGrammarParser.Break_stmtContext):
		self.AST.enterBreak_stmt(ctx)

	# Exit a parse tree produced by cGrammarParser#break_stmt.
	def exitBreak_stmt(self, ctx:cGrammarParser.Break_stmtContext):
		pass
	
	# Enter a parse tree produced by cGrammarParser#continue_stmt.
	def enterContinue_stmt(self, ctx:cGrammarParser.Continue_stmtContext):
		self.AST.enterContinue_stmt(ctx)

	# Exit a parse tree produced by cGrammarParser#continue_stmt.
	def exitContinue_stmt(self, ctx:cGrammarParser.Continue_stmtContext):
		pass

	# Enter a parse tree produced by cGrammarParser#return_stmt.
	def enterReturn_stmt(self, ctx:cGrammarParser.Return_stmtContext):
		self.AST.returnStmt(ctx)


	#################################################
	# For stuff										#
	#################################################
	# Enter a parse tree produced by cGrammarParser#for_loop.
	def enterFor_loop(self, ctx:cGrammarParser.For_loopContext):
		self.AST.enterFor_loop(ctx)

	# Exit a parse tree produced by cGrammarParser#for_loop.
	def exitFor_loop(self, ctx:cGrammarParser.For_loopContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#first_for_statements.
	def enterFirst_for_statements(self, ctx:cGrammarParser.First_for_statementsContext):
		self.AST.enterFirst_for_statements(ctx)

	# Exit a parse tree produced by cGrammarParser#first_for_statements.
	def exitFirst_for_statements(self, ctx:cGrammarParser.First_for_statementsContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#first_for_statement.
	def enterFirst_for_statement(self, ctx:cGrammarParser.First_for_statementContext):
		self.AST.enterFirst_for_statement(ctx)

	# Exit a parse tree produced by cGrammarParser#first_for_statement.
	def exitFirst_for_statement(self, ctx:cGrammarParser.First_for_statementContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#first_stmt_for.
	def enterFirst_stmt_for(self, ctx:cGrammarParser.First_stmt_forContext):
		self.AST.enterFirst_stmt_for(ctx)

	# Exit a parse tree produced by cGrammarParser#first_stmt_for.
	def exitFirst_stmt_for(self, ctx:cGrammarParser.First_stmt_forContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#second_stmt_for.
	def enterSecond_stmt_for(self, ctx:cGrammarParser.Second_stmt_forContext):
		self.AST.enterSecond_stmt_for(ctx)

	# Exit a parse tree produced by cGrammarParser#second_stmt_for.
	def exitSecond_stmt_for(self, ctx:cGrammarParser.Second_stmt_forContext):
		self.AST.climbTree()


	# Enter a parse tree produced by cGrammarParser#third_stmt_for.
	def enterThird_stmt_for(self, ctx:cGrammarParser.Third_stmt_forContext):
		self.AST.enterThird_stmt_for(ctx)

	# Exit a parse tree produced by cGrammarParser#third_stmt_for.
	def exitThird_stmt_for(self, ctx:cGrammarParser.Third_stmt_forContext):
		self.AST.climbTree()



	#################################################
	# Function stuff								#
	#################################################
	# Enter a parse tree produced by cGrammarParser#functiondecl.
	def enterFunctiondecl(self, ctx:cGrammarParser.FunctiondeclContext):
		self.AST.enterFunctiondecl(ctx)

	# Exit a parse tree produced by cGrammarParser#functiondecl.
	def exitFunctiondecl(self, ctx:cGrammarParser.FunctiondeclContext):
		self.AST.climbTree()
		
	# Enter a parse tree produced by cGrammarParser#initialargument.
	def enterInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
		self.AST.addArgumentList(ctx)

	# Exit a parse tree produced by cGrammarParser#initialargument.
	def exitInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
		self.AST.climbTree()

	# Enter a parse tree produced by cGrammarParser#argument.
	def enterArgument(self, ctx:cGrammarParser.ArgumentContext):
		self.AST.addArgument(ctx)

	def enterFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		self.AST.addFunctionBody(ctx)

	def exitFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		self.AST.climbTree()

	def enterFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.enterFunctiondecl(ctx)

	def exitFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.climbTree()





	def printAST(self):
		return str(self.AST)

	def toDot(self, filename):
		dotFile = open(filename, 'w')
		dotFile.write(str(self.AST))
		dotFile.close()

	
	def getAST(self):
		return self.AST

