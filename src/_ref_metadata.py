from multiprocessing import Pool, Semaphore, cpu_count, Lock
from tkinter.messagebox import NO
from tkinter.ttk import Separator
from typing import Tuple

from config import DIR_REF, PATH_METADATA_REF, PATH_TAXID_REF
from utils import updateJson
import glob
import json
import logging
import os.path
import re
import shutil
import sys
from pathlib import Path

# sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
# or
# sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
# and then add directory to path

sys.path.append(os.path.dirname(shutil.which("xtract")))
import edirect


def buildRefMetadata(path: str, taxid: int, organism: str, nsequences: int, sequences: dict, mean: int, minn: int,
                     maxx: int, ) -> dict:
    '''
    JSON
    '''
    return {
        "path": path,
        "taxid": taxid,
        "organism": organism,
        "nsequences": nsequences,
        "sequences": sequences,
        "mean": mean,
        "min": minn,
        "max": maxx,
    }


def getSeqLength(text) -> tuple[int, int, int]:
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


def _generate_ref_metadata(f_path: str | Path) -> tuple[str, dict]:
    # global outfile
    # outfile:str
    # global semaphoreJsonUpdate
    # semaphoreJsonUpdate:Semaphore
    # description lines pattern search in FASTA files
    pattern_descriptionLines = re.compile(r"^\>(.*)", re.M)
    pattern_codename = "N\w_[\w\d]*.[\w\d]?"  # code for contigs
    description_lines = re.findall(pattern_descriptionLines, open(f_path).read())
    codename = [(re.findall(pattern_codename, l))[0] for l in description_lines]

    # fetch taxonIDs
    command = f'efetch -db nuccore -id {",".join(codename)} -format docsum | xtract -pattern DocumentSummary -sep "|" -element TaxId Organism Title'
    out = edirect.pipeline(command)
    # process result
    out = out.split("\n")

    taxids = [a.split("\t")[0] for a in out]
    organisms = [a.split("\t")[1] for a in out]
    titles = [a.split("\t")[2] for a in out]

    logging.debug(f"{taxids}, {organisms}, {titles}")

    # sequences
    sequences = {i: [] for i in taxids}
    for t, n1, n2 in zip(taxids, codename, titles):
        sequences[t].append({n1: n2})

    taxid: int = sorted(
        list(sequences.keys()), key=lambda x: taxids.count(x), reverse=True
    )[0]
    organism: str = sorted(
        set(organisms), key=lambda x: organisms.count(x), reverse=True
    )[0]
    title: str = sorted(set(titles), key=lambda x: titles.count(x), reverse=True)[0]

    minn, maxx, meann = getSeqLength(open(f_path).readlines())
    newpath = (
            dir_ref
            / f"{taxid:0>7}-{organism.replace(' ', '_').replace('/', '').replace('.', '')}.fna"
    )

    # rename genome file 
    shutil.copy(f_path, newpath)

    taxid_str = f"{taxid:0>7}"
    data = buildRefMetadata(
        path=str(newpath),
        taxid=taxid,
        organism=organism,
        nsequences=len(description_lines),
        sequences=sequences,
        mean=meann,
        minn=minn,
        maxx=maxx,
    )

    updateJson(taxid_str, data)

    # # with open(DIR_REF / "_ncbiTaxonID.json", "w") as f:
    # with open(PATH_TAXID_REF, "w") as f:
    #     json.dump({k: {"taxid": v["taxid"]} for k, v in jsonData.items()}, f, indent=4)

    return taxid_str, data


def _init_child_job(lock_):
    global lock
    lock = lock_


def generateReferenceGenomesMetadata(folder: str | Path, extension: list[str] = (".fna",), force: bool = False,
                                     outfile: str | Path = None) -> dict:
    """Generate reference metadata for all files in folder with extension.

    Args:
        folder (str | Path): folder containing reference files genomes
        extension (list[str], optional): extension of reference files. Defaults to (".fna",).
        force (bool, optional): Overwrite metadata. Defaults to False.
        outfile (str | Path, optional): output path. Defaults to folder.

    Returns:
        dict: JSON metadata
    """
    if outfile == None:
        outfile = Path(folder) / "_metadata.json"
    else:
        outfile = Path(outfile)
    outfile.parent.mkdir(exist_ok=True, parents=True)

    try:
        mtdtDict = json.load(open(outfile, "r"))
    except:
        mtdtDict: dict = {}

    files = []
    for ext in extension:
        for path in glob.glob(str(Path(folder) / f"*{ext}")):
            files.append(path)

    # semaphoreJsonUpdate = Semaphore(1)
    lock = Lock()
    with Pool(cpu_count(), initializer=_init_child_job, initargs=(lock, outfile,)) as p:
        for taxid_str, data in p.map(_generate_ref_metadata, files):
            mtdtDict[taxid_str] = data

    return mtdtDict


# def getTIDFromMetadata():
#    """_summary_
#    """
#    with open(DIR_REF / "_metadata.json", "r") as f:
#        mtdt = json.load(f)
#    with open(DIR_REF / "_ncbiTaxonID.json", "w") as f:
#        json.dump({k: {"taxid": v["taxid"]} for k, v in mtdt.items()}, f, indent=4)


if __name__ == "__main__":
    dir_ref = DIR_REF
    path_metadata_ref = PATH_METADATA_REF
    generateReferenceGenomesMetadata(dir_ref, force=True, outfile=path_metadata_ref)
