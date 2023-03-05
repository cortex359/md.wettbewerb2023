import sys
import os
import subprocess
import re
from multiprocessing import Pool, Value
from datetime import datetime
import numpy as np
import time

SCRIPT = "parallel-v1"
SOLVER = "solver.vs7.non-det"
PROCESS_COUNT = 20
RESULTS = "../pi-cpp_vs.7/results" # path to dir in which a sub dir will be used to save result files into

def computePoints(id: int, file: str, start: float, end: float, count: int):
    results = []

    totalSize = end - start
    part = totalSize / PROCESS_COUNT
    step = totalSize / count

    weight = start + part * id
    partEnd = start + part * (id + 1)
    while weight < partEnd:
        result_file = f"{RESULTS}/{file}/{file}.w{weight:10.8f}.txt"
        p = subprocess.Popen([f"bin/{SOLVER}.run", f"../input/{file}.txt", result_file, f"{weight:10.8f}"],
                             stdout=subprocess.PIPE)
        output = str(p.communicate()[0])
        if output == None: break
        m = re.match("b'c:([0-9.]+)\s+b:([0-9.]+).*", output)

        results.append([weight, *m.groups()])
        results = list(list(float(n) for n in t) for t in results)

        with cnt.get_lock():
            cnt.value += 1
            # print(cnt.value, float(f"{weight:8.6f}"), m.group(2))
            print(
                f"b:{float(m.group(2)):8.6f} w:{weight:10.8f} run:{cnt.value} saved:{'/'.join(result_file.split('/')[-2:])}")

        weight += step

    return results


def init_globals(counter):
    global cnt
    cnt = counter


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("parallel.py [in_file] [samples] [start_weight] [start_weight]")
        name = "forest01"
        count = 1000
        start, end = (0., 2.)
    else:
        name = sys.argv[1]
        count = int(sys.argv[2])
        start = float(sys.argv[3])
        end = float(sys.argv[4])

    inputPath = f"../input/{name}.txt"
    if not os.path.isfile(inputPath):
        print("Failed to find input-file")
        exit(1)
    if not os.path.isdir(f"{RESULTS}/{name}/"):
        print(f"dir '{RESULTS}/{name}' must exist")
        exit(1)
    if count < 1:
        print("Count must at least be 1")
        exit(1)
    if count < PROCESS_COUNT:
        PROCESS_COUNT = count
    if start > end:
        print("Start must be less than end")
        exit(1)
    elif not (0 <= start <= 2 and 0 <= end <= 2):
        print("Start and End cant be less than zero or greater than 2")
        exit(1)

    path_to_logfile = f"logs/{name}.log"
    start_time = datetime.now()

    with open(path_to_logfile, "a") as logfile:
        logfile.write(f"{start_time} === Run started ===\n")
        logfile.write(f"== script={SCRIPT} solver={SOLVER} threads={PROCESS_COUNT}\n")
        logfile.write(f"== name={name} count={count} start={start} end={end}\n")

    if not os.path.isfile(path_to_logfile):
        print("Failed to create logfile")
        exit(1)

    cnt = Value("i", 0)

    with Pool(initializer=init_globals, initargs=(cnt,)) as p:
        r = p.starmap(computePoints, [(i, name, start, end, count) for i in range(PROCESS_COUNT)])

    r = [i for s in r for i in s]
    weight = [o[0] for o in r]
    c = [o[1] for o in r]
    b = [o[2] for o in r]

    maxB = max(b)
    maxC = c[b.index(maxB)]
    maxWeight = weight[b.index(maxB)]

    end_time = datetime.now()

    print(f"\nMaximum:")
    print(f"b:{maxB} weight:{maxWeight:10.8f} saved at {RESULTS}/{name}/{name}.w{maxWeight:10.8f}.txt")

    with open(path_to_logfile, "a") as logfile:
        logfile.write(f"-> b:{maxB} weight:{maxWeight:10.8f} saved at {name}/{name}.w{maxWeight:10.8f}.txt\n")
        logfile.write(f"== Runtime of {end_time-start_time} [H:M:S] for {count} runs\n")
        logfile.write(f"==          {(end_time-start_time).total_seconds() / count} seconds/run\n")
        logfile.write(f"{end_time} === Run ended ===\n")
