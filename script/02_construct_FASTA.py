import json

# support data
from config import DIR_READS_MASON, DIR_READS_SIMLORD, RANGE_LONG, RANGE_SHORT


def generateFasta(lines, outfile):
    read_number = 0
    for line in lines:
        if line[0] in ["A", "C", "G", "T"]:
            outfile.write(f">S0R{read_number}\n{str(line)}\n")


for n in RANGE_LONG:
    metadata_simlord = json.load(open(DIR_READS_SIMLORD / str(n) / "metadata.json"))
    fasta_out_simlord = DIR_READS_SIMLORD / str(n) / f"simlord_{n}.fasta"
    with open(fasta_out_simlord, "w") as out_simlord:
        counter_reads = 0
        with
        for v, k in metadata_simlord.items():
            print(v)
            with open(k["path"], 'r') as f:
                # introduce one description line for each read
                generateFasta(f.readlines(), out_simlord)

#for n in RANGE_SHORT:
#    metadata_mason = json.load(open(DIR_READS_MASON / str(n) / "metadata.json"))
#    fasta_out_mason = DIR_READS_MASON / str(n) / f"mason_{n}.fasta"
#    with open(fasta_out_mason, 'w') as out_mason:
#        counter_reads = 0
#        for v, k in metadata_mason.items():
#            print(v)
#            with open(k["path"], 'r') as f:
#                # introduce one description line for each read
#                generateFasta(f.readlines(), out_mason)
