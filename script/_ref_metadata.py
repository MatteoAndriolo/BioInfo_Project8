import glob
import json
import os.path
import re
import shutil
import sys
from pathlib import Path

# sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
# or
# sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
# and then add directory to path
sys.path.insert(1, os.path.dirname(shutil.which('xtract')))
import edirect

from _config import DIR_REF, PATH_METADATA_REF, PATH_TAXID_REF

##### SETUP
dir_ref = DIR_REF
path_metadata_ref = PATH_METADATA_REF
#####

##### regex patterns
pat_descriptionLines = re.compile(r'^\>(.*)', re.M)  # description lines pattern search in FASTA files
pat_codename = "N\w_[\w\d]*.[\w\d]?"  # code for contigs
#####


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
    return (min(lengthSeq), max(lengthSeq), int(sum(lengthSeq) / len(lengthSeq)))


def full_ref_metadata():
    jsonData = {}
    for f_path in glob.glob(str(dir_ref / '*.fna')):  # for all .fna files in reference directory
        name = Path(f_path).stem
        if name[-4:] == "_Ref":
            name = name[:-4]

        # extract description lines and contigs ID
        description_lines = re.findall(pat_descriptionLines, open(f_path).read())
        codename = [(re.findall(pat_codename, l))[0] for l in description_lines]

        # fetch taxonIDs
        command = f'efetch -db nuccore -id {",".join(codename)} -format docsum | xtract -pattern DocumentSummary -sep "|" -element TaxId Organism Title'
        out = edirect.pipeline(command)
        # process result
        out = out.split("\n")

        taxids = [a.split("\t")[0] for a in out]
        organism = [a.split("\t")[1] for a in out]
        title = [a.split("\t")[2] for a in out]

        print(taxids, organism, title)

        # sequences
        sequences = {i: [] for i in taxids}
        for t, n1, n2 in zip(taxids, codename, title):
            sequences[t].append({n1: n2})
        if len(sequences) == 1:
            taxid = list(sequences.keys())[0]
        else:
            taxid = sorted(list(sequences.keys()), key=lambda x: taxids.count(x), reverse=True)[0]

        # get statistics contigs
        minn, maxx, meann = getSeqLength(open(f_path).readlines())

        # populate metadata
        jsonData[name] = {
            "path": f_path,
            "taxId": taxid,
            "n_sequences": len(description_lines),
            "sequences": sequences,
            "mean_length_sequence": meann,
            "min": minn,
            "max": maxx
        }

    # dump json
    # with open(DIR_REF / "_newmetadata.json", "w") as f:
    with open(PATH_METADATA_REF) as f:
        json.dump(jsonData, f, indent=4)
    # with open(DIR_REF / "_ncbiTaxonID.json", "w") as f:
    with open(PATH_TAXID_REF) as f:
        json.dump({k: {"taxId": v["taxId"]} for k, v in jsonData.items()}, f, indent=4)


# def transferidfrommetadata():
#     with open(DIR_REF / "_metadata.json", "r") as f:
#         mtdt = json.load(f)
#     with open(DIR_REF / "_ncbiTaxonID.json", "w") as f:
#         json.dump({k: {"taxId": v["taxId"]} for k, v in mtdt.items()}, f, indent=4)


if __name__ == "__main__":
    full_ref_metadata()
    # transferidfrommetadata()
