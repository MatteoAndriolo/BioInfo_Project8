import glob
import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from config import DIR_TEMP, ROOT_DIR


# dir_fasta: Path = DIR_FASTA
# dir_fasta_simlord: Path = ROOT_DIR / "0607/fasta"
# dir_truth: Path = DIR_FASTA
# dir_results: Path = DIR_RESULTS / "0704"
# dir_results_simlord: Path =
# dir_results_mason: Path = DIR_RESULTS / "0704"
# pathOutResults: Path = DIR_RESULTS / "0706_hybrid"
# pathOutResults.mkdir(exist_ok=True, parents=True)
# dir_metadata_results: Path = pathOutResults / "_results.json"
# path_metadata_fasta: Path = PATH_METADATA_FASTA
# names_ref = sorted(list(set(json.load(open(PATH_METADATA_REF, "r")).keys())))
# names_ref = [n.replace("_", " ") for n in names_ref]


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
    print("START", path)
    global rank
    fres: Path = path[0]
    ftruth: Path = path[1]
    temp = DIR_TEMP / f"{fres.stem}.eval"
    command = f"./newevaluate nodes.dmp {rank} {ftruth} {fres} > {temp}"
    print(command)
    # get data
    os.system(command)

    with open(temp, "r") as resin:
        results: str = resin.readline()
        print(results)

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
    print(outdict)
    return [fres.stem, outdict]


# evaluate data
def evaluate(dir_truth: Path, dir_results: Path, dir_output: Path) -> dict:
    '''
    Evaluete kraken2 results
    :param dir_truth: directory containing truth file
    :param dir_results: directory containing kraken2 results
    :return: json dictionary with results
    '''
    jsonData = {}
    res_truth_files = [[Path(a), dir_truth / f"{Path(a).stem}.truth"]
                       for a in sorted(glob.glob(f"{str(dir_results)}/*.cut"))
                       ]
    # truth_files = sorted([ for a in results_files])
    # files =list(zip(results_files, truth_files))
    print(res_truth_files)
    # with Pool(cpu_count() * 2) as p:
    with Pool(cpu_count() * 2) as p:
        for out in p.map(_evaluate, res_truth_files):
            print("dictionary")
            jsonData[out[0]] = out[1]

    json.dump(jsonData, open(dir_output / "_metadata.json", "w"), indent=4)
    return jsonData


def graph(dir_results: Path, show: str):
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    titles = {
        "tp": "TRUE POSITIVES",
        "fp": "FALSE POSITIVES",
        "fn": "FALSE NEGATIVES",
        "prec": "PRECISION",
        "f1": "F-SCORE",
        "sens": "SENSITIVITY",
        "pears": "PEARSON CORRELATION",
        "ok": "VAGUE POSITIVES",
        "no": "UNCLASSIFIED",
    }

    mtdt_fasta_low: dict = json.load(open(ROOT_DIR / "fasta/fasta_50_0704/_metadata.json", "r"))
    mtdt_fasta_high: dict = json.load(open(ROOT_DIR / "0607/fasta/_metadata.json", "r"))
    mtdt_results_low: dict = json.load(open(dir_out_low / "_metadata.json", "r"))
    mtdt_results_lowgenus: dict = json.load(open(dir_out_genus_low / "_metadata.json", "r"))
    mtdt_results_high: dict = json.load(open(dir_out_high / "_metadata.json", "r"))
    mtdt_results_highgenus: dict = json.load(open(dir_out_genus_high / "_metadata.json", "r"))
    for i in [100, 200, 300, 400, 500, 600, 700, 800, 900, 999]:
        name = f"{i:0>6}"
        mtdt_fasta_high[name] = mtdt_fasta_low[name]
        mtdt_results_high[name] = mtdt_results_low[name]
        mtdt_results_highgenus[name] = mtdt_results_low[name]

    # for a in list(mtdt_results_low.keys()):
    #     if math.isnan(mtdt_results_low[a]["f1"]):
    #         del mtdt_results_low[a]
    #     if math.isnan(mtdt_results_lowgenus[a]["f1"]):
    #         del mtdt_results_lowgenus[a]
    #     if math.isnan(mtdt_results_high[a]["f1"]):
    #         del mtdt_results_high[a]
    #     if math.isnan(mtdt_results_high[a]["f1"]):
    #         del mtdt_results_highgenus[a]

    xlabels: list[int] = sorted(list(map(int, mtdt_results_low.keys())))
    if 999 in xlabels:
        xlabels[xlabels.index(999)] = 1000
    if 1001 in xlabels:
        xlabels[xlabels.index(1001)] = 1000

    if show in ["tp", "fp", "fn", "ok", "no"]:
        Y_low = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in list(sorted(mtdt_results_low.items(),key=lambda x:x[0]))]
        Y_lowgenus = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in list(sorted(mtdt_results_lowgenus.items(),key=lambda x:x[0]))]
        Y_high = [mtdt_results_high[k][show] / mtdt_fasta_high[k]['nreads'] for k in
                  list(sorted(mtdt_results_high.keys()))]
        Y_highgenus = [mtdt_results_highgenus[k][show] / mtdt_fasta_high[k]['nreads'] for k in
                       list(sorted(mtdt_results_high.keys()))]
    else:
        Y_low = [k[show] for v, k in mtdt_results_low.items()]
        Y_lowgenus = [k[show] for v, k in mtdt_results_lowgenus.items()]
        Y_high = [mtdt_results_high[k][show] for k in list(sorted(mtdt_results_high.keys()))]
        Y_highgenus = [mtdt_results_highgenus[k][show] for k in list(sorted(mtdt_results_highgenus.keys()))]

    print(mtdt_results_low)
    print(mtdt_results_high)
    X = np.linspace(1, len(Y_high), len(Y_high))

    # fig, ax=plt.subplots(figsize=(9,7))
    # allYvalues = Y_low + Y_high + Y_highgenus + Y_lowgenus
    allYvalues = Y_high + Y_highgenus
    fig, ax = plt.subplots()
    ax.set_xticks(range(1, len(X) + 1, 1), xlabels)
    if show in ["prec", "sens", "f1", ]:
        ax.set_ylim(max(0, min(allYvalues) - .1), max(allYvalues) + .1)
        plt.ylabel("score")
    elif show in ["pears"]:
        ax.set_ylim(max(0, min(allYvalues) * 0.9), max(allYvalues) * 1.1)
        plt.ylabel("coefficent")
    else:
        plt.ylabel("percentage")
        ax.set_ylim(max(0, min(allYvalues) * 0.9), min(max(allYvalues) * 1.1, 1))
    plt.plot(X, Y_low, label="low-species")
    # plt.plot(X, Y_lowgenus, label="low-genus")
    plt.plot(X, Y_high, label="hybrid-species")
    # plt.plot(X, Y_highgenus, label="hybrid-genus")
    plt.legend()
    plt.title(titles[show])
    plt.xlabel("reads length")
    if show in ["prec", "sens", "f1"]:
        plt.ylabel("score")
    elif show in ["pears"]:
        plt.ylabel("coefficent")
    else:
        plt.ylabel("percentage")
    plt.xticks(rotation=90)

    fig.savefig(dir_results / f"{show}.jpg", bbox_inches="tight")


