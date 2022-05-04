from definitions import REF_DIR
import glob
from datetime import date
import re
import os
import hashlib
from time import time
import json
from timeit import timeit
import glob
from pathlib import Path

# description lines pattern search in FASTA files
p=re.compile(r'^\>(.*)', re.M)

# support data

metadataseq_path=os.path.join(REF_DIR,"metadata_seq.json")
metadata_path=os.path.join(REF_DIR,"metadata.json")
fna_path=sorted(list(glob.glob(os.path.join(REF_DIR,"**/*.fna"))))

jsonData = {}

# parse files
for f_path in fna_path:
    # extract name species
    name = Path(f_path).stem
    if name[-4:]=="_Ref":
        name=name[:-4]

    # reads description lines
    description_lines=re.findall(p, open(f_path).read())

    # generate data
    jsonData[name] = {
        "path": f_path,
        "data_creation": date.today().strftime("%Y%m%d"),
        "n_sequences": len(description_lines),
        "sequences": [i for i in description_lines]
    }


# write files with and without seqences name details.
with open(metadataseq_path, "w") as f:
    json.dump(jsonData, f, indent=4)

with open(metadata_path, "w") as f:
    for i in jsonData.keys():
        del jsonData[i]["sequences"]
    json.dump(jsonData, f, indent=4)
