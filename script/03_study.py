import glob
import json
import os
from multiprocessing import Pool, cpu_count

from _config import DIR_RESULTS, DIR_RES_OUT, PATH_METADATA_REF, ROOT_DIR, DIR_FASTA_REF


def _cut(path: str) -> dict:
    print(path)
    path2 = path.replace('.out', '.cut')
    command = f"cut -f 2-3 {path} > {path2}"
    os.system(command)


'''
Cut colums of out files
'''


def cut(path):
    with Pool(cpu_count() * 2) as p:
        p.map(_cut, glob.glob(str(path / "*.out"), recursive=True))


names_ref = sorted(list(set(json.load(open(PATH_METADATA_REF, "r")).keys())))
names_ref = [n.replace("_", " ") for n in names_ref]


def _test(x):
    save = [n in x for n in names_ref]
    x = x.replace("\t", "")
    if any(save) and x.split("|")[3] == "scientific name":
        return (names_ref[save.index(True)], x)
    else:
        return None


'''
Staring from node.dmp extract taxid|names of genomes of interest
'''


def test_names(path: str):
    out = {n: [] for n in names_ref}
    with open(path, "r") as fin, Pool(cpu_count() * 2) as p:
        for o in p.map(_test, fin.readlines()):
            if o:
                out[o[0]].append(o[1])

    json.dump(out, open("out.json", "w"), indent=4)


if __name__ == "__main__":
    # PHASE 0 CUT
    cut(DIR_FASTA_REF)
    # print(names)
    # test_names(ROOT_DIR / "script" / "DBKraken2" / "names.dmp")