#
#
# def count_reads(path: Path) -> int:
#     try:
#         with open(path, "r") as f:
#             reads_metadata = f.read().count("\n")  # simlord
#             return reads_metadata
#     except:
#         return 0
#
#
# def graph_unclussified(show):
#     import matplotlib.pyplot as plt
#     import numpy as np
#
#     # TODO change range
#     xlabels = [str(x) for x in range(200, 1001, 100)]
#     xlabels.extend([str(x) for x in range(1000, 10001, 1000)])
#
#     titles = {"no": "UNCLASSIFIED"}
#
#     norm = []
#     for file in glob.glob("../fasta/fasta_50/**/*.truth"):
#         print(file)
#         norm.append(count_reads(file))
#     t = norm.pop(1)
#     t = norm.insert(9, t)
#
#     data = json.load(open(DIR_RESULTS / "results.json", "r"))
#     Y = [a[show] for a in data.values()]
#     t = Y.pop(1)
#     t = Y.insert(9, t)
#     Y = np.array(Y)
#     norm = np.array(norm)
#     Y = Y / norm
#     X = np.linspace(1, len(Y), len(Y))
#     # Y=np.linspace(90,100,50)
#
#     # fig, ax=plt.subplots(figsize=(9,7))
#     fig, ax = plt.subplots()
#     ax.set_xticks(range(1, 21, 1), xlabels)
#     ax.set_ylim(min(Y) * 0.9, max(Y) * 1.1)
#     plt.bar(X, Y)
#     plt.title(titles[show])
#     plt.xlabel("reads length")
#     plt.ylabel("")
#     plt.xticks(rotation=90)
#
#     fig.savefig(dir_results / f"{show}.jpg", bbox_inches="tight")


if __name__ == "__main__":
    dir_res_lowerror = ROOT_DIR / "results/0704/"
    dir_truth_lowerror = ROOT_DIR / "fasta/fasta_50_0704/"
    dir_res_simlord_high = ROOT_DIR / "0607/results/simlord"
    dir_truth_high = ROOT_DIR / "0607/fasta/"
    dir_out_low = ROOT_DIR / "newResults/low"
    dir_out_high = ROOT_DIR / "newResults/high"
    dir_out_genus_low = ROOT_DIR / "newResults/hlow"
    dir_out_genus_high = ROOT_DIR / "newResults/hhigh"
    dir_out_low.mkdir(parents=True, exist_ok=True)
    dir_out_high.mkdir(parents=True, exist_ok=True)
    dir_out_genus_low.mkdir(parents=True, exist_ok=True)
    dir_out_genus_high.mkdir(parents=True, exist_ok=True)
    # rank = "species"
    # evaluate(dir_truth_lowerror, dir_res_lowerror, dir_out_low)
    # rank = "genus"
    # evaluate(dir_truth_lowerror, dir_res_lowerror, dir_out_genus_low)
    # rank = "species"
    # evaluate(dir_truth_high, dir_res_simlord_high, dir_out_high)
    # rank = "genus"
    # evaluate(dir_truth_high, dir_res_simlord_high, dir_out_genus_high)

    # dir_outimages=dir_out_genus_low.parent
    # dir_outimages = ROOT_DIR / "newResults/newResultsHybrid"
    dir_outimages = ROOT_DIR / "newResults/species"
    dir_outimages.mkdir(parents=True,exist_ok=True)
    show = "tp"
    graph(dir_outimages, show)
    show = "fn"
    graph(dir_outimages, show)
    show = "prec"
    graph(dir_outimages, show)
    show = "sens"
    graph(dir_outimages, show)
    show = "f1"
    graph(dir_outimages, show)
    show = "pears"
    graph(dir_outimages, show)
    show = "ok"
    graph(dir_outimages, show)
    show = "no"
    graph(dir_outimages, show)
    # graph_unclussified(show)
    # pass
