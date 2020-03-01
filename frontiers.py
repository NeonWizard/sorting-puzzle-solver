import bisect
from abc import ABC, abstractmethod

class Frontier(ABC):
	@abstractmethod
	def insert(self, node_in):
		pass
	@abstractmethod
	def remove(self):
		pass

	@abstractmethod
	def empty(self):
		pass

	@abstractmethod
	def size(self):
		pass

# ========================

class DFFrontier(Frontier):
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

class BFFrontier(Frontier):
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

class HFFrontier(Frontier):
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


def main():
	hff = HFFrontier()
	print(hff.empty())

if __name__ == "__main__":
	main()