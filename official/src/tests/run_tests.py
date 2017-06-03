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

def parse(inputFile, dotSolution, pSolution, translate=True):
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

	pSolutionsPath = str(resdir) + "/solutions/" + pSolution
	dotSolutionsPath = str(resdir) + "/solutions/" + dotSolution


	try:
		walker = ParseTreeWalker()
		walker.walk(ASTbuilder, tree)

		ast = ASTbuilder.getAST()

		translator = PTranslator()
		translator.translate(ast, translate=translate)

		translator.saveProgram(pResultPath)
		ASTbuilder.toDot(dotResultPath)

	except Exception as inst:
		fail("Failure for " + str(inputFile) + "\n" + str(inst))
	
	assert(cmp(dotResultPath, dotSolutionsPath))
	if translate:
		assert(cmp(pResultPath, pSolutionsPath))


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



# ===============================
# 			Pointers
# ===============================

def test_address_assignment():
	parse("pointers/address_assignment.c", "pointers/address_assignment.dot", "pointers/address_assignment.p")

def test_advanced_pointers1():
	parse("pointers/advanced_pointers1.c", "pointers/advanced_pointers1.dot", "pointers/advanced_pointers1.p")
	
def test_advanced_pointers2():
	parse("pointers/advanced_pointers2.c", "pointers/advanced_pointers2.dot", "pointers/advanced_pointers2.p")

def test_advanced_pointers3():
	parse("pointers/advanced_pointers3.c", "pointers/advanced_pointers3.dot", "pointers/advanced_pointers3.p")

def test_dereference1():
	parse("pointers/dereference1.c", "pointers/dereference1.dot", "pointers/dereference1.p")

def test_dereference2():
	parse("pointers/dereference2.c", "pointers/dereference2.dot", "pointers/dereference2.p")

def test_pointer():
	parse("pointers/pointer.c", "pointers/pointer.dot", "pointers/pointer.p")

	
# ===============================
# 			Assignments
# ===============================

def test_assignments1bis():
	parse("primitive_types/assignments1bis.c", "primitive_types/assignments1bis.dot", "primitive_types/assignments1bis.p")

def test_assignments1():
	parse("primitive_types/assignments1.c", "primitive_types/assignments1.dot", "primitive_types/assignments1.p")

def test_assignments2():
	parse("primitive_types/assignments2.c", "primitive_types/assignments2.dot", "primitive_types/assignments2.p")
	

# ===============================
# 			Comments
# ===============================

def test_mixed_comments():	
	parse("comments/mixed_comments.c", "comments/mixed_comments.dot", "comments/mixed_comments.p")

def test_multiline_comment():	
	parse("comments/multiline_comment.c", "comments/multiline_comment.dot", "comments/multiline_comment.p")

def test_singleline_comment():	
	parse("comments/singleline_comment.c", "comments/singleline_comment.dot", "comments/singleline_comment.p")


# ===============================
# 		Ifelse, while, ...
# ===============================

def test_break_continue():
	parse("flow_control/break_continue.c", "flow_control/break_continue.dot", "flow_control/break_continue.p")

def test_for():
	parse("flow_control/for.c", "flow_control/for.dot", "flow_control/for.p")

def test_ifelse():
	parse("flow_control/ifelse.c", "flow_control/ifelse.dot", "flow_control/ifelse.p")

def test_while():
	parse("flow_control/while.c", "flow_control/while.dot", "flow_control/while.p")

		
# ===============================
# 			Functions
# ===============================

def test_advanced_function_calls():
	parse("functions/advanced_function_calls.c", "functions/advanced_function_calls.dot", "functions/advanced_function_calls.p")

def test_functions():
	parse("functions/functions.c", "functions/functions.dot", "functions/functions.p")

def test_function_calls():
	parse("functions/function_calls.c", "functions/function_calls.dot", "functions/function_calls.p")

def test_printf1():
	parse("functions/printf1.c", "functions/printf1.dot", "functions/printf1.p")

def test_printf2():
	parse("functions/printf2.c", "functions/printf2.dot", "functions/printf2.p")

def test_return_types1():
	parse("functions/return_types1.c", "functions/return_types1.dot", "functions/return_types1.p")

def test_return_types2():
	parse("functions/return_types2.c", "functions/return_types2.dot", "functions/return_types2.p")

def test_scanf1():
	parse("functions/scanf1.c", "functions/scanf1.dot", "functions/scanf1.p")

def test_scanf2():
	parse("functions/scanf2.c", "functions/scanf2.dot", "functions/scanf2.p")


# ===============================
# 			Arrays
# ===============================
	
def test_arrays():
	parse("miscellaneous/arrays.c", "miscellaneous/arrays.dot", "miscellaneous/arrays.p")

	
# ===============================
# 		  Global vars
# ===============================

def test_advanced_global_var():
	parse("global_variables/advanced_global_var.c", "global_variables/advanced_global_var.dot", "global_variables/advanced_global_var.p")

def test_global_vars():
	parse("global_variables/global_vars.c", "global_variables/global_vars.dot", "global_variables/global_vars.p")


# ===============================
# 		 Negative values
# ===============================

def test_minus_values():
	parse("miscellaneous/minus_values.c", "miscellaneous/minus_values.dot", "miscellaneous/minus_values.p")

def test_negative_expressions():
	parse("miscellaneous/negative_expressions.c", "miscellaneous/negative_expressions.dot", "miscellaneous/negative_expressions.p")


