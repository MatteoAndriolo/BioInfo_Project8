<<<<<<< HEAD
import glob
import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from config import DIR_TEMP, ROOT_DIR


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
    @param dir_truth: directory containing truth file
    @param dir_results: directory containing kraken2 results
    @return: json dictionary with results
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


def graph(dir_results: Path, *listshow):
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    for show in listshow:
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

        xlabels: list[int] = sorted(list(map(int, mtdt_results_low.keys())))
        if 999 in xlabels:
            xlabels[xlabels.index(999)] = 1000
        if 1001 in xlabels:
            xlabels[xlabels.index(1001)] = 1000

        if show in ["tp", "fp", "fn", "ok", "no"]:
            Y_low = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in
                     list(sorted(mtdt_results_low.items(), key=lambda x: x[0]))]
            Y_lowgenus = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in
                          list(sorted(mtdt_results_lowgenus.items(), key=lambda x: x[0]))]
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
    dir_outimages.mkdir(parents=True, exist_ok=True)
    graph(dir_outimages, "tp", "fn", "prec", "sens", "f1", "pears", "ok", "no")
=======
import glob
import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from config import DIR_TEMP, ROOT_DIR


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
    @param dir_truth: directory containing truth file
    @param dir_results: directory containing kraken2 results
    @return: json dictionary with results
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


def graph(dir_results: Path, *listshow):
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    for show in listshow:
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

        xlabels: list[int] = sorted(list(map(int, mtdt_results_low.keys())))
        if 999 in xlabels:
            xlabels[xlabels.index(999)] = 1000
        if 1001 in xlabels:
            xlabels[xlabels.index(1001)] = 1000

        if show in ["tp", "fp", "fn", "ok", "no"]:
            Y_low = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in
                     list(sorted(mtdt_results_low.items(), key=lambda x: x[0]))]
            Y_lowgenus = [k[show] / mtdt_fasta_low[v]['nreads'] for v, k in
                          list(sorted(mtdt_results_lowgenus.items(), key=lambda x: x[0]))]
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
    dir_outimages.mkdir(parents=True, exist_ok=True)
    graph(dir_outimages, "tp", "fn", "prec", "sens", "f1", "pears", "ok", "no")
>>>>>>> 70b5b395b1eaa7513738515891a8c944145dedb4
