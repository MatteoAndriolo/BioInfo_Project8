import json

# support data
from multiprocessing import Pool, cpu_count

from config import DIR_READS_MASON, DIR_READS_SIMLORD, RANGE_LONG, RANGE_SHORT, DIR_FASTA_MASON, DIR_FASTA_SIMLORD


def generateFasta(folder):
    s = str(folder).split("/")
    n, typ = s[-1], s[-2]
    fastaDir = DIR_FASTA_SIMLORD if typ == "simlord" else DIR_FASTA_MASON

    with open(fastaDir / f"{typ}_{n}.fasta", "w") as outfile, \
            open(folder / "metadata.json", "r") as mdf:
        metadata = json.load(mdf)
        read_number = 0
        for k, v in metadata.items():
            print(v["path"])
            with open(v["path"], "r") as f:
                for line in f.readlines():
                    if line[0] in ["A", "C", "G", "T"]:
                        outfile.write(f">S0R{read_number}\n{str(line)}\n")


listFolders = [DIR_READS_MASON / str(n) for n in RANGE_SHORT]
listFolders.extend([DIR_READS_SIMLORD / str(n) for n in RANGE_LONG])

with Pool(2 * cpu_count()) as p:
    p.map(generateFasta, listFolders)

exit(5)
##############################################################################################################à


for n in RANGE_LONG:
    metadata_simlord = json.load(open(DIR_READS_SIMLORD / str(n) / "metadata.json"))
    fasta_out_simlord = DIR_READS_SIMLORD / str(n) / f"simlord_{n}.fasta"
    with open(fasta_out_simlord, "w") as out_simlord:
        counter_reads = 0
        for v, k in metadata_simlord.items():
            print(v)
            with open(k["path"], 'r') as f:
                # introduce one description line for each read
                generateFasta(f.readlines(), out_simlord)

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
