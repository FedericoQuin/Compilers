from enum import Enum


class AnsiEscapeCodes(Enum):
	Red = 1
	Purple = 2
	Clean = 3

	def __str__(self):
		if self.value == AnsiEscapeCodes.Red.value:
			return "\033[1;31m"
		elif self.value == AnsiEscapeCodes.Purple.value:
			return "\033[1;35m"
		elif self.value == AnsiEscapeCodes.Clean.value:
			return "\033[0m"


# Lowercase enum values because Warning is a python keyword :(
class ExType(Enum):
	error = 1
	warning = 2

	def __str__(self):
		if self.value == ExType.error.value:
			return "Error: "
		elif self.value == ExType.warning.value:
			return "Warning: "
		return ""

	def getColor(self):
		if self.value == ExType.error.value:
			return str(AnsiEscapeCodes.Red)
		elif self.value == ExType.warning.value:
			return str(AnsiEscapeCodes.Purple)
		return str(AnsiEscapeCodes.Clean)




def determineExPrefix(exType, position):
	return exType.getColor() + \
		("" if position == None else "(" + ",".join([str(i) for i in position]) + ")") + \
		" " + str(exType) + str(AnsiEscapeCodes.Clean)



# TODO figure out if splitting up exceptions in different custom exceptions is of any value
# TODO warning messages for (if time permits this):
#	- reference before assignment of variable
#	- access outside array

class ErrorMsgHandler:
	@staticmethod
	def throwErrorMessage(exType, errorString, node=None):
		raise Exception(determineExPrefix(exType, (None if node == None else node.position)) + errorString)

	# =============================
	# SymboltableBuilder exceptions
	# =============================
	@staticmethod
	def functionAlreadyInitialised(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Funtion '" + str(node.value) + "' has already been initialized.", node)

	@staticmethod
	def symbolAlreadyDeclared(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Symbol '" + str(node.value) + "' has already been declared in this scope.", node)
	

	# ===========================
	# ExistenceChecker exceptions
	# ===========================
	@staticmethod
	def varRefBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Variable '" + str(node.value) + "' referenced before declaration.", node)

	@staticmethod
	def functionBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before declaration.", node)

	@staticmethod
	def functionBeforeInit(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before initialisation.", node)


	# ===================
	# VarTypes exceptions
	# ===================
	@staticmethod
	def extensiveDerefencing():
		# TODO this has been one of the worst method namings... ever... in like... the history of all method namings.
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference variable more times than its pointer count.")

	@staticmethod
	def addrOfFunction():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Address of functions is not supported.")

	# ======================
	# TypeChecker exceptions
	# ======================
	@staticmethod
	def typesAssignmentWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for assignment don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)

	@staticmethod
	def typesComparisonWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for comparison don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)

	@staticmethod
	def returnTypeWrong(node, functionSymbol, requiredType, givenType):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Return type doesn't match '" + functionSymbol + "' signature ('" + requiredType.getStrType() + "' required, '" + givenType.getStrType() + "' given).", \
			node)

	@staticmethod
	def typeInitWrong(node, type1, type2):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for initialization don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)
		pass

	@staticmethod
	def arrayElementWrongAccess(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Elements of array '" + str(node.value) + "' should be accessed with an integer.", node)

	@staticmethod
	def functionArgsInvalid(node, amtRequired, amtGiven):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Function arguments invalid: '" + str(node.value) + "' takes " \
			+ str(amtRequired) + " " + ("arguments" if amtRequired != 1 else "argument") + " " + \
			"(" + str(amtGiven) + " " + ("arguments" if amtGiven != 1 else "argument") + " given).", \
			node)

	@staticmethod
	def functionArgWrong(node, typeReq, typeGiven, index):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Argument for function call '" + str(node.value) + "' did not match the signature ('" \
			+ typeReq.getStrType() + "' required, '" + typeGiven.getStrType() + "' given, argument #" + str(index) + ").", \
			node)


	# =======================
	# TypeDeductor exceptions
	# =======================
	@staticmethod
	def derefMultipleVars(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference more than 1 variable.", node)

	@staticmethod
	def derefInvalidExpression(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference non-int/pointer expressions.", node)

	@staticmethod
	def derefNonPointer(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference non-pointer variable '" + str(node.value) + "'.", node)

	@staticmethod
	def overDereferencing(node, maxAmt, amt):
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Cannot dereference variable '" + str(node.value) + "' " + str(amt) + " times (only " \
			+ str(maxAmt) + (" times" if maxAmt != 1 else " time") + " allowed).", \
			node)

	@staticmethod
	def typesOperationWrong(node, type1, type2, operationNode):
		# TODO make sure operationNode is always valid by checking TypeDeductor method
		ErrorMsgHandler.throwErrorMessage(ExType.error, \
			"Types for operation '" + str(operationNode.type.name) + "' don't match ('" + type1.getStrType() + "' and '" + type2.getStrType() + "').", \
			node)


