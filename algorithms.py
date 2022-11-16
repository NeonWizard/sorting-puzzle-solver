from node import Node


class Graph:
    def __init__(self, problem, frontier):
        self.problem = problem
        self.frontier = frontier

        self.numNodesGenerated = 0
        self.maxNodesStored = 0

        self.closed = set()

    def search(self):
        self.numNodesGenerated = 0
        self.maxNodesStored = 0

        problem = self.problem

        root = Node(problem.initialState, None, 0, 0,
                    problem.heuristic(problem.initialState))
        self.frontier.insert(root)
        self.closed = set()

        while (not self.frontier.empty()):
            node = self.frontier.remove()
            if (node.state in self.closed):
                continue

            # print()
            # if node.parent != None: print(str(node.parent.state))
            # print(str(node.action))
            # print(str(node.state))
            # input()

            print("\r", end="")
            print(f"Nodes generated: {self.numNodesGenerated}; ", end="")
            print(f"Frontier size: {self.frontier.size()}; ", end="")
            print(f"Current heuristic: {node.heuristic}", end="")

            s1 = node.state
            if (problem.goalTest(s1)):
                return node

            self.closed.add(node.state)
            actions = problem.actions(s1)
            for action in actions:
                s2 = problem.result(s1, action)
                if (s2 in self.closed):
                    continue

                new_node = Node(s2, node, action,
                                node.totalDepth + 1, problem.heuristic(s2))

                self.frontier.insert(new_node)
                node.addChild(new_node)

                self.numNodesGenerated += 1
                self.maxNodesStored = max(self.maxNodesStored, len(
                    self.closed) + self.frontier.size())

        return False
