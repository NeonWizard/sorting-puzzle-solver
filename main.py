from state import State
from problem import Problem
import frontiers
from algorithms import *

import machinevision

import time

# TODO: add command line arguments for frontier, vial count, etc


def solve(puzzle, algorithm, frontier, verbose=True):
    state = State(puzzle)  # initial state
    problem = Problem(state)

    frontier = frontier()
    algorithm = algorithm(problem, frontier)

    startTime = time.time()
    result = algorithm.search()
    endTime = time.time()

    print()
    problem.printPath(result, verbose)
    print()

    print("Path cost:\t\t{}".format(result.totalDepth if result else -1))
    print("Nodes generated:\t{}".format(algorithm.numNodesGenerated))
    print("Max nodes stored:\t{}".format(algorithm.maxNodesStored))
    print("Time elapsed:\t\t{} seconds".format(round(endTime-startTime, 3)))
    print()


def main():
    print("== Tired of using your brain to solve puzzles? Look no further. ==")
    print()

    print("Would you like to load the puzzle from a file?")
    filename = input(
        "Type a filename, or leave blank to continue to manual input: ")
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

    while True:
        inp = input("Verbose solution? (Y/N): ").lower()
        if inp == "y":
            verbose = True
            break
        elif inp == "n":
            verbose = False
            break
        else:
            print("Invalid option. Please try again.")
    print()

    if not (filename.isspace() or filename == ""):
        puzzle = machinevision.simplify_vials(
            machinevision.get_vials(filename))
    else:
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
            for key in verifyMap:
                if verifyMap[key] != 4:
                    print("There are {} {} bubbles.".format(
                        verifyMap[key], key))
            return
        print()

    puzzle += [[], []]  # add empty vials

    print("Solving...")
    print()
    solve(puzzle, Graph, frontier, verbose)


if __name__ == "__main__":
    main()
