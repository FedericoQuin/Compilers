
from src.py.AST.ASTNode import ASTNodeType, pointerType
from src.py.AST.AST import AST
from src.py.ST.SymbolTable import SymbolTable, SymbolMapping
from src.py.UTIL.VarTypes import *


class TypeDeductor:
	
	@staticmethod
	def deductType(node, symbolTable):
		"""
			Returns the type of the (rvalue) node.
		"""
		if node.type == ASTNodeType.RValueChar:
			return CharType()
		elif node.type == ASTNodeType.RValueInt:
			return IntType()
		elif node.type == ASTNodeType.RValueFloat:
			return FloatType()
		elif node.type == ASTNodeType.RValueID:
			nodeType = symbolTable.lookupSymbol(node.value).type
			# Return the type, except if the ID references an array (without element access)
			return nodeType if not(type(nodeType) is ArrayType) else nodeType.addressOf()
		elif node.type == ASTNodeType.LValue:
			nodeType = symbolTable.lookupSymbol(node.value).type
			return nodeType if not(type(nodeType) is ArrayType) else nodeType.addressOf()
		elif node.type == ASTNodeType.Addition:
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Subtraction:
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Mul:
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Div:
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Brackets:
			return TypeDeductor.deductType(node.children[0], symbolTable)
		elif node.type == ASTNodeType.FunctionCall:
			return symbolTable.lookupSymbol(node.value).type
		elif node.type == ASTNodeType.RValueArrayElement:
			return symbolTable.lookupSymbol(node.value).type.type
		elif node.type == ASTNodeType.LValueArrayElement:
			return symbolTable.lookupSymbol(node.value).type.type
		elif node.type == ASTNodeType.RValueAddress:
			return symbolTable.lookupSymbol(node.children[0].value).type.addressOf()
		elif node.type == ASTNodeType.Dereference:
			return TypeDeductor.checkDereferenceValidity(node, symbolTable)
		elif node.type == ASTNodeType.Greater or \
			node.type == ASTNodeType.GreaterOrEqual or \
			node.type == ASTNodeType.Or or \
			node.type == ASTNodeType.And or \
			node.type == ASTNodeType.Equals or \
			node.type == ASTNodeType.NotEquals or \
			node.type == ASTNodeType.Less or \
			node.type == ASTNodeType.LessOrEqual:
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Not or \
			node.type == ASTNodeType.Brackets or \
			node.type == ASTNodeType.NegateBrackets:
			return TypeDeductor.deductType(node.children[0], symbolTable)
		else:
			raise Exception("Could not deduct type of node '" + str(node.type.name) + "'.")


	@staticmethod
	def checkDereferenceValidity(node, symbolTable):
		"""
			Checks the validity of dereferencing.
			Returns the type after dereferencing.
		"""
		queue = [node]
		rvalueSymbol = None
		derefCount = 0

		while len(queue) != 0:
			currentNode = queue.pop()
			[queue.append(i) for i in currentNode.children]

			if currentNode.type == ASTNodeType.Dereference:
				derefCount += len(currentNode.value)
			elif currentNode.type == ASTNodeType.RValueID:
				if rvalueSymbol != None:
					raise Exception("Error: cannot dereference more than 1 variable.")
				rvalueSymbol = currentNode.value
			else:
				# All other nodes are part of an expression
				rType = type(TypeDeductor.deductType(currentNode, symbolTable))
				if not(rType is IntType) and not(rType is PointerType):
					raise Exception("Error: cannot dereference non-int/pointer expressions.")
		
		rvalueIdType = symbolTable.lookupSymbol(rvalueSymbol).type
		if type(rvalueIdType) is ArrayType:
			rvalueIdType = rvalueIdType.addressOf()
		
		if not(type(rvalueIdType) is PointerType):
			raise Exception("Error: cannot dereference non-pointer variable '" + str(rvalueSymbol) + "'.")
		if derefCount > rvalueIdType.ptrCount:
			if rvalueIdType.ptrCount == 0:
				raise Exception("Error: cannot dereference non-pointer variable '" + str(rvalueSymbol) + "'.")
			raise Exception("Error: cannot dereference variable '" + rvalueSymbol + "' " + str(derefCount) + " times (only " \
				+ str(rvalueIdType.ptrCount) + (" times" if rvalueIdType.ptrCount != 1 else " time") + " allowed).")

		return rvalueIdType.dereference(derefCount)


	@staticmethod
	def checkTypeChildrenExpression(children, symbolTable):
		"""
			Compares the types of the children. If the types differ: throw Exception.
			Returns the type of the children if equal.
		"""
		type1 = TypeDeductor.deductType(children[0], symbolTable)
		type2 = TypeDeductor.deductType(children[1], symbolTable)
		if (type1 != type2):
			raise Exception("Types do not match: " + type1.getStrType() + " and " + type2.getStrType() + ".")
		return type1