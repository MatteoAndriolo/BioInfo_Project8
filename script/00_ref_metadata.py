from datetime import date
import re
import os
import hashlib
from time import time
import json
from timeit import timeit
import glob
from config import dir_ref
from pathlib import Path

# description lines pattern search in FASTA files
p=re.compile(r'^\>(.*)', re.M)

# support data
#mtdt_seq=dir_ref/"metadata_seq.json"
mtdt_path=dir_ref/"metadata.json"
files_path=glob.glob(str(dir_ref/'*.fna'))
jsonData = {}

# jsonData["data_creation"]= date.today().strftime("%Y%m%d")

# parse files
for f_path in files_path:
    name = Path(f_path).stem
    if name[-4:]=="_Ref":
        name=name[:-4]

    description_lines=re.findall(p, open(f_path).read())

    jsonData[name] = {
        "path": f_path,
        "n_sequences": len(description_lines),
        "sequences": [i for i in description_lines]
    }

# with open(mtdt_seq, "w") as f:
#     json.dump(jsonData, f, indent=4)

with open(mtdt_path, "w") as f:
    for i in jsonData.keys():
        del jsonData[i]["sequences"]
    json.dump(jsonData, f, indent=4)