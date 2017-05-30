
from src.py.AST.ASTNode import *
from src.py.UTIL.VarTypes import *

def mapTypeToVarType(nodeType):
	if nodeType == ASTNodeType.IntDecl:
		return IntType()
	elif nodeType == ASTNodeType.FloatDecl:
		return FloatType()
	elif nodeType == ASTNodeType.CharDecl:
		return CharType()
	elif nodeType == ASTNodeType.BoolDecl:
		return BoolType()
	elif nodeType == ASTNodeType.IntSignature:
		return IntType()
	elif nodeType == ASTNodeType.FloatSignature:
		return FloatType()
	elif nodeType == ASTNodeType.CharSignature:
		return CharType()
	elif nodeType == ASTNodeType.Void:
		return VoidType()
		
	raise Exception("Could not map node '" + str(nodeType) + "' to primitive type.")

