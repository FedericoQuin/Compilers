from src.py.AST.ASTNode import ASTNode, ASTNodeType
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.ErrorMsgHandler import ErrorMsgHandler

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
				ErrorMsgHandler.varRefBeforeDecl(node)
		
		elif node.type == ASTNodeType.FunctionCall:
			# Is the function declared?
			if self.symbolTable.lookupSymbol(node.value) == None:
				ErrorMsgHandler.functionBeforeDecl(node)
			# Is the function initialized yet?
			elif self.symbolTable.lookupSymbol(node.value).type.initialized == False:
				ErrorMsgHandler.functionBeforeInit(node)