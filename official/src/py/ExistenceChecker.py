from src.py.AST.ASTNode import ASTNode, ASTNodeType
from src.py.ST.SymbolTable import SymbolTable

class ExistenceChecker:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable

	def checkExistence(self, node):
		if node.type == ASTNodeType.LValue \
			or node.type == ASTNodeType.LValueArrayElement \
			or node.type == ASTNodeType.RValueArrayElement \
			or node.type == ASTNodeType.RValueID:
			
			# Check wether the symbol is present in the symboltable, otherwise throw an error
			if self.symbolTable.lookupSymbol(node.value) == None:
				raise Exception("Error: variable '" + str(node.value) + "' referenced before declaration.")
		
		elif node.type == ASTNodeType.FunctionCall:
			# Is the function declared?
			if self.symbolTable.lookupSymbol(node.value) == None:
				raise Exception("Error: function '" + str(node.value) + "' called before declaration.")
			# Is the function initialized yet?
			elif self.symbolTable.lookupSymbol(node.value).type.initialized == False:
				raise Exception("Error: function '" + str(node.value) + "' called before initialisation.")