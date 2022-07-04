import glob
import json
import math
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from config import DIR_RESULTS, PATH_METADATA_REF, DIR_FASTA, DIR_TEMP, PATH_METADATA_FASTA

dir_fasta: Path = DIR_FASTA
dir_truth: Path = DIR_FASTA
dir_results: Path = DIR_RESULTS / "0704"
dir_metadata_results: Path = dir_results / "_results.json"
path_metadata_fasta: Path = PATH_METADATA_FASTA
names_ref = sorted(list(set(json.load(open(PATH_METADATA_REF, "r")).keys())))
names_ref = [n.replace("_", " ") for n in names_ref]
rank = "species"


## cut and test names
# def _cut(path: str) -> dict:
#     print(path)
#     path2 = path.replace(".out", ".cut")
#     command = f"cut -f 2-3 {path} > {path2}"
#     os.system(command)
#
#
# Cut colums of out files
# def cut(path):
#     with Pool(cpu_count() * 2) as p:
#         p.map(_cut, glob.glob(str(path / "*.out"), recursive=True))


# def _test(x):
#     save = [n in x for n in names_ref]
#     x = x.replace("\t", "")
#     if any(save) and x.split("|")[3] == "scientific name":
#         return (names_ref[save.index(True)], x)
#     else:
#         return None
#
#
# Staring from node.dmp extract taxid|names of genomes of interest
# def test_names(path: str):
#     out = {n: [] for n in names_ref}
#     with open(path, "r") as fin, Pool(cpu_count() * 2) as p:
#         for o in p.map(_test, fin.readlines()):
#             if o:
#                 out[o[0]].append(o[1])
#
#     json.dump(out, open("out.json", "w"), indent=4)


def _evaluate(path) -> list:
    print(path)
    global rank
    fres: Path = path[0]
    ftruth: Path = path[1]
    temp = DIR_TEMP / f"{fres.stem}.eval"
    command = f"./evaluate nodes.dmp {rank} {fres} {ftruth} > {temp}"
    # get data
    os.system(command)

    with open(temp, "r") as resin:
        print(resin.readline())
        results: str = resin.readline()
        print(results)

    # process data
    results = results[:-1]

    tp, fp, fn, ok, no, tot, sens, prec, f1, pears = map(float, results.split("\t"))
    outdict = {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "ok": ok,
        "no": no,
        "tot": tot,
        "sens": sens,
        "prec": prec,
        "f1": f1,
        "pears": pears,
    }

    return [fres.stem, outdict]


# evaluate data
def evaluate():
    jsonData = {}
    res_truth_files = [[Path(a), dir_truth / f"{Path(a).stem}.truth"]
                       for a in sorted(glob.glob(f"{str(dir_results)}/*.cut"))
                       ]
    # truth_files = sorted([ for a in results_files])
    # files =list(zip(results_files, truth_files))
    with Pool(cpu_count() * 2) as p:
        for out in p.map(_evaluate, res_truth_files):
            jsonData[out[0]] = out[1]

    json.dump(jsonData, open(dir_metadata_results, "w"), indent=4)


def graph(show):
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    titles = {
        "tp": "TRUE POSITIVES",
        "fp": "FALSE POSITIVES",
        "fn": "FALSE NEGATIVES",
        "prec": "PRECISION",
        "f1": "F SCORE",
        "sens": "SENSITIVITY",
        "pears": "PEARSON CORRELATION",
        "ok": "OK",
        "no": "UNCLASSIFIED",
    }

    mtdt: dict = json.load(open(dir_metadata_results, "r"))
    for a in list(mtdt.keys()):
        if math.isnan(mtdt[a]["f1"]):
            del mtdt[a]
    xlabels: list[int] = sorted(list(map(int, mtdt.keys())))
    if show in ["tp", "fp", "fn", "ok", "no"]:
        mtdt_reads = json.load(open(path_metadata_fasta, "r"))
        Y = [k[show] / mtdt_reads[v]["nreads"] for v, k in mtdt.items()]
    else:
        Y = [a[show] for a in mtdt.values()]
    # t = Y.pop(2)
    # Y.insert(9, t)
    X = np.linspace(1, len(Y), len(Y))
    # Y=np.linspace(90,100,50)

    # fig, ax=plt.subplots(figsize=(9,7))
    fig, ax = plt.subplots()
    ax.set_xticks(range(1, len(X) + 1, 1), xlabels)
    if mtdt_reads:
        ax.set_ylim(min(Y) - .1, max(Y) + .1)
    else:
        ax.set_ylim(min(Y) * 0.9, max(Y) * 1.1)
    plt.bar(X, Y)
    plt.title(titles[show])
    plt.xlabel("reads length")
    plt.ylabel("")
    plt.xticks(rotation=90)

    fig.savefig(dir_results / f"{show}.jpg", bbox_inches="tight")


def count_reads(path: Path) -> int:
    try:
        with open(path, "r") as f:
            reads_metadata = f.read().count("\n")  # simlord
            return reads_metadata
    except:
        return 0


def graph_unclussified(show):
    import matplotlib.pyplot as plt
    import numpy as np

    # TODO change range
    xlabels = [str(x) for x in range(200, 1001, 100)]
    xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    titles = {"no": "UNCLASSIFIED"}

    norm = []
    for file in glob.glob("../fasta/fasta_50/**/*.truth"):
        print(file)
        norm.append(count_reads(file))
    t = norm.pop(1)
    t = norm.insert(9, t)

    data = json.load(open(DIR_RESULTS / "results.json", "r"))
    Y = [a[show] for a in data.values()]
    t = Y.pop(1)
    t = Y.insert(9, t)
    Y = np.array(Y)
    norm = np.array(norm)
    Y = Y / norm
    X = np.linspace(1, len(Y), len(Y))
    # Y=np.linspace(90,100,50)

    # fig, ax=plt.subplots(figsize=(9,7))
    fig, ax = plt.subplots()
    ax.set_xticks(range(1, 21, 1), xlabels)
    ax.set_ylim(min(Y) * 0.9, max(Y) * 1.1)
    plt.bar(X, Y)
    plt.title(titles[show])
    plt.xlabel("reads length")
    plt.ylabel("")
    plt.xticks(rotation=90)

    fig.savefig(dir_results / f"{show}.jpg", bbox_inches="tight")


if __name__ == "__main__":
    # evaluate()
    show = "tp"
    graph(show)
    show = "fn"
    graph(show)
    show = "prec"
    graph(show)
    show = "sens"
    graph(show)
    show = "f1"
    graph(show)
    show = "pears"
    graph(show)
    show = "ok"
    graph(show)
    show = "no"
    # graph_unclussified(show)
    # pass
