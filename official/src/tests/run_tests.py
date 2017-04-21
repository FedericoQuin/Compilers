# To import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

pydir = parentdir + "/py/"
sys.path.insert(0, pydir)

from antlr4 import *
from pytest import *
from cGrammarLexer import cGrammarLexer
from cGrammarParser import cGrammarParser
from ASTCreator import ASTCreator
from PTranslator import PTranslator
from filecmp import *
from AST.ASTNode import *
from MyErrorListener import MyErrorListener

testdir = os.path.dirname(os.path.abspath(__file__))
resdir = os.getcwd() + "/official/res"

def parse(inputFile, dotSolution, pSolution):

	input = FileStream(str(resdir) + "/test/" + inputFile)
	lexer = cGrammarLexer(input)
	stream = CommonTokenStream(lexer)
	parser = cGrammarParser(stream)
	parser._listeners = [MyErrorListener(str(resdir) + "/test/" + inputFile)]
	tree = parser.program()

	ASTbuilder = ASTCreator()

	try:
		walker = ParseTreeWalker()
		walker.walk(ASTbuilder, tree)

		ast = ASTbuilder.getAST()

		translator = PTranslator()
		translator.translate(ast)

		translator.saveProgram(str(testdir) + "/program.p")
		ASTbuilder.toDot(str(testdir) + "/output.dot")

	except Exception as inst:
		fail("EXCEPTION: " + str(inst))

	assert(cmp(str(testdir) + "/output.dot", str(resdir) + "/solutions/" + dotSolution))
	assert(cmp(str(testdir) + "/program.p", str(resdir) + "/solutions/" + pSolution))

def parseNoCatch(inputFile, dotSolution, pSolution):
	# For exception throwing purposes

	try:
		input = FileStream(str(resdir) + "/test/" + inputFile)
		lexer = cGrammarLexer(input)
		stream = CommonTokenStream(lexer)
		parser = cGrammarParser(stream)
		parser._listeners = [MyErrorListener(str(resdir) + "/test/" + inputFile)]
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
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("assignments1bis.c", "assignments1bis.dot", "assignments1bis.p")

def test_assignments1():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("assignments1.c", "assignments1.dot", "assignments1.p")


def test_assignments2():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("assignments2.c", "assignments2.dot", "assignments2.p")


def test_mainFunction():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("mainFunction.c", "mainFunction.dot", "mainFunction.p")


def test_mixedComments():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("mixedComments.c", "mixedComments.dot", "mixedComments.p")


def test_multiLineComment():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("multiLineComment.c", "multiLineComment.dot", "multiLineComment.p")


def test_singleLineComment():	
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("singleLineComment.c", "singleLineComment.dot", "singleLineComment.p")

def test_increment():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("increment.c", "increment.dot", "increment.p")

def test_ifelse():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("ifelse.c", "ifelse.dot", "ifelse.p")

def test_while():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("while.c", "while.dot", "while.p")

def test_for():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("for.c", "for.dot", "for.p")

def test_brackets():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("brackets.c", "brackets.dot", "brackets.p")

def test_break_continue():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("break_continue.c", "break_continue.dot", "break_continue.p")

def test_functions():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("functions.c", "functions.dot", "functions.p")

def test_pointer():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("pointer.c", "pointer.dot", "pointer.p")

def test_function_calls():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("function_calls.c", "function_calls.dot", "function_calls.p")

def test_arrays():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("arrays.c", "arrays.dot", "arrays.p")

def test_global_vars():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("global_vars.c", "global_vars.dot", "global_vars.p")

def test_includes():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("includes.c", "includes.dot", "includes.p")

def test_scanf():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("scanf.c", "scanf.dot", "scanf.p")

def test_printf():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	ASTNode.ID = 0
	parse("printf.c", "printf.dot", "printf.p")



def test_errors():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
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
			print (string)
			print(errorMessages[i])
			assert(string == errorMessages[i])