
from src.py.SA.ErrorMsgHandler import ErrorMsgHandler


def strictEqual(obj1, obj2):
	if type(obj1) is FunctionType:
		return strictEqual(obj2, obj1.returnType)
	elif type(obj1) is ArrayType:
		return strictEqual(obj2, obj1.type)
	elif type(obj1) is PointerType:
		if obj1.ptrCount == 0:
			return strictEqual(obj2, obj1.type)
		elif obj1.ptrCount != 0 and type(obj2) is PointerType:
			return obj1.ptrCount == obj2.ptrCount and strictEqual(obj1.type, obj2.type)
	elif type(obj1) is ReferenceType:
		return strictEqual(obj2, obj1.referencedType)

	if type(obj2) is FunctionType:
		return strictEqual(obj1, obj2.returnType)
	elif type(obj2) is ArrayType:
		return strictEqual(obj1, obj2.type)
	elif type(obj2) is PointerType:
		if obj2.ptrCount == 0:
			return strictEqual(obj1, obj2.type)
		elif obj2.ptrCount != 0 and type(obj1) is PointerType:
			return obj2.ptrCount == obj1.ptrCount and strictEqual(obj2.type, obj1.type)
	elif type(obj2) is ReferenceType:
		return strictEqual(obj1, obj2.referencedType)

	return type(obj1) is type(obj2)
		

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
		return "default"


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
		self.memorySize = 1

	def __str__(self):
		return "int"
	
	def __eq__(self, object):
		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		elif type(object) is ReferenceType:
			return object == self
		elif type(object) is FunctionType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getDefaultValue(self):
		return "0"

	def getPString(self):
		return "i"


class FloatType(VarType):
	def __init__(self):
		self.memorySize = 1

	def __str__(self):
		return "float"

	def __eq__(self, object):
		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		elif type(object) is ReferenceType:
			return object == self
		elif type(object) is FunctionType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getDefaultValue(self):
		return "0.0"

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
		elif type(object) is ReferenceType:
			return object == self
		elif type(object) is FunctionType:
			return object == self
		if type(object) == type(self):
			return True
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getDefaultValue(self):
		return "' '"

	def getPString(self):
		return "c"

class BoolType(VarType):
	def __init__(self):
		self.memorySize = 1

	def __str__(self):
		return "bool"

	def __eq__(self, object):
		if type(object) is BoolType:
			return True

		if type(object) is PointerType:
			return object == self
		elif type(object) is ArrayType:
			return object == self
		elif type(object) is ReferenceType:
			return object == self
		elif type(object) is FunctionType:
			return object == self
		return False

	def addressOf(self):
		return PointerType(self, 1)

	def getDefaultValue(self):
		return "f"

	def getPString(self):
		return "b"

class ReferenceType(VarType):
	def __init__(self, _type):
		self.referencedType = _type

	def __str__(self):
		return str(self.referencedType)

	def __eq__(self, object):
		return object == self.referencedType

	def addressOf(self):
		return self.referencedType.addressOf()
	
	def getDefaultValue(self):
		return self.referencedType.getDefaultValue()

	def getPString(self):
		return self.referencedType.getPString()


class PointerType(VarType):
	def __init__(self, _type, ptrCount):
		self.type = _type
		self.ptrCount = ptrCount
		self.memorySize = 1

	def __str__(self):
		return str(self.type) + ''.join(["*" for i in range(self.ptrCount)])

	def __eq__(self, object):
		if type(object) is ArrayType:
			return object == self
		elif type(object) is ReferenceType:
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
			ErrorMsgHandler.extensiveDereferencing()
		return PointerType(self.type, self.ptrCount - amt)

	def getDefaultValue(self):
		if self.ptrCount != 0:
			return "0"
		return self.type.getDefaultValue()

	def getPString(self):
		if self.ptrCount == 0:
			return self.type.getPString()
		else:
			return "a"


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

	def getDefaultValue(self):
		return self.type.getDefaultValue()

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

	def getDefaultValue(self):
		return self.returnType.getDefaultValue()

	def addressOf(self):
		ErrorMsgHandler.addrOfFunction

	def getPString(self):
		return self.returnType.getPString()





