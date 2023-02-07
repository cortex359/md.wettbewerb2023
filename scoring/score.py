import math



class Tree:
	name: str = ""
	radius: float = 0.0
	index: int = 0
	counter: int = 0

	def __init__(self, name: str, radius: float, index: int):
		self.name = name
		self.radius = radius

	def count(self):
		self.counter += 1

	def __str__(self):
		return f'{self.name:15s} {self.radius:4.1f} {self.counter:8d}'


def calc_b(forest_file: str):
	with open(f"input_files/{forest_file}.txt") as file:
		testcase = [line.removesuffix("\n") for line in file]

	testcase_name = testcase[0]
	testcase_b = int(testcase[1].split()[0])
	testcase_l = int(testcase[1].split()[1])

	trees = []
	i = 0

	for l in testcase[2:]:
		trees.append(Tree(l.split()[1], float(l.split()[0]), i))
		i += 1

	with open(f"result_files/{forest_file}.txt.out") as file:
		forest = [line.removesuffix("\n") for line in file]

	for tree in forest:
		# x, y, size, flavor = tree.split()[0,1]
		flavor = int(tree.split()[3])
		trees[flavor].count()

	a_value = 0
	d_value = 0
	total_trees = 0

	for t in trees:
		# print(t)
		a_value += t.radius * t.radius * t.counter
		d_value += t.counter * t.counter
		total_trees += t.counter

	a_value *= math.pi
	a_value /= testcase_b * testcase_l

	d_value = 1 - ((1/(total_trees * total_trees)) * d_value)

	b_value = a_value * d_value

	#print(f'A = {a_value:10.8f}')
	#print(f'D = {d_value:10.8f}')
	print(f'B = {b_value:10.8f}')


testcases = [
	"forest01",
	"forest02",
	"forest03",
	"forest04",
	"forest05",
	"forest06",
	"forest07",
	"forest08",
	"forest09",
	"forest10"
]

for testf in testcases:
	calc_b(testf)