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

testdir = os.path.dirname(os.path.abspath(__file__))
resdir = os.getcwd() + "/official/res"

def func(x):
	return x + 1

def test_assignments1bis():
	# Example test, see https://docs.pytest.org/en/latest/getting-started.html#getstarted for more
	if not os.path.exists("output"):
		os.makedirs("output")


	input = FileStream(str(resdir) + "/test/assignments1bis.c")
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

		translator.saveProgram(str(testdir) + "/output/program.p")
		ASTbuilder.toDot(str(testdir) + "/output/output.dot")

	except Exception as inst:
		fail("EXCEPTION: " + str(inst))


	