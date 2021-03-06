from enum import Enum

class ASTNodeType(Enum):
	Assignment = 1
	FloatDecl = 2
	IntDecl = 3
	CharDecl = 4
	LValue = 5
	RValueInt = 6
	RValueFloat = 7
	RValueChar = 8
	RValueExpression = 9 #not used yet
	Program = 10
	Block = 11


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