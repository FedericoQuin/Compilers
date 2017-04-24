


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

class VoidType(VarType):
	def __str__(self):
		return "void"
	
	def __eq__(self, object):
		if type(object) is VoidType:
			return True
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

class FunctionType(VarType):
	def __init__(self, returnType, arguments):
		self.returnType = returnType
		self.arguments = arguments
		self.memorySize = 0

	def __str__(self):
		return str(self.returnType) + " func(" + ",".join([str(i) for i in self.arguments]) + ")"

	def __eq__(self, object):
		if type(object) is FunctionType:
			return self.returnType == object.returnType
		
		return self.returnType == object

	def getStrType(self):
		return str(self.returnType)



