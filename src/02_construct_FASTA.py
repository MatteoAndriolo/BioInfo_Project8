import json
import os, shutil
from pathlib import Path
from definitions import READS_DIR

c=20
pi=0.11
pd=0.4
ps=0.01
tag=f"c{c}pi{pi}pd{pd}ps{ps}"
# support data
dir_reads=Path(READS_DIR)/"reads50_simlord"/tag
metadata_reads=json.load(open(dir_reads/"metadata.json"))
fasta_out=dir_reads/"fasta_sim_50.fasta"

metadata_reads=json.load(open(dir_reads/"metadata.json"))

# construct single file
if __name__=="__main__":
    with open(fasta_out, mode='w') as out_file:
        counter_reads=0
        for v,k in metadata_reads.items():
            print(v)
            with open(k["path"],'r') as f:
                # introduce one description line for each read
                for line in f:
                    # specify number of read introduced in the file (0 based)
                    out_file.write(">S0R"+str(counter_reads)+'\n'+str(line)+'\n')
                    counter_reads+=1
