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

testdir = os.path.dirname(os.path.abspath(__file__))
resdir = os.getcwd() + "/official/res"

def parse(inputFile, dotSolution, pSolution):

	input = FileStream(str(resdir) + "/test/" + inputFile)
	lexer = cGrammarLexer(input)
	stream = CommonTokenStream(lexer)
	parser = cGrammarParser(stream)
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