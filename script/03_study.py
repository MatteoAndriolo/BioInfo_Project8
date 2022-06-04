import glob
import json
import os
from multiprocessing import Pool, cpu_count

from _config import DIR_RESULTS, DIR_RES_OUT, PATH_METADATA_REF, ROOT_DIR


def _cut(path: str) -> dict:
    print(path)
    path2 = path.replace('.out', '.cut')
    command = f"cut -f 2-3 {path} >> {path2}"
    os.system(command)


def cut():
    with Pool(cpu_count() * 2) as p:
        p.map(_cut, glob.glob(str(DIR_RES_OUT / "**" / "*.out"), recursive=True))


names = sorted(list(set(json.load(open(PATH_METADATA_REF, "r")).keys())))
names=[n.replace("_"," ") for n in names]


def _test(x):
    save=[n in x for n in names]
    x = x.replace("\t", "")
    if any(save) and x.split("|")[3]=="scientific name":
            return (names[save.index(True)], x)
    else:
        return None


def test_names(path: str):
    out={n:[] for n in names}
    with open(path, "r") as fin, Pool(cpu_count() * 2) as p:
        for o in p.map(_test, fin.readlines()):
            if o:
                out[o[0]].append(o[1])

    json.dump(out,open("out.json","w"), indent=4)






if __name__ == "__main__":
    # PHASE 0 CUT
    cut()
    # print(names)
    # test_names(ROOT_DIR / "script" / "DBKraken2" / "names.dmp")

