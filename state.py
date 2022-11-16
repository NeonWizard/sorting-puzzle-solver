import copy

# TODO: Replace vials with numpy arrays


class State:
    def __init__(self, vials):
        self.vials = tuple([tuple(x) for x in copy.deepcopy(vials)])
        self._heuristic = None
        self._hash = None

    # - display function
    def __str__(self):
        out = ""
        for i, vial in enumerate(self.vials):
            out += "Vial {}: {}".format(i+1,
                                        "|".join([str(x) for x in vial])) + "\n"

        return out.rstrip("\n")

    # - heuristics
    def __lt__(self, rhs):
        return self.heuristic() < rhs.heuristic()

    def __eq__(self, rhs):
        return self.vials == rhs.vials

    def __hash__(self):
        if self._hash == None:
            self._hash = hash(self.vials)
        return self._hash

    def heuristic(self):
        if self._heuristic:
            return self._heuristic

        self._heuristic = 0
        # each vial's score is the amount of nonmatching colors
        for vial in self.vials:
            self._heuristic += len(set(vial)) - 1
        return self._heuristic


def main():
    s = State([[3, 3, 3, 3]])
    print(s)
    print(s.heuristic())


if __name__ == "__main__":
    main()
