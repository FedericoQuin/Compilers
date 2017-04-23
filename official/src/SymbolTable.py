from enum import Enum
class Scope(Enum):
	GLOBAL = 1
	LOCAL = 2


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






class SymbolTable:
	""" 
		Class used to store the symbol table when constructing the program text.
		Used implementation: hash tables for different scopes.
	"""

	# Static variable to hold current Allocation Address for new symbols, denoted in bytes.
	AllocationAddress = 0
	
	
	def __init__(self):
		self.globalScopeTable = {}
		self.localScopeTables = []

	def __str__(self):
		return "Global - " + str(self.globalScopeTable) + "\n" + \
			"\n".join(["Scope " + str(self.localScopeTables.index(table)+1) + " - " + str(table) for table in self.localScopeTables])

	def insertEntry(self, symbol, _type, scope = Scope.LOCAL):
		"""
			Insert an entry into the symbol table, at the specified scope (GLOBAL or LOCAL).
		"""

		# assign enough memory, depending on the type of the symbol
		# NOTE global variables should not collide with local variables,
		#	   since global variables can only be inserted when no local scope is open
		beginAddress = self.assignAddress(_type)

		if (scope == Scope.LOCAL):
			assert len(self.localScopeTables) != 0
			self.localScopeTables[-1].addSymbol(symbol, _type, beginAddress)
		else:
			self.globalScopeTable[symbol] = SymbolMapping(_type, beginAddress)
		
	def lookupSymbol(self, symbol):
		"""
			Lookup a symbol in the symboltable. This method checks the local symbol tables first before checking the global table.
			None is returned in case the symbol is not found in any table.
		"""
		localResult = self.searchSymbolLocal(symbol)
		return localResult if localResult != None else self.searchSymbolGlobal(symbol)

	def symbolExists(self, symbol, scope=None):
		if (scope == None):
			return True if self.lookupSymbol(symbol) != None else False
		elif (scope == Scope.LOCAL):
			return True if self.searchSymbolLocal(symbol) != None else False
		elif (scope == Scope.GLOBAL):
			return True if symbol in self.globalScopeTable else False
		
		return False

	def enterScope(self):
		"""
			Enters a new scope.
		"""
		self.localScopeTables.append(STSingleScope(SymbolTable.AllocationAddress))

	def leaveScope(self):
		"""
			Leaves the current local scope.
		"""
		# 'free' up all the memory addresses used in the local scope first
		SymbolTable.AllocationAddress = self.localScopeTables[-1].getBeginAddress()
		del self.localScopeTables[-1]

	def searchSymbolLocal(self, symbol):
		"""
			Searches for the symbol in the local symbol tables.
			Returns None if the symbol is not found.
		"""
		for table in reversed(self.localScopeTables):
			# reversed order because the most local table is found at the last entry.
			if (table.contains(symbol)):
				return table.lookupSymbol(symbol)

		return None

	def searchSymbolGlobal(self, symbol):
		"""
			Searches for the symbol in the global symbol table.
			Returns None if the symbol is not found.
		"""
		if symbol in self.globalScopeTable:
			return self.globalScopeTable[symbol]

		return None

	def assignAddress(self, _type):
		"""
			Provides (virtual) space for a variable of type _type.
		"""
		# TODO not sure if values are accurate
		address = SymbolTable.AllocationAddress

		SymbolTable.AllocationAddress += self.getMemorySize(_type)
		if address == SymbolTable.AllocationAddress:
			return None
		return address

	def getMemorySize(self, _type):
		return _type.getMemorySize()



class STSingleScope:
	"""
		Class used to store the symbol table for a single scope segment.
	"""
	def __init__(self, beginAddress):
		self.table = {}
		self.beginAddress = beginAddress

	def __str__(self):
		return str(self.table)

	def contains(self, symbol):
		return symbol in self.table

	def lookupSymbol(self, symbol):
		return self.table[symbol]

	def addSymbol(self, symbol, _type, addr = 0):
		self.table[symbol] = SymbolMapping(_type, addr)
	
	def getSymbolCount(self):
		return len(self.table)

	def getBeginAddress(self):
		return self.beginAddress


class SymbolMapping:
	def __init__(self, _type, addr):
		self.type = _type
		self.addr = addr
	
	def __str__(self):
		return "(" + str(self.type) + ", " + str(self.addr) + ")"

	def __repr__(self):
		return str(self)