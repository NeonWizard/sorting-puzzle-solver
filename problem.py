from state import State
from action import Action


class Problem:
    def __init__(self, initialState):
        self.initialState = initialState

    def goalTest(self, state):
        for vial in state.vials:
            if len(vial) == 0:
                continue
            if len(vial) != 4 or len(set(vial)) != 1:
                return False
        return True

    def actions(self, state):
        actions = []
        for i1, v1 in enumerate(state.vials):
            for i2, v2 in enumerate(state.vials):
                if i1 == i2:
                    continue  # can't act with self
                if len(v1) == 0:
                    continue  # can't move from empty vial
                if len(v2) == 4:
                    continue  # can't move into full vial
                if len(v2) != 0 and v2[-1] != v1[-1]:
                    continue  # not same color on top of vials

                actions.append(Action(i1, i2))
        return actions

    def result(self, state, action):
        vials = [list(x) for x in state.vials]
        bubble = vials[action.vial].pop()
        vials[action.vialDest].append(bubble)

        s2 = State(vials)

        return s2

    def heuristic(self, state):
        return state.heuristic()

    def printPath(self, endNode, verbose=True):
        solution = []
        node = endNode
        while node.state != self.initialState:
            solution.append(node)
            node = node.parent

        for node in solution[::-1]:
            print("= Step {} =".format(node.totalDepth))
            print(node.action)
            if verbose:
                print(node.state)
            print()


def main():
    state = State([[5, 5, 5], [4, 4, 4, 4], [5]])
    p = Problem(state)

    print([str(x) for x in p.actions(state)])


if __name__ == "__main__":
    main()
