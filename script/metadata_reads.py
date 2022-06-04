import glob
import json
from multiprocessing import Pool, cpu_count
from pathlib import Path

from _config import DIR_READS_MASON, RANGE_SHORT, PATH_METADATA_REF, DIR_READS_SIMLORD, RANGE_LONG

# PATH_METADATA_REF_REDUCED, DIR_REF_REDUCED, DIR_READS_REDUCED, DIR_READS_MASON_REDUCED

dir_reads_mason = DIR_READS_MASON


def count_reads(path) -> None:
    # print(path)
    with open(Path(path) / "metadata.json", "r") as metadatafile:
        reads_metadata = json.load(metadatafile)
        for k, v in reads_metadata.items():
            with open(v["path"], "r") as f:
                reads_metadata[k]["nreads"] = f.read().count("@")  # simlord
                # reads_metadata[k]["nreads"] = f.read().count(">")  # mason
    with open(Path(path) / "metadata.json", "w") as metadatafile:
        json.dump(reads_metadata, metadatafile, indent=4)
        metadatafile.close()


def return_emptyfile_names(path) -> list:
    out = []
    with open(Path(path) / "metadata.json", "r") as metadatafile:
        reads_metadata = json.load(metadatafile)
        for k, v in reads_metadata.items():
            if int(v["nreads"]) == 0:
                # print(v["path"])
                out.append(v["path"].split("/")[-1])
    return out


def find_reads_with0():
    from _config import DIR_READS_MASON_REDUCED

    mtdt: dict = json.load(open(Path(DIR_READS_MASON_REDUCED) / str(RANGE_SHORT[0]) / "metadata.json", "r"))
    jsonDic = {n: {} for n in mtdt.keys()}

    for n in RANGE_SHORT:
        mtdt: dict = json.load(open(Path(DIR_READS_MASON_REDUCED) / str(n) / "metadata.json", "r"))
        for v, k in mtdt.items():
            jsonDic[v][str(n)] = k["nreads"]
    with open("metadata_reads.josn", "w") as fout:
        json.dump(jsonDic, fout, indent=4)


def filter_json_ref() -> None:
    with open(Path(PATH_METADATA_REF_REDUCED), "r") as fin, open(Path(DIR_REF_REDUCED) / "missing.json", "w") as fout:
        mtdt: dict = json.load(fin)
        jsonDict = {v: k for v, k in mtdt.items() if k["nseq"] == 0}

        json.dump(jsonDict, fout, indent=4)

    jsonDict = {}
    with open(Path(DIR_READS_REDUCED) / "missing.json", "w") as fout:
        for n in RANGE_SHORT:
            for path in glob.glob(str(DIR_READS_REDUCED) + '/mason/' + str(n) + '/metadata.json'):
                with open(path, "r") as fin:
                    mtdt: dict = json.load(fin)
                    temp = {v: k for v, k in mtdt.items() if k["nreads"] == 0}
            jsonDict[str(n)] = temp

        json.dump(jsonDict, fout, indent=4)


def getNamesOf0FromBoth():
    mtdt = {}
    mtdtred = {}
    for n in RANGE_SHORT:
        with open(DIR_READS_MASON / str(n) / "metadata.json", "r") as fref:
            # open(DIR_READS_MASON_REDUCED / str(n) / "metadata.json", "r") as frefred:
            t = json.load(fref)
            # tred = json.load(frefred)
        mtdt[n] = {v: k for v, k in t.items() if k["nreads"] == 0}
        # mtdtred = {v: k for v, k in tred.items() if k["nreads"] == 0}
    print(mtdtred, mtdt)
    with open(DIR_READS_MASON / "missing.json", "w") as fout:
        # , open(DIR_READS_MASON_REDUCED / "missing.json","w") as foutred:
        # json.dump(mtdtred, foutred, indent=4)
        json.dump(mtdt, fout, indent=4)


if __name__ == "__main__":
    # return names of files with 0 reads produced
    # listFolders = [DIR_READS_SIMLORD / str(n) for n in RANGE_LONG]
    listFolders = [DIR_READS_MASON / str(n) for n in RANGE_SHORT]
    with Pool(cpu_count() * 2) as p:
        out = {}
        for i, a in enumerate(p.map(return_emptyfile_names, listFolders)):
            out[str(RANGE_SHORT[i])] = a
    with open(DIR_READS_MASON / "missing.json", "w") as fout:
        json.dump(out, fout, indent=4)

    # with open(PATH_METADATA_REF, "r") as f:
    #     mtdt = json.load(f)
    #     for n in out:
    #         with open(mtdt[n[:-3]]["path"], "r") as f2:
    #             stri = f2.read()
    #             stri = stri.split(">")
    #             # print(len(stri))
    #             c = [len(a.replace("\n", "")) for a in stri]
    #             c.pop(0)
    #
    #             if min(c) < 1000:
    #                 print(n[:-3], max(c), min(c), len(c))

    # find_reads_with0()

    # filter_json_ref()

    getNamesOf0FromBoth()
