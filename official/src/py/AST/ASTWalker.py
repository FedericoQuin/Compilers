
from src.py.AST.AST import AST
from src.py.AST.ASTNode import *

class ASTWalker:
	def __init__(self, ast):
		self.nodes = []
		self.AST = ast

	def traverseDepthFirst(self):
		# The queue stores tuples of the node, and on which level in the AST it belongs
		queue = []
		queue.append((self.AST.root, 0))

		while (len(queue) != 0):
			currentNode = queue.pop(0)
			for node in reversed(currentNode[0].children):
				queue.insert(0,(node, currentNode[1] + 1))
			self.nodes.append(currentNode)

	def getNodesDepthFirst(self):
		"""
			Returns a list with tuples of the form (NODE, LEVEL), where
				NODE = The node in the AST
				LEVEL = The level in the AST where the node was found
		"""
		self.traverseDepthFirst()
		return self.nodes
			