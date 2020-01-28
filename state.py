import config
import copy

class State:
	def __init__(self, vials):
		self.vials = copy.deepcopy(vials)

	# - display function
	def __str__(self):
		out = ""
		for i, vial in enumerate(self.vials):
			out += "Vial {}: {}".format(i+1, "|".join(config.colorMap[x] for x in vial)) + "\n"
		return out.rstrip("\n")

	def __eq__(self, rhs):
		return self.vials == rhs.vials

	def heuristic(self):
		val = 0
		for vial in self.vials:
			val += len(set(vial)) - 1
		return val


def main():
	s = State([[3, 3, 3, 3]])
	print(s)
	print(s.heuristic())

if __name__ == "__main__":
	main()