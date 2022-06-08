import glob
import os
from multiprocessing import Pool, cpu_count


def _cut(path):
    command = f"cut -f 2-3 {path} > {path.replace('.out', '.cut')}"
    os.system(command)


def cutfiles():
    with Pool(cpu_count()) as p:
        p.map(_cut, glob.glob("0606_nonames_as0603/**/*.out", recursive=True))


if __name__ == "__main__":
    cutfiles()
