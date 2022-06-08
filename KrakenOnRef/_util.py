import glob
import json
import os
import re
from multiprocessing import Pool, cpu_count
from pathlib import Path

# from script._config import PATH_TAXID_REF
PATH_TAXID_REF = Path("../../ref/ref_50/_ncbiTaxonID.json")

p_taxid = ".?(\d{1,})\)"
p_initfasta = "S.*\t"
taxidJson = json.load(open(PATH_TAXID_REF, "r"))


def uncertainTaxidsFromKraken() -> dict:
    uncertainJson = {}
    for file in glob.glob("*.cut"):
        name = file[:-4]
        taxid = list(map(int, re.findall(p_taxid, open(file, "r").read())))
        settaxid = set(taxid)

        if len(settaxid) == 1:
            continue

        uncertainJson[name] = []
        for tid in settaxid:
            for line in open(file, "r").readlines():
                if f"(taxid {tid})" in line:
                    tname = re.sub(p_initfasta, "", line)[:-1]
                    uncertainJson[name].append({tid: {"name": tname, "acc": taxid.count(tid) / len(taxid)}})
                    # uncertainJson[name].append({"taxId": int(tid), "taxName": tname})
                    break

    #############################
    json.dump(uncertainJson, open("_uncertainTaxonIDs.json", "w"), indent=4)
    return uncertainJson


def taxid_manual_finals() -> dict:
    forcednames = json.load(open("supportData/_forcedTaxID.json", "r"))
    jsonData = {}
    for file in glob.glob("*.cut"):
        name = file[:-4]
        taxid = list(map(int, re.findall(p_taxid, open(file, "r").read())))
        settaxid = set(taxid)

        if len(settaxid) == 1:
            tid = settaxid.pop()
        elif name.replace(" ", "_") in forcednames:
            tid = forcednames[name]["taxId"]
        elif len(settaxid) == len(taxid):
            tid = settaxid
        else:
            exit(5)

        for line in open(file, "r").readlines():
            if f"(taxid {tid})" in line:
                tname = re.sub(p_initfasta, "", line)[:-1]
                break
        jsonData[name] = {"taxId": int(tid), "taxName": tname}

    #############################
    json.dump(jsonData, open("_krakenTaxonID.json", "w"), indent=4)
    return jsonData


def _res_nametoid(path):
    with open(path, "r") as fin:
        data = fin.read()
    data = re.sub(r"(S0R\d*).*\(taxid (\d*)\)", r"\g<1>|\g<2>", data)
    data = re.sub("\|", "\t", data)
    with open(path, "w") as fout:
        fout.write(data)


def result_nameToID():
    with Pool(cpu_count() * 2) as p:
        p.map(_res_nametoid, glob.glob("cut/*.cut", recursive=True))


def _createTruth(path: Path):
    taxid = taxidJson[path.stem]['taxId']
    with open(path, "r") as fin:
        data = fin.read()
    data = re.sub(r" \d*$", f" {taxid}", data)
    with open(str(path).replace(".cut", ".truth"), "w") as fout:
        fout.write(data)


def createTruth():
    with Pool(cpu_count() * 2) as p:
        p.map(_createTruth, map(Path, glob.glob("cut/*.cut", recursive=True)))


def _evaluate(path):
    print(path)
    rank = "species"
    nodes_dir = Path("../../script/nodes.dmp")
    temp_dir = Path(".temp")
    temp_dir.mkdir(exist_ok=True)
    temp = temp_dir / (Path(path[0]).stem)
    command = f"../../script/evaluate {nodes_dir} {rank} {path[0]} {path[1]} > {temp}"
    # get data
    os.system(command)
    with open(temp, "r") as resin:
        resin.readline()
        results: str = resin.readline()
    # os.system(f"rm {temp}")

    # process data
    results = results[:-1]
    tp, fp, fn, ok, no, tot, sens, prec, f1, pears = map(float, results.split("\t"))
    outdict = {"tp": tp, "fp": fp, "fn": fn, "ok": ok, "no": no, "tot": tot, "sens": sens, "prec": prec, "f1": f1,
               "pears": pears}

    return [Path(path[0]).stem, outdict]


# evaluate data
def evaluate():
    jsonData = {}
    cut_files = sorted(glob.glob(f"cut/*.cut", recursive=True))
    truth_files = sorted(glob.glob(f"cut/*.truth", recursive=True))
    files = zip(cut_files, truth_files)
    with Pool(cpu_count() * 2) as p:
        for out in p.map(_evaluate, files):
            jsonData[out[0]] = out[1]

    json.dump(jsonData, open("results.json", "w"), indent=4)


if __name__ == "__main__":
    # uncertainTaxidsFromKraken()
    # taxid_manual_finals()
    # result_nameToID()
    # createTruth()
    evaluate()
    # pass
