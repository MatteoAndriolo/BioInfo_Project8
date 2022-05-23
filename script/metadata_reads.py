import json
from multiprocessing import Pool, cpu_count
from pathlib import Path

from config import DIR_READS_MASON, RANGE_SHORT, PATH_METADATA_REF


def count_reads(path) -> None:
    print(path)
    with open(Path(path) / "metadata.json", "r") as metadatafile:
        reads_metadata = json.load(metadatafile)
        for k, v in reads_metadata.items():
            with open(v["path"], "r") as f:
                reads_metadata[k]["nreads"] = f.read().count("@")  # simlord
                # reads_metadata[k]["nreads"] = f.read().count(">")  # mason
    with open(Path(path) / "metadata.json", "w") as metadatafile:
        json.dump(reads_metadata, metadatafile, indent=4)
        metadatafile.close()


def find_mason_empty(path) -> list:
    out = []
    with open(Path(path) / "metadata.json", "r") as metadatafile:
        reads_metadata = json.load(metadatafile)
        for k, v in reads_metadata.items():
            if int(v["nreads"]) == 0:
                # print(v["path"])
                out.append(v["path"].split("/")[-1])
    return out


if __name__=="__main__":
    # listFolders = [DIR_READS_SIMLORD / str(n) for n in RANGE_LONG]
    listFolders = [DIR_READS_MASON / str(n) for n in RANGE_SHORT]
    print(listFolders)
    with Pool(cpu_count() * 2) as p:
        out = []
        for a in p.map(find_mason_empty, listFolders):
            out.extend(a)

        print(out)

    with open(PATH_METADATA_REF,"r") as f:
        mtdt=json.load(f)
        for n  in out:
            with open(mtdt[n[:-3]]["path"],"r") as f2:
                stri=f2.read()
                stri=stri.split(">")
                print(stri)
                print(len(stri))
                c=[len(a) for a in stri]
                print(n[:-3],max(a),min(a),len(c))




