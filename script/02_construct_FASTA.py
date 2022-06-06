import json
from multiprocessing import Pool, cpu_count

from _config import DIR_READS_MASON, RANGE_SHORT, DIR_FASTA_MASON, DIR_FASTA_SIMLORD, DIR_READS_SIMLORD, RANGE_LONG, \
    PATH_TAXID_REF


def generateFasta(folder):
    # reads/reads_50/simlord/10000
    s = str(folder).split("/")      
    n, simulator = s[-1], s[-2]     # get info simulator (name and length sequences)
    
    # manage path and files path
    fastaDir = DIR_FASTA_SIMLORD if simulator == "simlord" else DIR_FASTA_MASON
    fasta_file_path = fastaDir / f"{simulator}_{n}.fasta"
    fasta_truth_file_path = fastaDir / f"{simulator}_{n}.truth"

    mtdt = json.load(open(folder / "metadata.json", "r"))

    # with open(fasta_file_path, "w") as outfile:
    # with open(fasta_truth_file_path, "w") as truthfile:
    with open(fasta_file_path, "w") as outfile, open(fasta_truth_file_path, "w") as truthfile, open(PATH_TAXID_REF,"r") as ftid:
        next = False
        read_number = 0
        taxid=json.load(ftid)
        # 0 based indexes
        blocks={}
        for k, v in mtdt.items():
            if v["nreads"]==0:
               # TODO check cotrrectness
               # blocks[k]=read_number
               blocks[k]=None
               continue
            print(v["path"])
            with open(v["path"], "r") as f:
                for line in f.readlines():
                    if line[0] == "@":
                        next = True
                    elif next and line[0] in ["A", "C", "G", "T"]:
                        outfile.write(f">S0R{read_number}\n{str(line)}\n")
                        truthfile.write(f">S0R{read_number}\t{taxid[k[:-6]]['taxId']}\n")
                        read_number += 1
                        next = False
                    else:
                        next = False
        blocks[k] = read_number-1
    return (simulator, n, {"path": str(fasta_file_path), "nreads": read_number + 1, "index_end":blocks})


if __name__ == "__main__":
    # Folder where take files in order to generate fasta
    listFolders = [DIR_READS_MASON / str(n) for n in RANGE_SHORT]
    listFolders.extend([DIR_READS_SIMLORD / str(n) for n in RANGE_LONG])

    masonJson = {}      # output dictionary for mason
    simlordJson = {}    # output dictionary for simlord

    with Pool(2 * cpu_count()) as p:
        for out in p.map(generateFasta, listFolders):
            if out[0] == "mason":
                masonJson[out[1]] = out[2]
            elif out[0] == "simlord":
                simlordJson[out[1]] = out[2]
            else:
                raise ValueError

    # dump json files
    if masonJson:
        with open(DIR_FASTA_MASON / "metadata.json", "w") as f:
            json.dump(masonJson, f, indent=4, sort_keys=True)
    if simlordJson:
        with open(DIR_FASTA_SIMLORD / "metadata.json", "w") as f:
            json.dump(simlordJson, f, indent=4, sort_keys=True)

    exit(5)

    # for n in RANGE_LONG:
    #    metadata_simlord = json.load(open(DIR_READS_SIMLORD / str(n) / "metadata.json"))
    #    fasta_out_simlord = DIR_READS_SIMLORD / str(n) / f"simlord_{n}.fasta"
    #    with open(fasta_out_simlord, "w") as out_simlord:
    #        counter_reads = 0
    #        for v, k in metadata_simlord.items():
    #            print(v)
    #            with open(k["path"], 'r') as f:
    #                # introduce one description line for each read
    #                generateFasta(f.readlines(), out_simlord)

    # for n in RANGE_SHORT:
    #    metadata_mason = json.load(open(DIR_READS_MASON / str(n) / "metadata.json"))
    #    fasta_out_mason = DIR_READS_MASON / str(n) / f"mason_{n}.fasta"
    #    with open(fasta_out_mason, 'w') as out_mason:
    #        counter_reads = 0
    #        for v, k in metadata_mason.items():
    #            print(v)
    #            with open(k["path"], 'r') as f:
    #                # introduce one description line for each read
    #                generateFasta(f.readlines(), out_mason)
