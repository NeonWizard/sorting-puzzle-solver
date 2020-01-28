import bisect

class DFFrontier:
	def __init__(self):
		self._arr = []

	def insert(self, node_in):
		self._arr.append(node_in)
	def remove(self):
		return self._arr.pop()

	def empty(self):
		return len(self._arr) == 0

	def size(self):
		return len(self._arr)

class BFFrontier:
	def __init__(self):
		self._arr = []

	def insert(self, node_in):
		self._arr.append(node_in)
	def remove(self):
		return self._arr.pop(0)

	def empty(self):
		return len(self._arr) == 0

	def size(self):
		return len(self._arr)

class HFFrontier:
	def __init__(self):
		self._arr = []

	def insert(self, node_in):
		bisect.insort(self._arr, node_in)
	def remove(self):
		return self._arr.pop(0)

	def empty(self):
		return len(self._arr) == 0

	def size(self):
		return len(self._arr)