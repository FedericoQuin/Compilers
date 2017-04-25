from enum import Enum
from src.py.VarTypes import *


class Scope(Enum):
	GLOBAL = 1
	LOCAL = 2


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
		
	def lookupSymbol(self, symbol, scope=None, level=None):
		"""
			Lookup a symbol in the symboltable. This method checks the local symbol tables first before checking the global table.
			None is returned in case the symbol is not found in any table.
		"""
		if scope == None:
			localResult = self.searchSymbolLocal(symbol)
			return localResult if localResult != None else self.searchSymbolGlobal(symbol)
		elif scope == Scope.GLOBAL:
			return self.searchSymbolGlobal(symbol)
		elif scope == Scope.LOCAL:
			if level == None:
				return self.searchSymbolLocal(symbol)
			else:
				return self.localScopeTables[level].lookupSymbol(symbol)

		return None

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
		if symbol in self.table:
			return self.table[symbol]
		return None

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