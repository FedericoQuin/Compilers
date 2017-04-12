
from AST.AST import AST
from AST.ASTNode import *

class ASTWalker:
	def __init__(self, ast):
		self.nodes = []
		self.AST = ast

	def traverseDepthFirst(self):
		queue = []
		queue.append(self.AST.root)

		while (len(queue) != 0):
			currentNode = queue.pop(0)
			for node in reversed(currentNode.children):
				queue.insert(0,node)
			self.nodes.append(currentNode)

	def getNodesDepthFirst(self):
		self.traverseDepthFirst()
		return self.nodes
			