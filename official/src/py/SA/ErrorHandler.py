from enum import Enum

# Lowercase enum values because Warning is a python keyword :(
class ExType(Enum):
	error = 1
	warning = 2

	def __str__(self):
		if self.value == ExType.error.value:
			return "\033[4;31m" + "Error: " + "\033[0m"
		elif self.value == ExType.warning.value:
			return "\033[1;35m" + "Warning: " + "\033[0m"
		return ""


# TODO figure out if splitting up exceptions in different custom exceptions is of any value
# TODO warning messages for (if time permits this):
#	- reference before assignment of variable
#	- access outside array

class ErrorMsgHandler:
	@staticmethod
	def throwErrorMessage(excType, errorString):
		raise Exception(str(excType) + errorString)


	@staticmethod
	def functionAlreadyDeclared(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Funtion '" + str(node.value) + "' has already been initialized.")

	@staticmethod
	def symbolAlreadyDeclared(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Symbol '" + str(node.value) + "' has already been declared in this scope.")
	

	@staticmethod
	def varRefBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Variable '" + str(node.value) + "' referenced before declaration.")

	@staticmethod
	def functionBeforeDecl(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' before declaration.")

	@staticmethod
	def functionBeforeInit(node):
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Function '" + str(node.value) + "' before initialisation.")


	@staticmethod
	def extensiveDerefencing():
		# TODO this has been one of the worst method namings... ever... in like... the history of all method namings.
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Cannot dereference variable more times than its pointer count.")

	@staticmethod
	def addrOfFunction():
		ErrorMsgHandler.throwErrorMessage(ExType.error, "Address of functions is not supported.")


		
		


