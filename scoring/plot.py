import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
sys.path.extend(['/home/cthelen/Projekte/MatheDual/Wettbewerb2023/md.wettbewerb2023'])
from forest_types import Tree
from scoring import score


def plot_forest(forest_specs: str, forest_map: str):
	with open(forest_specs) as file:
		testcase = [line.removesuffix("\n") for line in file]

	testcase_name = testcase[0]
	testcase_b = int(testcase[1].split()[0])
	testcase_l = int(testcase[1].split()[1])

	trees = []
	i = 0

	for l in testcase[2:]:
		trees.append(Tree(l.split()[1], float(l.split()[0]), i))
		i += 1

	with open(forest_map) as file:
		forest = [line.removesuffix("\n") for line in file]

	px = 1/plt.rcParams['figure.dpi']  # pixel in inches
	fig, ax = plt.subplots(1, 1, figsize=(testcase_b*1.2*px, testcase_l*1.2*px))
	#fig, ax = plt.subplots(1, 1)

	colors = cm.gist_rainbow(np.linspace(0, 1, len(trees)))

	for tree in forest:
		x = float(tree.split()[0])
		y = float(tree.split()[1])
		r = float(tree.split()[2])
		flavor = int(tree.split()[3])
		trees[flavor].count()
		#ax.add_patch(plt.Circle((x, y), r, edgecolor=colors[flavor], fill=False))
		ax.add_patch(plt.Circle((x, y), r, facecolor=colors[flavor]))

	b_value, a_value, d_value = score.calc_values_from_trees(trees, testcase_l*testcase_b)

	ax.set_xlim(0, testcase_b)
	ax.set_ylim(0, testcase_l)

	ax.set_aspect('equal')
	ax.plot()

	plt.title(f'{testcase_name}, b={b_value:.7f}, a={a_value:.7f}, d={d_value:.7f}')
	#plt.show()

	print(f"Finished with {forest_file}.")
	fig.savefig(f"plots/{forest_file}.svg")


forest_file: str = ""
if len(sys.argv) == 2:
	forest_file = f'forest{sys.argv[1]}'
elif len(sys.argv) == 1:
	forest_file = "forest01"

if forest_file != "":
	forest_specs = f"input_files/{forest_file}.txt"
	forest_map = f"result_files/{forest_file}.txt"
elif len(sys.argv) == 3:
	forest_specs = sys.argv[1]
	forest_map = sys.argv[2]
else:
	print("ERROR")
	exit(1)

print(f"Plotting {forest_file} with\n  specs = {forest_specs}\n    map = {forest_map}")
plot_forest(forest_specs, forest_map)