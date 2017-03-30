# from copy import deepcopy

class ASTNode:
	ID = 0

	def __init__(self, type, parent=None, value=None):
		self.type = type
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
		return str(self.uniqueID) + ' [label="' + str(self.type) + ((' \\n' + str(self.value)) if self.value != None else '') + '"];\n' \
			+ ''.join([str(child) for child in self.children]) \
			+ ''.join([(str(self.uniqueID) + " -> " + str(child.uniqueID) + ";\n") for child in self.children])

	def addChild(self, type, value=None):
		self.children.append(ASTNode(type, self, value))
		return self.children[-1]

	
		