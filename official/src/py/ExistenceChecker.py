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
				raise Exception("Error: variable referenced before declaration: " + str(node.value) + ".")
		
		elif node.type == ASTNodeType.FunctionCall:
			if self.symbolTable.lookupSymbol(node.value) == None:
				raise Exception("Error: function called before declaration: " + str(node.value) + ".")