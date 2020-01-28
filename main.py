from state import State
from problem import Problem

from frontiers import *
from algorithms import *

import config

def solve(puzzle, algorithm, frontier):
	state = State(puzzle) # initial state
	problem = Problem(state)
	
	frontier = frontier()
	algorithm = algorithm(problem, frontier)

	result = algorithm.search()
	print()
	problem.printPath(result)
	print()
	if (result):
		print("Path cost:\t\t{}".format(result.totalDepth))
		print("Nodes generated:\t{}".format(algorithm.numNodesGenerated))
		print("Nodes stored:\t\t{}".format(algorithm.maxNodesStored))
	else:
		print("Path cost:\t\t{}".format(-1))
		print("Nodes generated:\t{}".format(algorithm.numNodesGenerated))
		print("Nodes stored:\t\t{}".format(algorithm.maxNodesStored))

	print()

def main():
	print("== Tired of using your brain to solve puzzles? Look no further. ==")
	print()

	print("Currently supported colors:")
	for x in config.colorMap:
		if (type(x) != str): continue
		print("\t- {}".format(x))
	print()

	vials = int(input("How many vials: "))
	print()

	print("Please be sure to consult the above color map, and type")
	print("colors (space separated) from bottom of vial to top.")
	print()
	puzzle = []
	i = 0
	while i < vials:
		inp = input("Vial {} contents: ".format(i+1)).split()
		if len(inp) != 4:
			print("Vial must contain 4 elements!")
			continue

		puzzle.append([config.colorMap[x.lower()] for x in inp])
		i += 1

	puzzle += [[], []]

	solve(puzzle, Graph, BFFrontier)

if __name__ == "__main__":
	main()