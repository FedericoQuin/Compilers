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
from src.py.SA.ErrorMsgHandler import ExType, determineExPrefix

testdir = os.path.dirname(os.path.abspath(__file__))
resdir = os.getcwd() + "/res"

def parse(inputFile, dotSolution, pSolution, symbolTableSolution = "", translate=True):
	ASTNode.ID = 0
	SymbolTable.AllocationAddress = 0

	inputFilePath = str(resdir) + "/happyDayTests/" + inputFile
	input = FileStream(inputFilePath)

	lexer = cGrammarLexer(input)
	stream = CommonTokenStream(lexer)
	parser = cGrammarParser(stream)
	parser._listeners = [MyErrorListener(inputFilePath)]
	tree = parser.program()

	ASTbuilder = ASTCreator(stream)

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
		translator.translate(ast, stResultPath, translate=translate)

		translator.saveProgram(pResultPath)
		ASTbuilder.toDot(dotResultPath)

	except Exception as inst:
		fail("Failure for " + str(inputFile) + "\n" + str(inst))
	
	assert(cmp(dotResultPath, dotSolutionsPath))
	if translate:
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

		ASTbuilder = ASTCreator(stream)

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
	parse("increment.c", "increment.dot", "increment.p", "increment.symboltable", translate=False)

def test_prefixIncDec():
	parse("prefixIncDec.c", "prefixIncDec.dot", "prefixIncDec.p", "prefixIncDec.symboltable", translate=False)

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
	parse("pointer.c", "pointer.dot", "pointer.p", "pointer.symboltable", translate=False)

def test_function_calls():
	parse("function_calls.c", "function_calls.dot", "function_calls.p", "function_calls.symboltable")

def test_arrays():
	parse("arrays.c", "arrays.dot", "arrays.p", "arrays.symboltable", translate=False)

def test_global_vars():
	parse("global_vars.c", "global_vars.dot", "global_vars.p", "global_vars.symboltable", translate=False)

def test_includes():
	parse("includes.c", "includes.dot", "includes.p", "includes.symboltable", translate=False)

def test_scanf():
	parse("scanf.c", "scanf.dot", "scanf.p", "scanf.symboltable", translate=False)

def test_printf():
	parse("printf.c", "printf.dot", "printf.p", "printf.symboltable", translate=False)

def test_redefining_symbols():
	parse("redefining_symbols.c", "redefining_symbols.dot", "redefining_symbols.p", "redefining_symbols.symboltable")

def test_return_types1():
	parse("return_types1.c", "return_types1.dot", "return_types1.p", "return_types1.symboltable", translate=False)

def test_return_types2():
	parse("return_types2.c", "return_types2.dot", "return_types2.p", "return_types2.symboltable")

def test_minus_values():
	parse("minus_values.c", "minus_values.dot", "minus_values.p", "minus_values.symboltable")

def test_address_assignment():
	parse("address_assignment.c", "address_assignment.dot", "address_assignment.p", "address_assignment.symboltable")

def test_dereference1():
	parse("dereference1.c", "dereference1.dot", "dereference1.p", "dereference1.symboltable", translate=False)

# TODO unlock this task when 'advanced' dereferencing is finished
# def test_dereference2():
# 	parse("dereference2.c", "dereference2.dot", "dereference2.p", "dereference2.symboltable")

def test_by_reference():
	parse("by_reference.c", "by_reference.dot", "by_reference.p", "by_reference.symboltable", translate=False)


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
		"type_check10.c",
		"type_check11.c",
		# "type_check10.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (2,8)) + "Types for initialization don't match ('char' and 'int').",
		determineExPrefix(ExType.error, (3,9)) + "Types for initialization don't match ('float' and 'int').",
		determineExPrefix(ExType.error, (2,9)) + "Types for operation 'Addition' don't match ('int' and 'float').",
		determineExPrefix(ExType.error, (4,5)) + "Types for comparison don't match ('int' and 'float').",
		determineExPrefix(ExType.error, (5,1)) + "Function arguments invalid: 'getCookies' takes 0 arguments (1 argument given).",
		determineExPrefix(ExType.error, (5,1)) + "Function arguments invalid: 'somethingElse' takes 3 arguments (4 arguments given).",
		determineExPrefix(ExType.error, (4,14)) + "Argument for function call 'wrongTypes' did not match the signature ('int' required, 'char' given, argument #2).",
		determineExPrefix(ExType.error, (16,14)) + "Argument for function call 'someFunction' did not match the signature ('char' required, 'int' given, argument #1).",
		determineExPrefix(ExType.error, (6,13)) + "Argument for function call 'thatOtherFunction' did not match the signature ('float' required, 'int' given, argument #2).",
		determineExPrefix(ExType.error, (4,7)) + "Types for initialization don't match ('int' and 'void').",
		determineExPrefix(ExType.error, (8,9)) + "Argument for function call 'aFunction' is not a valid reference argument ('int' reference required, argument #1)."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])


def test_existences():
	# Tests the existenceChecker
	errorFiles = [
		"existence1.c",
		"existence2.c",
		"existence3.c",
		"existence4.c",
		"existence5.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (2,1)) + "Variable 'a' referenced before declaration.",
		determineExPrefix(ExType.error, (4,1)) + "Function 'getCookies' called before declaration.",
		determineExPrefix(ExType.error, (11,25)) + "Variable 'tedt' referenced before declaration.",
		determineExPrefix(ExType.error, (4,9)) + "Function 'test' called before initialisation.",
		determineExPrefix(ExType.error, (9,0)) + "Function 'testing' has already been initialized."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])

def test_duplicate_declarations():
	errorFiles = [
		"dup_decl1.c",
		"dup_decl2.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (3,1)) + "Symbol 'a' has already been declared in this scope.",
		determineExPrefix(ExType.error, (8,1)) + "Symbol 'testing' has already been declared in this scope."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])


def test_wrong_returns():
	errorFiles = [
		"wrong_return1.c",
		"wrong_return2.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (2,1)) + "Return type doesn't match 'testing' signature ('int' required, 'char' given).",
		determineExPrefix(ExType.error, (2,1)) + "Return type doesn't match 'testing' signature ('void' required, 'int' given)."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])


def test_array_wrongAccess():
	errorFiles = [
		"array_wrong_access1.c",
		"array_wrong_access2.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (5,1)) + "Elements of array 'a' should be accessed with an integer.",
		determineExPrefix(ExType.error, (6,1)) + "Elements of array 'myString' should be accessed with an integer."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])


def test_derefences():
	errorFiles = [
		"dereference1.c",
		"dereference2.c",
		"dereference3.c",
		"dereference4.c",
		"dereference5.c"
		]
	errorMessages = [
		determineExPrefix(ExType.error, (5,5)) + "Cannot dereference variable 'a' 4 times (only 3 times allowed).",
		determineExPrefix(ExType.error, (8,1)) + "Types for assignment don't match ('int' and 'float').",
		determineExPrefix(ExType.error, (5,1)) + "Cannot dereference more than 1 variable.",
		determineExPrefix(ExType.error, (5,3)) + "Types for operation 'Addition' don't match ('int*' and 'char').",
		determineExPrefix(ExType.error, (4,2)) + "Cannot dereference non-pointer variable 'a'."
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])



