import glob
import json
import math
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from config import DIR_RESULTS, PATH_METADATA_REF, DIR_FASTA, DIR_TEMP, PATH_METADATA_FASTA, ROOT_DIR


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
    """
    Evaluate cutted output file of kraken2
    @return:
    """
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


def graph(*listshow):
    """
    Create graphs of evaluation parameters
    @param listshow: insert comma separated list of parameters of interest ("tp","fp","fn","prec","f1","sens","pears","ok","no")
    @return:
    """
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])

    for show in listshow:
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
        mtdt_fasta = json.load(open(path_metadata_fasta, "r"))
        for a in list(mtdt.keys()):
            if math.isnan(mtdt[a]["f1"]):
                del mtdt[a]
        xlabels: list[int] = sorted(list(map(int, mtdt.keys())))
        if show in ["tp", "fp", "fn", "ok", "no"]:
            Y = [k[show] / mtdt_fasta[v]['nreads'] for v, k in mtdt.items()]
        else:
            Y = [a[show] for a in mtdt.values()]
        # t = Y.pop(2)
        # Y.insert(9, t)
        X = np.linspace(1, len(Y), len(Y))
        # Y=np.linspace(90,100,50)

        # fig, ax=plt.subplots(figsize=(9,7))
        fig, ax = plt.subplots()
        ax.set_xticks(range(1, len(X) + 1, 1), xlabels)
        if mtdt_fasta:
            ax.set_ylim(max(0, min(Y) - .1), max(Y) + .1)
        else:
            ax.set_ylim(max(0, min(Y) * 0.9), max(Y) * 1.1)
        plt.bar(X, Y)
        plt.title(titles[show])
        plt.xlabel("reads length")
        plt.ylabel("percentage")
        plt.xticks(rotation=90)

        fig.savefig(dir_results_images / f"{show}.jpg", bbox_inches="tight")


def count_reads(path: Path) -> int:
    try:
        with open(path, "r") as f:
            reads_metadata = f.read().count("\n")  # simlord
            return reads_metadata
    except:
        return 0


def compare(*listshow):
    """
    Create graphs of evaluation parameters
    @param listshow: insert comma separated list of parameters of interest ("tp","fp","fn","prec","f1","sens","pears","ok","no")
    @return:
    """
    # xlabels = [str(x) for x in range(100, 1001, 100)]
    # xlabels.extend([str(x) for x in range(1000, 10001, 1000)])
    for show in listshow:
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

        mtdt_species: dict = json.load(open(dir_metadata_results, "r"))
        mtdt_genus: dict = json.load(open(dir_metadata_results_genus, "r"))
        mtdt_hybrid: dict = json.load(open(dir_metadata_results_hybrid, "r"))
        mtdt_fasta = json.load(open(path_metadata_fasta, "r"))
        for a in list(mtdt_species.keys()):
            if math.isnan(mtdt_species[a]["f1"]):
                del mtdt_species[a]
            if math.isnan(mtdt_genus[a]["f1"]):
                del mtdt_genus[a]
            if math.isnan(mtdt_hybrid[a]["f1"]):
                del mtdt_hybrid[a]
        xlabels: list[int] = sorted(list(map(int, mtdt_species.keys())))
        if show in ["tp", "fp", "fn", "ok", "no"]:
            Y_species = [k[show] / mtdt_fasta[v]['nreads'] for v, k in mtdt_species.items()]
            Y_genes = [k[show] / mtdt_fasta[v]['nreads'] for v, k in mtdt_genus.items()]
            Y_hybrid = [k[show] / mtdt_fasta[v]['nreads'] for v, k in mtdt_hybrid.items()]
        else:
            Y_species = [a[show] for a in mtdt_species.values()]
            Y_genes = [a[show] for a in mtdt_genus.values()]
            Y_hybrid = [a[show] for a in mtdt_hybrid.values()]
        # t = Y.pop(2)
        # Y.insert(9, t)
        X = np.linspace(1, len(Y_species), len(Y_species))
        # Y=np.linspace(90,100,50)

        # fig, ax=plt.subplots(figsize=(9,7))
        fig, ax = plt.subplots()
        ax.set_xticks(range(1, len(X) + 1, 1), xlabels)
        if mtdt_fasta:
            ax.set_ylim(max(0, min(Y_genes + Y_species + Y_hybrid) - .1),
                        min(1, max(Y_species + Y_genes + Y_hybrid) + .1))
        else:
            ax.set_ylim(max(0, min(Y_genes + Y_species + Y_hybrid) * 0.9),
                        min(max(Y_species + Y_genes + Y_hybrid) * 1.1, 1))
        plt.plot(X, Y_genes, label="genes")
        plt.plot(X, Y_species, label="species")
        plt.plot(X, Y_hybrid, label="hybrid-species")
        plt.legend()
        plt.title(titles[show])
        plt.xlabel("reads length")
        plt.ylabel("percentage")
        plt.xticks(rotation=90)

        fig.savefig(dir_results_images / f"{show}.jpg", bbox_inches="tight")


if __name__ == "__main__":
    dir_fasta: Path = DIR_FASTA
    dir_truth: Path = DIR_FASTA
    dir_results: Path = DIR_RESULTS / "0704"
    dir_metadata_results: Path = dir_results / "_results.json"
    dir_results_images: Path = DIR_RESULTS / "0706_hybrid"
    dir_metadata_results_genus: Path = dir_results / "genus/_results.json"
    dir_metadata_results_hybrid: Path = ROOT_DIR / "0607/results/_metadata_hybrid_species.json"
    path_metadata_fasta: Path = PATH_METADATA_FASTA
    names_ref = sorted(list(set(json.load(open(PATH_METADATA_REF, "r")).keys())))
    names_ref = [n.replace("_", " ") for n in names_ref]
    # rank = "species"
    # evaluate(dir_truth_lowerror, dir_res_lowerror, dir_out_low)
    # rank = "genus"
    # evaluate(dir_truth_lowerror, dir_res_lowerror, dir_out_genus_low)
    # rank = "species"
    # evaluate(dir_truth_high, dir_res_simlord_high, dir_out_high)
    # rank = "genus"
    # evaluate(dir_truth_high, dir_res_simlord_high, dir_out_genus_high)

    compare("tp", "fn", "prec", "sens", "f1", "pears", "ok", "no")
