from enum import Enum
class Scope(Enum):
	GLOBAL = 1
	LOCAL = 2

class SymbolTable:
	""" 
		Class used to store the symbol table when constructing the program text.
		Used implementation: hash tables for different scopes.
	"""
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
		if (scope == Scope.LOCAL):
			assert len(self.localScopeTables) != 0
			self.localScopeTables[-1].addSymbol(symbol, _type)
		else:
			self.globalScopeTable[symbol] = _type
		
	def lookupSymbol(self, symbol):
		"""
			Lookup a symbol in the symboltable. This method checks the local symbol tables first before checking the global table.
			None is returned in case the symbol is not found in any table.
		"""
		localResult = self.searchSymbolLocal(symbol)
		return localResult if localResult != None else self.globalScopeTable[symbol]

	def enterScope(self):
		"""
			Enters a new scope.
		"""
		self.localScopeTables.append(STSingleScope())

	def leaveScope(self):
		"""
			Leaves the current local scope.
		"""
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

		
		

class STSingleScope:
	"""
		Class used to store the symbol table for a single scope segment.
	"""
	def __init__(self):
		self.table = {}

	def __str__(self):
		return str(self.table)

	def contains(self, symbol):
		return self.table[symbol] != None

	def lookupSymbol(self, symbol):
		return self.table[symbol]

	def addSymbol(self, symbol, _type):
		self.table[symbol] = _type
	