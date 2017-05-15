


class VarType:
	def __init__(self):
		self.memorySize = 0

	def __repr__(self):
		return str(self)

	def __eq__(self, object):
		if type(object) == type(self):
			return True
		return False
	
	def __ne__(self, object):
		return not(object == self)
	
	def getMemorySize(self):
		return self.memorySize

	def getStrType(self):
		return str(self)

	def getPString(self):
		return ""



class VoidType(VarType):
	def __str__(self):
		return "void"
	
	def __eq__(self, object):
		if type(object) is VoidType:
			return True
		elif type(object) is PointerType:
			return object == self
		return False



class IntType(VarType):
	def __init__(self):
		self.memorySize = 4

	def __str__(self):
		return "int"
	
	def __eq__(self, object):
		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getPString(self):
		return "i"


class FloatType(VarType):
	def __init__(self):
		self.memorySize = 4

	def __str__(self):
		return "float"

	def __eq__(self, object):
		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getPString(self):
		return "r"


class CharType(VarType):
	def __init__(self):
		self.memorySize = 1

	def __str__(self):
		return "char"

	def __eq__(self, object):
		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getPString(self):
		return "c"



class PointerType(VarType):
	def __init__(self, _type, ptrCount):
		self.type = _type
		self.ptrCount = ptrCount
		self.memorySize = 4

	def __str__(self):
		return str(self.type) + ''.join(["*" for i in range(self.ptrCount)])

	def __eq__(self, object):
		if type(object) is ArrayType:
			return object == self
		elif type(object) is IntType and self.ptrCount != 0:
			return True
		if self.ptrCount == 0 and object == self.type:
			return True
		elif type(self) == type(object):
			return self.ptrCount == object.ptrCount and self.type == object.type
		return False

	def addressOf(self):
		return PointerType(self.type, self.ptrCount + 1)

	def dereference(self, amt = 1):
		if amt > self.ptrCount:
			raise Exception("Cannot dereference variable more times than its pointer count.")
		return PointerType(self.type, self.ptrCount - amt)


class ArrayType(VarType):
	def __init__(self, _type, size):
		self.type = _type
		self.size = size
		self.memorySize = self.type.getMemorySize() * self.size

	def __str__(self):
		return str(self.type) + " [" + str(self.size) + "]"
	
	def __eq__(self, object):
		if type(object) == FunctionType:
			return object == self
		if type(object) == type(self) and type(self.type) == type(object.type):
			return True

		return self.type == object

	def getStrType(self):
		return str(self.type)

	def addressOf(self):
		return self.type.addressOf()

	def dereference(self, amt = 1):
		return self.type.dereference(amt)


class FunctionType(VarType):
	def __init__(self, returnType, arguments, initialized = False):
		self.returnType = returnType
		self.arguments = arguments
		self.memorySize = 0
		self.initialized = initialized
		self.declaredVariables = []

	def __str__(self):
		return str(self.returnType) + " func(" + ",".join([str(i) for i in self.arguments]) + ")"

	def __eq__(self, object):
		if type(object) is FunctionType:
			return self.returnType == object.returnType
		
		return self.returnType == object

	def addDeclaredVariable(self, varType):
		self.declaredVariables.append(varType)

	def getStrType(self):
		return str(self.returnType)

	def addressOf(self):
		raise Exception("Dereferencing of functions is not supported.")



