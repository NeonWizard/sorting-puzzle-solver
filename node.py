class Node:
	def __init__(self, state, parent, action, totalDepth, heuristic):
		self.state = state
		self.parent = parent
		self.action = action
		self.totalDepth = totalDepth
		self.heuristic = heuristic

		self.children = []

	def addChild(self, node):
		self.children.append(node)
	def removeChild(self, node):
		self.children.remove(node)

	def getChildCount(self):
		return len(self.children)