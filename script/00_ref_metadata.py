import glob
import json
import re
from pathlib import Path

from config import DIR_REF, PATH_METADATA_REF

# description lines pattern search in FASTA files
p = re.compile(r'^\>(.*)', re.M)

# support data
# mtdt_seq=dir_ref/"metadata_seq.json"
files_path = glob.glob(str(DIR_REF / '*.fna'))
jsonData = {}


# jsonData["data_creation"]= date.today().strftime("%Y%m%d")

def getSeqLength(text) -> (int, int, int):
    lengthSeq = []
    somma = 0
    for line in text:
        if ">" in line and somma != 0:
            lengthSeq.append(somma)
            somma = 0
        else:
            somma += len(line)
    if somma != 0:
        lengthSeq.append(somma)
    print(somma, lengthSeq)
    return (min(lengthSeq), max(lengthSeq), int(sum(lengthSeq) / len(lengthSeq)))


# parse files
for f_path in files_path:
    name = Path(f_path).stem
    if name[-4:] == "_Ref":
        name = name[:-4]

    description_lines = re.findall(p, open(f_path).read())

    minn, maxx, meann = getSeqLength(open(f_path).readlines())
    jsonData[name] = {
        "path": f_path,
        "n_sequences": len(description_lines),
        "sequences": [i for i in description_lines],
        "mean_length_sequence": meann,
        "min":minn,
        "max":maxx
    }

# with open(mtdt_seq, "w") as f:
#     json.dump(jsonData, f, indent=4)

with open(PATH_METADATA_REF, "w") as f:
    for i in jsonData.keys():
        del jsonData[i]["sequences"]
    json.dump(jsonData, f, indent=4)
