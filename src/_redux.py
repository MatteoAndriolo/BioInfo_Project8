import json
from multiprocessing import Pool, cpu_count

from _config import PATH_METADATA_REF, DIR_REF_REDUCED, MIN_FRAG_LENGTH, PATH_METADATA_REF_REDUCED


def filter(data):
    name: str = data[0]
    value: dict = data[1]
    lintro = []
    lseq = []
    reduced = False
    wrong_length = False
    print(f"Start {name}")

    with open(value["path"]) as fin:
        nsbefore = fin.read().count(">")

    with open(value["path"]) as fin:
        tseq = []
        lintro.append(fin.readline())
        if lintro[0][0] != ">":
            exit(5)
        for line in fin.readlines():
            if line[0] == ">":
                lintro.append(line)
                lseq.append(tseq)
                tseq = []
            else:
                tseq.append(line)

        if len(tseq):
            lseq.append(tseq)
            tseq.append(line)

        nseq = 0
        lenseq = []
        mean_length_sequence = 0

    newPath = DIR_REF_REDUCED / (name + ".fna")
    with open(newPath, "w") as fout:
        for k, v in zip(lintro, lseq):
            length_sequences = [len(a) for a in v]

            if min(length_sequences) != max(length_sequences):
                vv = [a for a in v if len(a) == max(length_sequences)]
                wrong_length = True

            sj = "".join(vv)
            ls = len(sj)
            nseq = sj.count(">")
            if (ls > MIN_FRAG_LENGTH):
                fout.write(k)
                nseq += 1
                fout.writelines(vv)
                lenseq.append(ls)
            else:
                reduced = True

    print(f"End {name}")
    return [name, {"path": str(newPath),
                   "mean_length_sequence": 0 if len(lenseq) == 0 else sum(lenseq) / len(lenseq),
                   "min": 0 if len(lenseq) == 0 else min(lenseq),
                   "max": 0 if len(lenseq) == 0 else max(lenseq),
                   "reduced": reduced,
                   "nseq_before": nsbefore,
                   "nseq": nseq,
                   "wrong_length": wrong_length
                   }]


if __name__ == "__main__":
    with open(PATH_METADATA_REF, "r") as fmtdt:
        mtdt_ref = json.load(fmtdt)

    with Pool(cpu_count()) as p, open(PATH_METADATA_REF_REDUCED, "w") as foutmtdt:
        # missing: dict = json.load(open(DIR_REF_REDUCED / "missing.json", "r"))
        # todo = {k: v for k, v in mtdt_ref_reduced.items() if v["nseq"] == 0}
        jData = {}
        for out in p.map(filter, mtdt_ref.items()):
            # for out in p.map(filter, todo.items()):
            jData[out[0]] = out[1]

        json.dump(jData, foutmtdt, indent=4)