# ===============================
# 		  	Booleans
# ===============================

def test_booleans1():
	parse("primitive_types/booleans1.c", "primitive_types/booleans1.dot", "primitive_types/booleans1.p")

def test_booleans2():
	parse("primitive_types/booleans2.c", "primitive_types/booleans2.dot", "primitive_types/booleans2.p")

def test_booleans3():
	parse("primitive_types/booleans3.c", "primitive_types/booleans3.dot", "primitive_types/booleans3.p")

def test_booleans4():
	parse("primitive_types/booleans4.c", "primitive_types/booleans4.dot", "primitive_types/booleans4.p")


# ===============================
# 		  Miscellaneous
# ===============================

def test_brackets():
	parse("miscellaneous/brackets.c", "miscellaneous/brackets.dot", "miscellaneous/brackets.p")

def test_factorial():
	parse("miscellaneous/factorial.c", "miscellaneous/factorial.dot", "miscellaneous/factorial.p")

def test_includes():
	parse("miscellaneous/includes.c", "miscellaneous/includes.dot", "miscellaneous/includes.p")

def test_main_function():
	parse("miscellaneous/main_function.c", "miscellaneous/main_function.dot", "miscellaneous/main_function.p")

def test_redefining_symbols():
	parse("miscellaneous/redefining_symbols.c", "miscellaneous/redefining_symbols.dot", "miscellaneous/redefining_symbols.p")

def test_by_reference():
	parse("miscellaneous/by_reference.c", "miscellaneous/by_reference.dot", "miscellaneous/by_reference.p")
	
	
	



def test_errors():
	errorFiles = [
		"input_errors/error_braces1.c",
		"input_errors/error_braces2.c",
		# "error_braces3.c"			
		# "error_no_semicolon.c"
		# "error_rubbish.c",		
		# "error_ifelse.c",		
		# "error_for.c",		
		# "error_while.c"		
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
		"type_checking/type_check1.c",
		"type_checking/type_check2.c",
		"type_checking/type_check3.c",
		"type_checking/type_check4.c",
		"type_checking/type_check5.c",
		"type_checking/type_check6.c",
		"type_checking/type_check7.c",
		"type_checking/type_check8.c",
		"type_checking/type_check9.c",
		"type_checking/type_check10.c",
		"type_checking/type_check11.c",
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
		"existence/existence1.c",
		"existence/existence2.c",
		"existence/existence3.c",
		"existence/existence4.c",
		"existence/existence5.c"
	]
	errorMessages = [
		determineExPrefix(ExType.error, (2,1)) + "Variable 'a' referenced before declaration.",
		determineExPrefix(ExType.error, (4,1)) + "Function 'getCookies' called before declaration.",
		determineExPrefix(ExType.error, (11,25)) + "Variable 'tedt' referenced before declaration.",
		determineExPrefix(ExType.error, (4,9)) + "Function 'test' called before initialization.",
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
		"existence/dup_decl1.c",
		"existence/dup_decl2.c"
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
		"type_checking/wrong_return1.c",
		"type_checking/wrong_return2.c"
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
		"arrays/array_wrong_access1.c",
		"arrays/array_wrong_access2.c"
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
		"dereferencing/dereference1.c",
		"dereferencing/dereference2.c",
		"dereferencing/dereference3.c",
		"dereferencing/dereference4.c",
	]
	errorMessages = [
		determineExPrefix(ExType.error, (5,5)) + "Cannot dereference variable 'a' 4 times (only 3 times allowed).",
		determineExPrefix(ExType.error, (8,1)) + "Types for assignment don't match ('int' and 'float').",
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


def test_noIncludes():
	errorFiles = [
		"includes/scanf_include.c",
		"includes/printf_include.c"
	]
	errorMessages = [
		determineExPrefix(ExType.error, (5,1)) + "'scanf' was not declared in this scope (try including header 'stdio.h').",
		determineExPrefix(ExType.error, (5,1)) + "'printf' was not declared in this scope (try including header 'stdio.h').",
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])

def test_formatString():
	errorFiles = [
		"type_checking/printf_argument1.c",
		"type_checking/printf_argument2.c",
		"type_checking/scanf_argument1.c",
		"type_checking/scanf_argument2.c"
	]
	errorMessages = [
		determineExPrefix(ExType.error, (7,37)) + "Type 'int' does not match the argument in the formatstring ('char' required, argument #1).",
		determineExPrefix(ExType.error, (8,42)) + "Type 'char' does not match the argument in the formatstring ('char*' required, argument #2).",
		determineExPrefix(ExType.error, (9,1)) + "Type 'float' does not match the argument in the formatstring ('int' required, argument #3).",
		determineExPrefix(ExType.error, (7,1)) + "Type 'int' does not match the argument in the formatstring ('char*' required, argument #1).",
	]
	for i in range(len(errorFiles)):
		try:
			ASTNode.ID = 0
			parseNoCatch(errorFiles[i], "", "")
		except Exception as inst:
			string = str(inst)
			assert(string == errorMessages[i])

def test_noMain():
	errorFile = "existence/nomain.c"
	errorMessage = determineExPrefix(ExType.error, None) + "The program does not contain a 'main' function."

	try:
		ASTNode.ID = 0
		parseNoCatch(errorFile, "", "")
	except Exception as inst:
		string = str(inst)
		assert(string == errorMessage)

