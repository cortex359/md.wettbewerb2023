import math
import sys
import matplotlib.pyplot as plt
import proplot as pplt
import numpy as np

from forest_types import Tree


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
    d_value = 1 - ((1/(total_trees * total_trees)) * d_value)
    b_value = a_value * d_value

    return b_value, a_value, d_value


def calc_table(forest_specs: str, forest_map: str):
    with open(f"{forest_specs}") as file:
        testcase = [line.removesuffix("\n") for line in file]

    global testcase_name
    testcase_name = testcase[0]
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

    b_value, a_value, d_value = calc_values_from_trees(trees, testcase_l * testcase_b)
    weight = float(forest_map.removesuffix(".txt").split(".w")[-1])
    print(f'w:{weight:1.3f} b:{b_value:10.8f} a:{a_value:10.8f} d:{d_value:10.8f}') #  {testcase_name}

    global weights, b_values, a_values, d_values
    weights.append(weight)
    b_values.append(b_value)
    a_values.append(a_value)
    d_values.append(d_value)

def plot_table(weights, b_values, a_values, d_values):
    b_max = max(b_values)
    a_max = max(a_values)
    d_max = max(d_values)

    b_max_pos = weights[b_values.index(b_max)]
    a_max_pos = weights[a_values.index(a_max)]
    d_max_pos = weights[d_values.index(d_max)]

    print(f'b_max: {b_max} at {b_max_pos}')
    print(f'a_max: {a_max} at {a_max_pos}')
    print(f'd_max: {d_max} at {d_max_pos}')

    fig, ax = plt.subplots()
    ax.plot(weights, b_values, linewidth=1.0, label=f'B-Value, max={b_max}', color='#ffaa55')
    ax.plot(weights, a_values, linewidth=1.0, label=f'A-Value, max={a_max}', color='#66aaff')
    ax.plot(weights, d_values, linewidth=1.0, label=f'D-Value, max={d_max}', color='#00bb00')
    ax.legend()

    #plt.axhline(y=b_max, color="black", linewidth=0.8, linestyle="-")
    #plt.axhline(y=a_max, color="black", linewidth=0.8, linestyle="-")
    #plt.axhline(y=d_max, color="black", linewidth=0.8, linestyle="-")

    plt.axvline(x=b_max_pos, color="#ffaa55", linewidth=1.5, linestyle="-")
    plt.axvline(x=a_max_pos, color="#66aaff", linewidth=1.5, linestyle="-")
    plt.axvline(x=d_max_pos, color="#00bb00", linewidth=1.5, linestyle="-")

    ax.set_xlabel('weight factor, step size: 0.001')
    ax.set_ylabel('score')
    ax.set_title(testcase_name)
    ax.set(xlim=(0, 2.0))
    plt.tight_layout()

    plt.show()

weights = []; b_values = []; a_values = []; d_values = []
testcase_name = ""

if __name__ == "__main__":
    if (len(sys.argv) >= 3):
        # score plot
        for fmap in sys.argv[2:]:
            calc_table(sys.argv[1], fmap)

plot_table(weights, b_values, a_values, d_values)