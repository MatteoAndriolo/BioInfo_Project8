import json
import os, shutil

# support data
metadata_reads=json.load(open("../reads/reads_50/metadata.json"))
dir_reads="../reads/reads_50"
fasta_out="../reads/fasta_sim_50.fasta"

metadata_reads=json.load(open("../reads/reads_50/metadata.json"))
dir_reads="../reads/reads_50"
fasta_out="../reads/fasta_sim_50.fasta"

# construct single file
with open(fasta_out, mode='w') as out_file:
    counter_reads=0
    for file in metadata_reads:
        with open(file["path"],'r') as f:
            # introduce one description line for each read
            for line in f:
                # specify number of read introduced in the file (0 based)
                out_file.write(">S0R"+str(counter_reads)+'\n'+str(line)+'\n')
                counter_reads+=1
