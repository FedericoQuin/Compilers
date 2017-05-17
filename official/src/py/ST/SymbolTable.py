from enum import Enum
from src.py.UTIL.VarTypes import *


class Scope(Enum):
	GLOBAL = 1
	LOCAL = 2


class SymbolTable:
	""" 
		Class used to store the symbol table when constructing the program text.
		Used implementation: tree like structure with hash tables for different scopes.
	"""

	
	def __init__(self):
		self.globalScopeTable = {}
		self.localScopeTables = STTree()


	def insertEntry(self, symbol, _type, scope = Scope.LOCAL):
		"""
			Insert an entry into the symbol table, at the specified scope (GLOBAL or LOCAL).
		"""
		if (scope == Scope.LOCAL):
			self.localScopeTables.addSymbol(symbol, _type)
		else:
			self.globalScopeTable[symbol] = SymbolMapping(_type)
		
	def lookupSymbol(self, symbol, scope=None, level=None):
		"""
			Lookup a symbol in the symboltable. This method checks the local symbol tables first before checking the global table.
			None is returned in case the symbol is not found in any table.
		"""
		if scope == None:
			localResult = self.searchSymbolLocal(symbol, level)
			return localResult if localResult != None else self.searchSymbolGlobal(symbol)
		elif scope == Scope.GLOBAL:
			return self.searchSymbolGlobal(symbol)
		elif scope == Scope.LOCAL:
			return self.searchSymbolLocal(symbol, level)

		return None


	def lookupFunction(self, symbol):
		"""
			Looks up a function in the symbol table (equivalent of a normal lookup, but always in the global scope).
		"""
		return lookupSymbol(symbol, Scope.GLOBAL)


	def symbolExists(self, symbol, scope=None):
		if (scope == None):
			return self.lookupSymbol(symbol) != None
		elif (scope == Scope.LOCAL):
			return self.searchSymbolLocal(symbol) != None
		elif (scope == Scope.GLOBAL):
			return symbol in self.globalScopeTable
		
		return False


	def enterScope(self):
		"""
			Enters a new scope.
		"""
		self.localScopeTables.enterScope()

	def leaveScope(self):
		"""
			Leaves the current local scope.
		"""
		self.localScopeTables.leaveScope()


	def searchSymbolLocal(self, symbol, level=None):
		"""
			Searches for the symbol in the local symbol tables.
			Returns None if the symbol is not found.
		"""
		return self.localScopeTables.lookupSymbol(symbol, level)

	def searchSymbolGlobal(self, symbol):
		"""
			Searches for the symbol in the global symbol table.
			Returns None if the symbol is not found.
		"""
		if symbol in self.globalScopeTable:
			return self.globalScopeTable[symbol]

		return None

	def getDefOcc(self, symbol):
		if self.symbolExists(symbol, Scope.GLOBAL):
			return 0
		else:
			return self.localScopeTables.getDefOcc(symbol)

	def getAppOcc(self):
		return self.localScopeTables.getDeepestLevel()




class STTree:
	def __init__(self):
		self.root = STSingleScope()

	def addSymbol(self, symbol, _type):
		#propagate to lowest level in symbol table
		assert self.rootActive()
		self.root.addSymbol(symbol, _type)

	def lookupSymbol(self, symbol, level):
		# Looks up the symbol in the symbol table
		# @param forced: forces to look in all possible scopes
		if level != None:
			level += 1
		return self.root.lookupSymbol(symbol, level)

	def enterScope(self):
		self.root.enterScope()

	def leaveScope(self):
		assert self.rootActive()
		self.root.leaveScope()

	def rootActive(self):
		return self.root.childActive == True

	def getDefOcc(self, symbol):
		return self.root.getDefOcc(symbol)	
	
	def getDeepestLevel(self):
		return self.root.getDeepestLevel()


class STSingleScope:
	"""
		Class used to store the symbol table for a single scope segment, and all the scopes below it.
	"""
	def __init__(self, parent=None, nextAddress=0):
		self.table = {}
		self.subScopes = []
		self.parent = parent
		self.nextAddress = nextAddress

		# Variable used to indicate wether the last child is 'active' --> used when adding new symbols
		self.childActive = False 

	def __str__(self):
		return str(self.table)

	def contains(self, symbol):
		if symbol in self.table:
			return True
		if self.childActive == True:
			return self.subScopes[-1].contains(symbol)
		return False

	def lookupSymbol(self, symbol, level):
		if level != None:
			if level == 0:
				return self.table[symbol] if symbol in self.table else None
			else:
				assert self.childActive
				return self.subScopes[-1].lookupSymbol(symbol, level - 1)
		
		mapping = None
		# Give priority to subscopes if present
		if self.childActive == True:
			mapping = self.subScopes[-1].lookupSymbol(symbol, None)
		
		if (mapping == None) and (symbol in self.table):
			mapping = self.table[symbol]
		return mapping

	def addSymbol(self, symbol, _type):
		if self.childActive == True:
			self.subScopes[-1].addSymbol(symbol, _type)
			return
		self.table[symbol] = SymbolMapping(_type, self.nextAddress)

		if self.parent != None:
			self.nextAddress += 4
	
	def getSymbolCount(self):
		return len(self.table)

	def enterScope(self):
		if self.childActive == True:
			self.subScopes[-1].enterScope()
			return
			
		self.childActive = True
		self.subScopes.append(STSingleScope(self, self.nextAddress))
		
	def leaveScope(self):
		if self.childActive == True and self.subScopes[-1].childActive == True:
			self.subScopes[-1].leaveScope()
			return
		self.childActive = False

		if self.parent != None:
			self.nextAddress = self.subScopes[-1].nextAddress

	def getDefOcc(self, symbol, level=0):
		lowerLevelOcc = None
		if self.childActive:
			lowerLevelOcc = self.subScopes[-1].getDefOcc(symbol, level+1)
		
		if lowerLevelOcc != None:
			return lowerLevelOcc
		elif self.contains(symbol):
			return level
		
		return None

	def getDeepestLevel(self, level=0):
		if self.childActive:
			return self.subScopes[-1].getDeepestLevel(level+1)
		return level


class SymbolMapping:
	def __init__(self, _type, address=0):
		self.type = _type
		self.address = address
	
	def __str__(self):
		return str(self.type)

	def __repr__(self):
		return str(self)