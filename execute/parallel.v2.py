from datetime import datetime
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

SCRIPT = "parallel-v2"
SOLVER = "solver.vs8.randomSeed"
PROCESS_COUNT = 20
VERSION = 3


def computePoints(id: int, file: str, weights):
    results = []

    index = id * (len(weights) // PROCESS_COUNT)
    end_index = index + (len(weights) // PROCESS_COUNT)

    while index < end_index:
        weighting, seed = weights[index]
        seed += 1000000
        p = subprocess.Popen([f"bin/{SOLVER}.run", file, f"{weighting:10.8f}", str(seed)],
                             stdout=subprocess.PIPE)

        output = str(p.communicate()[0])
        if output == None: break
        # c:0.839973 b:0.671978 a:0.851215 d:0.789434 seed:1000004 w:1 cs:441 it:441
        m = re.match("b'c:([0-9.]+)\s+b:([0-9.]+).*", output)

        results.append([weighting, seed, *m.groups()])
        results = list(list(float(n) for n in t) for t in results)

        with cnt.get_lock():
            cnt.value += 1
            print(f'{cnt.value:6d} w:{weighting:10.8f} seed:{seed} c:{float(m.group(1)):8.6f} b:{float(m.group(2)):8.6f}')

        index += 1

    return results


def init_globals(counter):
    global cnt
    cnt = counter

def plot(seed, weighting, b):
    maxB = max(b)
    maxSeed = seed[b.index(maxB)]
    maxWeighting = weighting[b.index(maxB)]

    # 3D Plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Add x, y gridlines
    ax.grid(visible=True, color='grey',
          linestyle='-.', linewidth=0.3,
          alpha=0.2)

    sctt = ax.scatter3D(seed, weighting, b,
          alpha=0.8,
          c=c,
          cmap=plt.get_cmap('Spectral'),
          marker='o')

    ax.scatter(maxSeed, maxWeighting, maxB, marker='^')

    ax.set_xlabel('seed', fontweight='bold')
    ax.set_ylabel('weighting', fontweight='bold')
    ax.set_zlabel('B Score', fontweight='bold')
    fig.colorbar(sctt, ax=ax, shrink=0.5, aspect=5)

    # plt.plot(maxWre, maxB, ".r", label="RE max")
    # plt.plot(maxWce, maxB, ".r", label="CE max")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("3d-plot.py [in_file] [samples] [weighting_range] [seed_range]")
        name = "forest01"
        total_sample_size = 1000
        weight_start, weight_end = (0., 2.)
        seed_start, seed_end = (1, 100)
    else:
        name = sys.argv[1]
        total_sample_size = int(sys.argv[2])
        weight_start, weight_end = map(float, sys.argv[3].split(","))
        seed_start, seed_end = map(int, sys.argv[4].split(","))

    re_int = weight_end - weight_start
    seed_range = seed_end - seed_start

    w_range = np.linspace(weight_start, weight_end, int(total_sample_size / seed_range))

    weights = [(r, c) for r in w_range for c in range(seed_start, seed_end + 1)]
    random.shuffle(weights)

    inputPath = f"../input/{name}.txt"
    if not os.path.isfile(inputPath):
        print("Failed to find input-file")
        exit(1)
    if total_sample_size < 100:
        print("Count must at least be 100")
        exit(1)
    if total_sample_size < PROCESS_COUNT:
        PROCESS_COUNT = total_sample_size

    path_to_logfile = f"logs/{name}.log"
    startTime = time.perf_counter_ns()
    start_time = datetime.now()

    with open(path_to_logfile, "a") as logfile:
        logfile.write(f"{start_time} === Run started ===\n")
        logfile.write(f"== script={SCRIPT} solver={SOLVER} threads={PROCESS_COUNT}\n")
        logfile.write(f"== name={name} total_sample_size={total_sample_size} seed_start={seed_start} seed_end={seed_end} weight_start={weight_start} weight_end={weight_end}\n")

    if not os.path.isfile(path_to_logfile):
        print("Failed to create logfile")
        exit(1)

    cnt = Value("i", 0)

    with Pool(initializer=init_globals, initargs=(cnt,)) as p:
        r = p.starmap(computePoints, [(i, inputPath, weights) for i in range(PROCESS_COUNT)])

    endTime = time.perf_counter_ns()

    print(f'---------------------------------------------')
    print(f'---> {inputPath}')
    print(f"Finished after {(endTime - startTime) / 1E9}s")

    r = [i for s in r for i in s]
    weighting = [o[0] for o in r]
    seed = [o[1] for o in r]
    c = [o[2] for o in r]
    b = [o[3] for o in r]

    maxB = max(b)
    maxSeed = seed[b.index(maxB)]
    maxWeighting = weighting[b.index(maxB)]

    end_time = datetime.now()

    print(f"\nMaximum:")
    print(f"b:{maxB} weight:{maxWeighting:10.8f} seed:{maxSeed} forest:{name}\n")

    with open(path_to_logfile, "a") as logfile:
        logfile.write(f"-> b:{maxB} weight:{maxWeighting:10.8f} seed:{maxSeed} not saved!\n")
        logfile.write(f"== Runtime of {end_time-start_time} [H:M:S] for {total_sample_size} runs\n")
        logfile.write(f"==          {(end_time-start_time).total_seconds() / total_sample_size} seconds/run\n")
        logfile.write(f"{end_time} === Run ended ===\n")
