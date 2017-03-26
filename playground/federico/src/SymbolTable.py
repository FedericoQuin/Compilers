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
        self.localScopeTable = {}

    def insertEntry(self, symbol, type, scope = Scope.LOCAL):
        if (scope == Scope.LOCAL):
            # temporary placeholder, simple testing for now
            self.localScopeTable[symbol] = type
        else:
            self.globalScopeTable[symbol] = type
        
    def lookupSymbol(self, symbol):
        if (self.localScopeTable[symbol] != None):
            return self.localScopeTable[symbol]
        else:
            return self.globalScopeTable[symbol]
