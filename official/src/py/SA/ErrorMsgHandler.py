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
		# raise Exception(str(exType) + errorString)


	@staticmethod
	def functionAlreadyInitialised(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Funtion '" + str(node.value) + "' has already been initialized.", node)

	@staticmethod
	def symbolAlreadyDeclared(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Symbol '" + str(node.value) + "' has already been declared in this scope.", node)
	

	@staticmethod
	def varRefBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Variable '" + str(node.value) + "' referenced before declaration.", node)

	@staticmethod
	def functionBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before declaration.", node)

	@staticmethod
	def functionBeforeInit(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' called before initialisation.", node)


	@staticmethod
	def extensiveDerefencing():
		# TODO this has been one of the worst method namings... ever... in like... the history of all method namings.
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference variable more times than its pointer count.")

	@staticmethod
	def addrOfFunction():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Address of functions is not supported.")


		
		


