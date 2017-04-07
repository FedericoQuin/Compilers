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


	def enterFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.enterBlock("FunctionBlock")

	def exitFunction(self, ctx:cGrammarParser.FunctionContext):
		self.AST.leaveBlock()


	def enterInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
		pass

	def exitInitialargument(self, ctx:cGrammarParser.InitialargumentContext):
		pass


	def enterArguments(self, ctx:cGrammarParser.ArgumentsContext):
		pass

	def exitArguments(self, ctx:cGrammarParser.ArgumentsContext):
		pass


	def enterArgument(self, ctx:cGrammarParser.ArgumentContext):
		pass

	def exitArgument(self, ctx:cGrammarParser.ArgumentContext):
		pass


	def enterFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		pass

	def exitFunction_body(self, ctx:cGrammarParser.Function_bodyContext):
		pass


	def enterStatements(self, ctx:cGrammarParser.StatementsContext):
		pass

	def exitStatements(self, ctx:cGrammarParser.StatementsContext):
		pass


	def enterStatement(self, ctx:cGrammarParser.StatementContext):
		pass

	def exitStatement(self, ctx:cGrammarParser.StatementContext):
		pass


	def enterDeclaration(self, ctx:cGrammarParser.DeclarationContext):
		self.AST.addDeclaration(ctx)

	def exitDeclaration(self, ctx:cGrammarParser.DeclarationContext):
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


	def enterRvalue(self, ctx:cGrammarParser.RvalueContext):
		self.AST.addRvalue(ctx)

	def exitRvalue(self, ctx:cGrammarParser.RvalueContext):
		self.AST.climbTree()


	def enterNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
		pass

	def exitNumericalvalue(self, ctx:cGrammarParser.NumericalvalueContext):
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


	# Enter a parse tree produced by cGrammarParser#identifier.
	def enterIdentifier(self, ctx:cGrammarParser.IdentifierContext):
		self.AST.enterID(ctx)

	# Exit a parse tree produced by cGrammarParser#identifier.
	def exitIdentifier(self, ctx:cGrammarParser.IdentifierContext):
		pass
		


	def printAST(self):
		return str(self.AST)

	def toDot(self, filename):
		dotFile = open(filename, 'w')
		dotFile.write(str(self.AST))
		dotFile.close()

	
	def getAST(self):
		return self.AST

