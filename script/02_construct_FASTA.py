import json
from multiprocessing import Pool, cpu_count

from _config import DIR_READS_MASON, RANGE_SHORT, DIR_FASTA_MASON, DIR_FASTA_SIMLORD, DIR_READS_SIMLORD, RANGE_LONG, \
    PATH_TAXID_REF

dir_fasta_mason = DIR_FASTA_MASON
dir_fasta_simlord = DIR_FASTA_SIMLORD


def generateFastaAndTruth(folder):
    # reads/reads_50/simlord/10000
    s = str(folder).split("/")
    n, simulator = s[-1], s[-2]  # get info simulator (name and length sequences)

    # manage path and files path
    fastaDir = dir_fasta_simlord if simulator == "simlord" else dir_fasta_mason
    fasta_file_path = fastaDir / f"{simulator}_{n}.fasta"
    fasta_truth_file_path = fastaDir / f"{simulator}_{n}.truth"

    mtdt = json.load(open(folder / "metadata.json", "r"))

    # with open(fasta_file_path, "w") as outfile:
    # with open(fasta_truth_file_path, "w") as truthfile:
    with open(fasta_file_path, "w") as outfile, open(fasta_truth_file_path, "w") as truthfile, open(PATH_TAXID_REF,
                                                                                                    "r") as ftid:
        next = False
        read_number = 0
        taxid = json.load(ftid)
        # 0 based indexes
        blocks = {}
        for k, v in mtdt.items():
            if v["nreads"] == 0:
                blocks[k] = None
                continue
            print(v["path"])
            with open(v["path"], "r") as f:
                for line in f.readlines():
                    if line[0] == "@":
                        next = True
                    elif next and line[0] in ["A", "C", "G", "T"]:
                        outfile.write(f">S0R{read_number}\n{str(line)}\n")
                        truthfile.write(f"S0R{read_number}\t{taxid[k[:-6]]['taxId']}\n")
                        read_number += 1
                        next = False
                    else:
                        next = False
            blocks[k] = read_number - 1
    return (simulator, n, {"path": str(fasta_file_path), "nreads": read_number + 1, "index_end": blocks})


if __name__ == "__main__":
    # Folder where take files in order to generate fasta
    listFolders = [DIR_READS_MASON / str(n) for n in RANGE_SHORT]
    listFolders.extend([DIR_READS_SIMLORD / str(n) for n in RANGE_LONG])

    masonJson = {}  # output dictionary for mason
    simlordJson = {}  # output dictionary for simlord

    with Pool(2 * cpu_count()) as p:
        for out in p.map(generateFastaAndTruth, listFolders):
            if out[0] == "mason":
                masonJson[out[1]] = out[2]
            elif out[0] == "simlord":
                simlordJson[out[1]] = out[2]
            else:
                raise ValueError

    # dump json files
    if masonJson:
        with open(dir_fasta_mason / "_metadata.json", "w") as f:
            json.dump(masonJson, f, indent=4, sort_keys=True)
    if simlordJson:
        with open(dir_fasta_simlord / "_metadata.json", "w") as f:
            json.dump(simlordJson, f, indent=4, sort_keys=True)
