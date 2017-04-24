import os,sys,inspect


from antlr4 import *
from pytest import *
from filecmp import *

from src.cGrammarLexer import cGrammarLexer
from src.cGrammarParser import cGrammarParser

from src.py.MyErrorListener import MyErrorListener
from src.py.PTranslator import PTranslator
from src.py.AST.ASTNode import *
from src.py.AST.ASTCreator import ASTCreator
from src.py.ST.SymbolTable import SymbolTable

testdir = os.path.dirname(os.path.abspath(__file__))
resdir = os.getcwd() + "/res"

def parse(inputFile, dotSolution, pSolution, symbolTableSolution = ""):
	ASTNode.ID = 0
	SymbolTable.AllocationAddress = 0

	inputFilePath = str(resdir) + "/happyDayTests/" + inputFile
	input = FileStream(inputFilePath)

	lexer = cGrammarLexer(input)
	stream = CommonTokenStream(lexer)
	parser = cGrammarParser(stream)
	parser._listeners = [MyErrorListener(inputFilePath)]
	tree = parser.program()

	ASTbuilder = ASTCreator()

	pResultPath = str(testdir) + "/program.p"
	dotResultPath = str(testdir) + "/output.dot"
	stResultPath = str(testdir) + "/symbolTable.txt"

	pSolutionsPath = str(resdir) + "/solutions/" + pSolution
	dotSolutionsPath = str(resdir) + "/solutions/" + dotSolution
	stSolutionsPath = str(resdir) + "/solutions/" + symbolTableSolution


	try:
		walker = ParseTreeWalker()
		walker.walk(ASTbuilder, tree)

		ast = ASTbuilder.getAST()

		translator = PTranslator()
		translator.translate(ast, stResultPath)

		translator.saveProgram(pResultPath)
		ASTbuilder.toDot(dotResultPath)

	except Exception as inst:
		fail("Failure for " + str(inputFile) + "\n" + str(inst))
	
	assert(cmp(dotResultPath, dotSolutionsPath))
	assert(cmp(pResultPath, pSolutionsPath))
	# assert(cmp(stResultPath, stSolutionsPath))

def parseNoCatch(inputFile, dotSolution, pSolution):
	# For exception throwing purposes

	try:
		input = FileStream(str(resdir) + "/deathTests/" + inputFile)
		lexer = cGrammarLexer(input)
		stream = CommonTokenStream(lexer)
		parser = cGrammarParser(stream)
		parser._listeners = [MyErrorListener(str(resdir) + "/deathTests/" + inputFile)]
		tree = parser.program()

		ASTbuilder = ASTCreator()

		walker = ParseTreeWalker()
		walker.walk(ASTbuilder, tree)

		ast = ASTbuilder.getAST()

		translator = PTranslator()
		translator.translate(ast)

		translator.saveProgram(str(testdir) + "/program.p")
		ASTbuilder.toDot(str(testdir) + "/output.dot")
	except Exception as inst:
		raise inst

	assert(False)


def test_assignments1bis():
	parse("assignments1bis.c", "assignments1bis.dot", "assignments1bis.p", "assignments1bis.symboltable")

def test_assignments1():
	parse("assignments1.c", "assignments1.dot", "assignments1.p", "assignments1.symboltable")


def test_assignments2():
	parse("assignments2.c", "assignments2.dot", "assignments2.p", "assignments2.symboltable")


def test_mainFunction():
	parse("mainFunction.c", "mainFunction.dot", "mainFunction.p", "mainFunction.symboltable")


def test_mixedComments():	
	parse("mixedComments.c", "mixedComments.dot", "mixedComments.p", "mixedComments.symboltable")


def test_multiLineComment():	
	parse("multiLineComment.c", "multiLineComment.dot", "multiLineComment.p", "multiLineComment.symboltable")


def test_singleLineComment():	
	parse("singleLineComment.c", "singleLineComment.dot", "singleLineComment.p", "singleLineComment.symboltable")

def test_increment():
	parse("increment.c", "increment.dot", "increment.p", "increment.symboltable")

def test_ifelse():
	parse("ifelse.c", "ifelse.dot", "ifelse.p", "ifelse.symboltable")

def test_while():
	parse("while.c", "while.dot", "while.p", "while.symboltable")

def test_for():
	parse("for.c", "for.dot", "for.p", "for.symboltable")

def test_brackets():
	parse("brackets.c", "brackets.dot", "brackets.p", "brackets.symboltable")

def test_break_continue():
	parse("break_continue.c", "break_continue.dot", "break_continue.p", "break_continue.symboltable")

def test_functions():
	parse("functions.c", "functions.dot", "functions.p", "functions.symboltable")

def test_pointer():
	parse("pointer.c", "pointer.dot", "pointer.p", "pointer.symboltable")

def test_function_calls():
	parse("function_calls.c", "function_calls.dot", "function_calls.p", "function_calls.symboltable")

def test_arrays():
	parse("arrays.c", "arrays.dot", "arrays.p", "arrays.symboltable")

def test_global_vars():
	parse("global_vars.c", "global_vars.dot", "global_vars.p", "global_vars.symboltable")

def test_includes():
	parse("includes.c", "includes.dot", "includes.p", "includes.symboltable")

def test_scanf():
	parse("scanf.c", "scanf.dot", "scanf.p", "scanf.symboltable")

def test_printf():
	parse("printf.c", "printf.dot", "printf.p", "printf.symboltable")



def test_errors():
	errorFiles = [
		"error_braces1.c",
		"error_braces2.c",
		# "error_braces3.c"			// TODO
		# "error_no_semicolon.c"	// TODO improve current error
		# "error_rubbish.c",		// TODO
		# "error_ifelse.c",		// TODO
		# "error_for.c",		// TODO
		# "error_while.c"		// TODO
		]
	errorMessages = [
		"3:0: Error while/after parsing statement\n\n^\nBraces don't match",
		"2:36: Error while/after parsing expression\n\tint someDecl = (5 + 8) * 3 * (5 + 4;\n\t                                   ^\nBraces don't match",
		"",
		"",
		"",
		"",
		"",
		""
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])

def test_types():
	# Tests the typechecker
	errorFiles = [
		"type_check1.c",
		"type_check2.c",
		"type_check3.c",
		"type_check4.c",
		"type_check5.c",
		"type_check6.c",
		"type_check7.c",
		"type_check8.c",
		"type_check9.c",
		"type_check10.c"
		]
	errorMessages = [
		"Types for assignment don't match: char and int.",
		"Types for assignment don't match: float and int.",
		"Types do not match: int and float.",
		"Types for comparison don't match: int and float.",
		"Function arguments invalid: 'getCookies' takes 0 arguments (1 argument given).",
		"Function arguments invalid: 'somethingElse' takes 3 arguments (4 arguments given).",
		"Argument for function call 'wrongTypes' did not match the signature: int and char (argument #2).",
		"Argument for function call 'someFunction' did not match the signature: char and int (argument #1).",
		"Argument for function call 'thatOtherFunction' did not match the signature: float and int (argument #2).",
		"Types for assignment don't match: int and void."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])