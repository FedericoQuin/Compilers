from enum import Enum

class AutoNumber(Enum):
	def __new__(cls):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj

class ASTNodeType(AutoNumber):
	Assignment = ()
	FloatDecl = ()
	IntDecl = ()
	CharDecl = ()
	ArrayDecl = ()
	ArrayType = ()
	ArraySize = ()
	LValue = ()
	LValueArrayElement = () # TODO new
	RValueArrayElement = () # TODO new
	ArrayElementIndex = () # TODO new
	RValueInt = ()
	RValueFloat = ()
	RValueChar = ()
	RValueID = ()
	FunctionCall = ()
	Program = ()
	Block = ()
	Addition = ()
	Subtraction = ()
	Mul = ()
	Div = ()
	PrefixIncr = ()
	PostfixIncr = ()
	PrefixDecr = ()
	PostfixDecr = ()
	IfElse = ()
	IfTrue = ()
	IfFalse = ()
	IfCondition = ()
	Or = ()
	And = ()
	Not = ()
	Equals = ()
	NotEquals = ()
	Greater = ()
	GreaterOrEqual = ()
	Less = ()
	LessOrEqual = ()
	While = ()
	WhileCondition = ()
	WhileBody = ()
	For = ()
	ForStmt1 = ()
	ForStmt2 = ()
	ForStmt3 = ()
	ForBody = ()
	NegateBrackets = ()
	Brackets = ()
	Break = ()
	Continue = ()
	Function = ()
	FunctionArgs = ()
	FunctionBody = ()
	FunctionName = ()
	Return = ()
	Void = ()
	Include = ()


class ASTNode:
	ID = 0

	def __init__(self, _type, parent=None, value=None):
		self.type = _type
		self.children = []
		self.parent = parent
		self.value = value

		# maybe temporary
		self.uniqueID = ASTNode.ID
		ASTNode.ID += 1

	def __str__(self):
		''' 
		Returns the dot representation of this node and all its children.
		In this representation the node will have its value displayed aswell if its value is not None.
		'''
		return str(self.uniqueID) + ' [label="' + str(self.type.name) + ( (' \\n' + str(self.value)) if self.value != None else '') + '"];\n' \
			+ getStringOfArray(self.children) \
			+ ''.join([(str(self.uniqueID) + " -> " + str(child.uniqueID) + ";\n") for child in self.children])

	def addChild(self, type, value=None):
		self.children.append(ASTNode(type, self, value))
		return self.children[-1]

	
		
def getStringOfArray(array):
	return ''.join([str(item) for item in array])

class pointerType:
	def __init__(self, _type, ptrCount):
		self.type = _type
		self.ptrCount = ptrCount

		if ptrCount != 0:
			self.name = str(self.type.name) + " " + "".join(["*" for i in range(ptrCount)])
		else:
			self.name = str(self.type.name)
	
	def __str__(self):
		return self.name

	def __repr__(self):
		return str(self)