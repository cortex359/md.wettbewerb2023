import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import Forest
import os

if len(sys.argv) >= 3:
    forest = sys.argv[1]
    teams = sys.argv[2:]
else:
    exit(1)

def approx_score(b: float) -> int:
    return int(round((11.0485842207 ** (1.02479492518 + 1.56922969137 * b)) + (0.382775141267 * 3309.20728729 ** b), 0))

def calc_team(team, forest):
    table_file = f'web/data/{team}/{team}.{forest}.table'

    with open(f"{table_file}") as file:
        table = [line.removesuffix("\n") for line in file if line.strip() != ""]

    map_name = table[0]
    map_size = float(table[1].split()[0]) * float(table[1].split()[1])

    trees = []
    for row in table[2:]:
        radius, tree, _, count = row.split()
        t = Forest.Tree(tree, float(radius))
        t.counter = int(count)
        trees.append(t)

    b_value, a_value, d_value = Forest.calc_values_from_trees(trees, map_size)
    return b_value, a_value, d_value, map_name
    #print(f'b:{b_value:16.14f} a:{a_value:16.14f} d:{d_value:16.14f} {map_name} ({team})')


results = []
for team in teams:
    b_value, a_value, d_value, map_name = calc_team(team, forest)
    #print(f'| {b_value:16.14f} | {a_value:16.14f} | {d_value:16.14f} | {map_name} | {team} |')
    results.append((b_value, a_value, d_value, team))

#bestIndx = [r[0] for r in results].index(max([r[0] for r in results]))
#b_value, a_value, d_value, team = results[bestIndx]

print(f"# {forest.capitalize()}: {map_name}\n")

print("|                b |                a |                d | score* | Team                  |")
print("|-----------------:|-----------------:|-----------------:|-------:|:----------------------|")

results.sort()
for r in results:
    b_value, a_value, d_value, team = r
    print(f'| {b_value:16.14f} | {a_value:16.14f} | {d_value:16.14f} | {approx_score(b_value):6d} | {team} |')

our_map = f'results/current_best/{forest}.txt.out'
our_specs = f'input/{forest}.txt'

b_our_best, a_our_best, d_our_best = Forest.calc_values_from_files(our_specs, our_map)

print(f'| {b_our_best:16.14f} | {a_our_best:16.14f} | {d_our_best:16.14f} | {approx_score(b_our_best):6d} | PI |')

if b_value > 0 and a_value > 0 and d_value > 0:
    print(f'| {(((b_our_best/b_value)-1)*100):15.11f}% | {(((a_our_best/a_value)-1)*100):15.11f}% | {(((d_our_best/d_value)-1)*100):15.11f}% | {(approx_score(b_our_best) - approx_score(b_value)):6d} | rel. diff to {team} |')
print(f'\n---\n')


exit(0)






weights = []; b_values = []; a_values = []; d_values = []
testcase_name = ""

if __name__ == "__main__":
    OUTPUT = "md-table"
    if (len(sys.argv) >= 3):
        # score plot
        for fmap in sys.argv[2:]:
            calc_table(sys.argv[1], fmap)

#plot_table(weights, b_values, a_values, d_values)