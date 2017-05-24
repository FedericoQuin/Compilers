
from src.py.AST.ASTNode import ASTNodeType


class UselessDecorator:
	def __init__(self):
		self.nodeLevel = None

		# List of potential useless nodes.
		self.potentialUselessNodes = [ASTNodeType.RValueArrayElement, ASTNodeType.RValueInt, \
			ASTNodeType.RValueFloat, ASTNodeType.RValueChar, ASTNodeType.RValueID, ASTNodeType.RValueAddress, \
			ASTNodeType.FunctionCall, ASTNodeType.Addition, ASTNodeType.Subtraction, ASTNodeType.Mul, \
			ASTNodeType.Div, ASTNodeType.Dereference]

	def checkUselessness(self, node, nodeLevel):
		"""Checks if a node is useless. If it is, adjust the node."""
		if self.nodeLevel != None and nodeLevel <= self.nodeLevel:
			self.nodeLevel = None
		# If subnodes also need to be labeled useless, adjust it here


		# Verify that the node is useful/useless
		# To do this, check its parents in the 'body' in which it resides
		# If none of the parents are, for example, an initiliazation, we can conclude that the node is useless.
		#
		# Example 1:
		#		for (int i = 5; i < 20; i==) {
		#			i + 5;
		#		}
		# In this case, the parent of the Addition node is a ForBody. We can conclude the node is useless since it is not used.
		#
		# Example 2:
		# 		int getCookies() {return 5;}
		#	
		#		int main() {
		#			getCookies();
		#		}
		# The return value of getCookies is not used, therefore the function call is useless.
		if node.type in self.potentialUselessNodes and self.nodeLevel == None:
			currentNode = node.parent

			while currentNode != None:
				# If the node is the end of a code block, and no useful node has been found on the path -> conclude that the original node is useless
				if self.isEndBlock(currentNode):
					break

				if self.isUsefulNode(currentNode):
					# Stop the function if a useful node has been found, don't adjust anything
					return
				currentNode = currentNode.parent
				
			# TODO remove, here for debugging reasons
			# print("Found a useless node!!!\n" + str(node.type) + " at " + "(" + ",".join([str(i) for i in node.position]) + ")" + "\n")
			node.useless = True
			self.nodeLevel = nodeLevel
				

	def isEndBlock(self, node):
		potentialNodes = [ASTNodeType.WhileBody, ASTNodeType.ForBody, ASTNodeType.FunctionBody, ASTNodeType.Block]
		return node.type in potentialNodes
		
	def isUsefulNode(self, node):
		# TODO make sure what to do with printf, scanf
		usefulNodes = [ASTNodeType.Assignment, ASTNodeType.Initialization, ASTNodeType.FunctionCall, \
			ASTNodeType.Or, ASTNodeType.And, ASTNodeType.Not, ASTNodeType.Equals, ASTNodeType.NotEquals, \
			ASTNodeType.Greater, ASTNodeType.GreaterOrEqual, ASTNodeType.Less, ASTNodeType.LessOrEqual, \
			ASTNodeType.NegateBrackets, ASTNodeType.Return, ASTNodeType.Condition, ASTNodeType.Scanf, ASTNodeType.Printf]
		return node.type in usefulNodes
