import math
import random
import sys
import os
import subprocess
import re
from multiprocessing import Pool, Value
import matplotlib.pyplot as plt
import numpy as np
import time

PROCESS_COUNT = 8
VERSION = 2

if VERSION == 2:
	SOLVER_BINARY = "/home/cthelen/Projekte/MatheDual/Wettbewerb2023/pi-cpp/inputs/Solver_weight_Release"
elif VERSION == 1:
	SOLVER_BINARY = "/home/cthelen/Projekte/MatheDual/Wettbewerb2023/pi-cpp/inputs/Solver_Release"


def computePoints(id: int, file: str, weights):
	results = []

	index = id * (len(weights) // PROCESS_COUNT)
	end_index = index + (len(weights) // PROCESS_COUNT)

	while index < end_index:
		_wre, _wce = weights[index]
		p = subprocess.Popen([SOLVER_BINARY, file, str(_wre), str(_wce)], stdout=subprocess.PIPE)

		if VERSION == 2:
			output = str(p.communicate()[0])
			if output == None: break
			# c:0.850105  b:0.680084  a:0.862289  d:0.788696  wre:0.602  wce:1.96  cs:128  it:614
			# m = re.match("b'c:([0-9.]+)\s+b:([0-9.]+)\s+a:([0-9.]+)\s+d:([0-9.]+)\s+wre:([0-9.]+)\s+wce:([0-9.]+)\s+cs:([0-9]+)\s+it:([0-9]+).*", output)
			m = re.match("b'c:([0-9.]+)\s+b:([0-9.]+).*", output)

		if VERSION == 1:
			output = str(p.communicate()[0]).split("\\n")[-4]
			if output == None: break
			m = re.match("Max: (\d*\.\d*) = (\d*\.\d*) \* (\d*\.\d*) .*", output)

		results.append([_wre, _wce, *m.groups()])
		results = list(list(float(n) for n in t) for t in results)

		with cnt.get_lock():
			cnt.value += 1
			print(f'{cnt.value:6d} wre:{_wre:8.6f} wce:{_wce:8.6f} c:{float(m.group(1)):8.6f} b:{float(m.group(2)):8.6f}')

		index += 1

	return results


def init_globals(counter):
	global cnt
	cnt = counter


if __name__ == "__main__":
	if len(sys.argv) != 5:
		print("paralell.py [in_file] [samples] [re_range] [ce_range]")
		in_file = "input_files/forest01.txt"
		total_sample_size = 1000
		re_start, re_end = (0., 2.)
		ce_start, ce_end = (0., 5.)
	else:
		in_file = sys.argv[1]
		total_sample_size = int(sys.argv[2])
		re_start, re_end = map(float, sys.argv[3].split(","))
		ce_start, ce_end = map(float, sys.argv[4].split(","))

	re_int = re_end - re_start
	ce_int = ce_end - ce_start
	i = int(math.ceil(math.sqrt(total_sample_size / (ce_int * re_int))))

	re_weights = np.linspace(re_start, re_end, int(re_int * i))
	ce_weights = np.linspace(ce_start, ce_end, int(ce_int * i))

	weights = [(r, c) for r in re_weights for c in ce_weights]
	random.shuffle(weights)

	if not os.path.isfile(in_file):
		print("Failed to find input-file")
		exit(1)
	if total_sample_size < 100:
		print("Count must at least be 100")
		exit(1)

	startTime = time.perf_counter_ns()

	cnt = Value("i", 0)

	with Pool(initializer=init_globals, initargs=(cnt,)) as p:
		r = p.starmap(computePoints, [(i, in_file, weights) for i in range(PROCESS_COUNT)])

	endTime = time.perf_counter_ns()

	print(f'---------------------------------------------')
	print(f'---> {in_file}')
	print(f"Finished after {(endTime - startTime) / 1E9}s")

	r = [i for s in r for i in s]
	wre = [o[0] for o in r]

	if VERSION == 1:
		b = [o[1] for o in r]

	if VERSION == 2:
		wce = [o[1] for o in r]
		c = [o[2] for o in r]
		b = [o[3] for o in r]

	maxB = max(b)
	maxWre = wre[b.index(maxB)]
	maxWce = wce[b.index(maxB)]

	print(f'Maximum b:{maxB} with wre:{maxWre} and wce:{maxWce}')

	# plt.plot(wre, wce, ".", color="orange", label="B", linewidth=0.2)
	# plt.plot(wce, b, ".", color="yellow", label="C", linewidth=0.2)

	# 3D Plot
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')

	# Add x, y gridlines
	ax.grid(visible=True, color='grey',
			linestyle='-.', linewidth=0.3,
			alpha=0.2)

	sctt = ax.scatter3D(wce, wre, b,
			alpha=0.8,
			c=c,
			cmap=plt.get_cmap('Spectral'),
			marker='o')

	ax.scatter(maxWce, maxWre, maxB, marker='^')

	ax.set_xlabel('WCE', fontweight='bold')
	ax.set_ylabel('WRE', fontweight='bold')
	ax.set_zlabel('B Score', fontweight='bold')
	fig.colorbar(sctt, ax=ax, shrink=0.5, aspect=5)

	# plt.plot(maxWre, maxB, ".r", label="RE max")
	# plt.plot(maxWce, maxB, ".r", label="CE max")
	plt.show()
