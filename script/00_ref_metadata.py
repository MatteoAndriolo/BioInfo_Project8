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
metadataseq_path="../ref/ref_50/metadata_seq.json"
metadata_path="../ref/ref_50/metadata.json"
files_path=glob.glob('../ref/ref_50/**/*.fna')
jsonData = {}

# parse files
for f_path in files_path:
    name = Path(f_path).stem
    if name[-4:]=="_Ref":
        name=name[:-4]

    description_lines=re.findall(p, open(f_path).read())

    jsonData[name] = {
        "path": f_path,
        "data_creation": date.today().strftime("%Y%m%d"),
        "n_sequences": len(description_lines),
        "sequences": [i for i in description_lines]
    }


with open(metadataseq_path, "w") as f:
    json.dump(jsonData, f, indent=4)

with open(metadata_path, "w") as f:
    for i in jsonData.keys():
        del jsonData[i]["sequences"]
    json.dump(jsonData, f, indent=4)
