
from src.py.AST.ASTNode import ASTNodeType, pointerType
from src.py.AST.AST import AST
from src.py.ST.SymbolTable import SymbolTable, SymbolMapping
from src.py.UTIL.VarTypes import *
from src.py.SA.ErrorMsgHandler import ErrorMsgHandler


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
		elif node.type == ASTNodeType.RValueBool:
			return BoolType()
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
			# Check to see if the children are of equal type
			return TypeDeductor.checkTypeChildrenExpression(node.children, symbolTable)
		elif node.type == ASTNodeType.Not or \
			node.type == ASTNodeType.Brackets or \
			node.type == ASTNodeType.NegateBrackets:
			return TypeDeductor.deductType(node.children[0], symbolTable)
		elif node.type == ASTNodeType.Negate:
			childType = TypeDeductor.deductType(node.children[0], symbolTable)
			if not(childType == IntType() or childType == FloatType()):
				ErrorMsgHandler.negateInvalid(node, childType)
			return childType
		elif node.type == ASTNodeType.Condition:
			# Don't need to typecheck further, handled later
			return BoolType()
		else:
			raise Exception("Could not deduct type of node '" + str(node.type.name) + "'.")


	@staticmethod
	def checkDereferenceValidity(node, symbolTable):
		"""
			Checks the validity of dereferencing.
			Returns the type after dereferencing.
		"""

		def getPtrCount(node, originalNode, stopAtExpressionOperator = False):
			operations = [ASTNodeType.Negate, ASTNodeType.Addition, ASTNodeType.Subtraction, \
				ASTNodeType.Mul, ASTNodeType.Div, ASTNodeType.Or, ASTNodeType.And, ASTNodeType.Not, \
				ASTNodeType.Equals, ASTNodeType.NotEquals, ASTNodeType.Greater, ASTNodeType.GreaterOrEqual, \
				ASTNodeType.Less, ASTNodeType.LessOrEqual]
			count = 0
			while node != originalNode:
				node = node.parent
				if node.type == ASTNodeType.Dereference:
					count += node.value.count("*")
				elif node.type in operations and stopAtExpressionOperator == True:
					return count
			return count

		queue = [node]
		derefType = None
		typeDerefCount = 0


		while len(queue) != 0:
			currentNode = queue.pop()
			[queue.append(i) for i in currentNode.children]

			if currentNode.type == ASTNodeType.Dereference:
				pass
			elif currentNode.type == ASTNodeType.RValueID or currentNode.type == ASTNodeType.RValueArrayElement:
				newType = TypeDeductor.deductType(currentNode, symbolTable)
				if type(newType) is ArrayType:
					newType = newType.addressOf()
				elif type(newType) is ReferenceType:
					newType = newType.referencedType

				totalCount = getPtrCount(currentNode, node)
				partialCount = getPtrCount(currentNode, node, True)

				if partialCount == 0:
					# TODO add check for int values
					pass
				elif type(newType) != PointerType:
					ErrorMsgHandler.derefNonPointer(currentNode)
				elif newType.ptrCount == 0:
					ErrorMsgHandler.derefNonPointer(currentNode)
				elif newType.ptrCount < partialCount:
					ErrorMsgHandler.overDereferencing(currentNode, newType.ptrCount, partialCount)
				
				if typeDerefCount < totalCount and newType.ptrCount >= totalCount:
					typeDerefCount = totalCount
					derefType = newType.dereference(totalCount)
				elif typeDerefCount < partialCount and newType.ptrCount >= partialCount:
					typeDerefCount = partialCount
					derefType = newType.dereference(partialCount)					
				elif derefType != None and newType.ptrCount > derefType.ptrCount:
					derefType = newType.dereference(typeDerefCount)

			else:
				# All other nodes are part of an expression
				rType = type(TypeDeductor.deductType(currentNode, symbolTable))
				if not(rType is IntType) and not(rType is PointerType):
					ErrorMsgHandler.derefInvalidExpression(node)

		
		if derefType == None:
			print("whyyyyyy")
		return derefType


	@staticmethod
	def checkTypeChildrenExpression(children, symbolTable):
		"""
			Compares the types of the children. If the types differ: throw Exception.
			Returns the type of the children if equal.
		"""
		type1 = TypeDeductor.deductType(children[0], symbolTable)
		type2 = TypeDeductor.deductType(children[1], symbolTable)
		if (type1 != type2):
			ErrorMsgHandler.typesOperationWrong(children[0], type1, type2, children[0].parent)
		return type1