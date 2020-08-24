from state import State
from problem import Problem

import frontiers
from algorithms import *

import time

def solve(puzzle, algorithm, frontier):
	state = State(puzzle) # initial state
	problem = Problem(state)

	frontier = frontier()
	algorithm = algorithm(problem, frontier)

	startTime = time.time()
	result = algorithm.search()
	endTime = time.time()

	print()
	problem.printPath(result)
	print()

	print("Path cost:\t\t{}".format(result.totalDepth if result else -1))
	print("Nodes generated:\t{}".format(algorithm.numNodesGenerated))
	print("Max nodes stored:\t{}".format(algorithm.maxNodesStored))
	print("Time elapsed:\t\t{} seconds".format(round(endTime-startTime, 3)))
	print()

def main():
	print("== Tired of using your brain to solve puzzles? Look no further. ==")
	print()

	print("Which frontier?")
	print("\tDFF - Depth First")
	print("\tBFF - Breadth First")
	print("\tHF - Heuristic")
	frontierStr = input(">>> ").lower()
	if (frontierStr == "dff"):
		frontier = frontiers.DFFrontier
	elif (frontierStr == "bff"):
		frontier = frontiers.BFFrontier
	elif (frontierStr == "hf"):
		frontier = frontiers.HFrontier
	else:
		print("Invalid frontier option.")
		return
	print()

	vials = int(input("How many vials (excluding 2 empty): "))
	print()

	print("Type colors (space separated) from top of vial to bottom.")
	print()
	puzzle = []
	verifyMap = {}
	i = 0
	while i < vials:
		inp = input("Vial {} contents: ".format(i+1)).split()[::-1]
		if len(inp) != 4:
			print("Vial must contain 4 elements!")
			continue

		for x in inp:
			verifyMap[x] = verifyMap.get(x, 0) + 1

		puzzle.append(inp)
		i += 1

	if not all([x == 4 for x in verifyMap.values()]):
		print("Puzzle state is not valid.")
		return

	puzzle += [[], []] # add empty vials

	solve(puzzle, Graph, frontier)

if __name__ == "__main__":
	main()