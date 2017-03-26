# from copy import deepcopy

class ASTNode:
	ID = 0

	def __init__(self, type, parent=None, value=None):
		self.type = type
		self.children = []
		self.parent = parent
		self.value = None

		# maybe temporary
		self.uniqueID = ASTNode.ID
		ASTNode.ID += 1

	def __str__(self):
		return str(self.uniqueID) + ' [label="' + str(self.type) + '"];\n' + ''.join([str(child) for child in self.children]) \
			+ ''.join([(str(self.uniqueID) + " -> " + str(child.uniqueID) + ";\n") for child in self.children])

	def addChild(self, type, value=None):
		self.children.append(ASTNode(type, self, value))
		return self.children[-1]

	
		