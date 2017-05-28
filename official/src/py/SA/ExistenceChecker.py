from src.py.AST.ASTNode import ASTNode, ASTNodeType
from src.py.ST.SymbolTable import SymbolTable
from src.py.SA.ErrorMsgHandler import ErrorMsgHandler

class ExistenceChecker:
	def __init__(self, symbolTable):
		self.symbolTable = symbolTable
		self.stdioIncluded = False

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

		elif node.type == ASTNodeType.Printf or node.type == ASTNodeType.Scanf:
			if self.stdioIncluded == False:
				ErrorMsgHandler.undefinedFunction(node, str(node.type.name).lower(), "stdio.h")

		elif node.type == ASTNodeType.Include:
			if node.value == "stdio.h":
				self.stdioIncluded = True



	@staticmethod
	def checkMainExistence(nodeList):
		for (node, nodeLevel) in nodeList:
			if node.type == ASTNodeType.Function and node.value == "main":
				return
		ErrorMsgHandler.mainDoesntExist()
