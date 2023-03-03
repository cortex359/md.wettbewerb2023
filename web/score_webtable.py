import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import Forest
import os

if len(sys.argv) == 2:
    forest = sys.argv[1]
else:
    forest = 'forest02'

table_file = f'/home/cthelen/Projekte/MatheDual/Wettbewerb2023/md.wettbewerb2023/web/data/uka/uka.{forest}.table'

our_map = f'/home/cthelen/Projekte/MatheDual/Wettbewerb2023/md.wettbewerb2023/results/current_best/{forest}.txt.out'
our_specs = f'/home/cthelen/Projekte/MatheDual/Wettbewerb2023/pi/input_files/{forest}.txt'

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
    # print(tree, count)

b_value, a_value, d_value = Forest.calc_values_from_trees(trees, map_size)
print(f'b:{b_value:16.14f} a:{a_value:16.14f} d:{d_value:16.14f} {map_name} (koeln)')

b_our_best, a_our_best, d_our_best = Forest.calc_values_from_files(our_specs, our_map)

print(f'b:{b_our_best:16.14f} a:{a_our_best:16.14f} d:{d_our_best:16.14f} {map_name} (pi)')

if b_value > 0 and a_value > 0 and d_value > 0:
    print(f'b:{(((b_our_best/b_value)-1)*100):15.11f}% a:{(((a_our_best/a_value)-1)*100):15.11f}% d:{(((d_our_best/d_value)-1)*100):15.11f}% {map_name} (relative diff.)')
print(f'---\n')



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