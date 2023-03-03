import math


class Tree:
    name: str = ""
    radius: float = 0.0
    index: int = 0
    counter: int = 0

    def __init__(self, name: str, radius: float, index: int = 0):
        self.name = name
        self.radius = radius

    def count(self):
        self.counter += 1

    def __str__(self):
        return f'{self.name:15s} {self.radius:4.1f} {self.counter:8d}'


def calc_values_from_trees(trees: [Tree], mapsize: int):
    a_value = 0
    d_value = 0
    total_trees = 0

    for t in trees:
        a_value += t.radius * t.radius * t.counter
        d_value += t.counter * t.counter
        total_trees += t.counter

    a_value *= math.pi
    a_value /= mapsize
    d_value = 1 - ((1 / (total_trees * total_trees)) * d_value)
    b_value = a_value * d_value

    return b_value, a_value, d_value


def calc_values_from_files(forest_specs: str, forest_map: str):
    with open(f"{forest_specs}") as file:
        testcase = [line.removesuffix("\n") for line in file]

    testcase_b = int(testcase[1].split()[0])
    testcase_l = int(testcase[1].split()[1])

    trees = []
    i = 0

    for l in testcase[2:]:
        trees.append(Tree(l.split()[1], float(l.split()[0]), i))
        i += 1

    with open(f"{forest_map}") as file:
        forest = [line.removesuffix("\n") for line in file]

    for tree in forest:
        flavor = int(tree.split()[3])
        trees[flavor].count()

    return calc_values_from_trees(trees, testcase_l * testcase_b)
