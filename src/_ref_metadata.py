import glob
import json
import logging
import os.path
import re
import shutil
import sys
from multiprocessing import Pool, cpu_count, Lock
from pathlib import Path
from typing import Tuple, List, Union

from config import DIR_REF, PATH_METADATA_REF

# sh -c "$(curl -fsSL ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
# or
# sh -c "$(wget -q ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
# and then add directory to path

sys.path.append(os.path.dirname(shutil.which("xtract")))
import edirect


lock=Lock()
def _updateJson(file: Union[str, Path], key: Union[int, str], value: Union[dict, list]) -> None:
    """Safely update json files

    Args:
        file (str | Path): path Json file to update
        key (int | str): key
        value (dict | list): value
        semaphore (Semaphore): semaphore for safe multithreading
    """
    global lock
    with lock:
        # semaphore.acquire()
        if os.path.exists(file):
            shutil.copy2(file, file.parent / f"{file.name}.bkp")
        else:
            json.dump({},open(file,"w"))
        try:
            mtdt: dict = json.load(open(file, "r"))
            mtdt[key] = value
            json.dump(mtdt, open(file, "w"), indent=4)
            logging.debug(f"UPDATE JSON:{key} json updated succesfully")
        except Exception as e:
            logging.error(f"NOTUPDATED JSON: {key} json failed {e}")
            if os.path.exists(file):
                shutil.move(file.parent / f"{file.name}.bkp", file)
        # semaphore.release()


def _buildRefMetadata(path: str, taxid: int, organism: str, nsequences: int, sequences: dict, mean: int, minn: int,
                      maxx: int, ) -> dict:
    """
    Build json metadata entry given appropriate data from a reference genome

    :param path:
    :param taxid:
    :param organism:
    :param nsequences:
    :param sequences:
    :param mean:
    :param minn:
    :param maxx:
    :return:
    """
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


def _getSeqLength(text) -> Tuple[int, int, int]:
    """
    Read genome data and extract statistics about reference genome
    :param text: input read from file
    :return: minimum, maximum, mean sequence length
    """
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
    return min(lengthSeq), max(lengthSeq), int(sum(lengthSeq) / len(lengthSeq))


def _generate_ref_metadata(f_path: Union[str, Path]) -> Tuple[str, dict]:
    """
    Private function used in multithreading.
    Generate json metadata from a file


    :param f_path: path of reference genome file
    :return: taxonomicid_str(str), data(dict)
    """
    # global outfile
    # outfile:str
    # global semaphoreJsonUpdate
    # semaphoreJsonUpdate:Semaphore
    # description lines pattern search in FASTA files
    logging.info(f"START: {f_path}")
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

    minn, maxx, meann = _getSeqLength(open(f_path).readlines())
    newpath = (
            dir_ref
            / f"{taxid:0>7}-{organism.replace(' ', '_').replace('/', '').replace('.', '')}.fna"
    )

    logging.debug(f"GENERATING {taxid}: metadata fetched succesfully")
    # rename genome file
    try:
        shutil.copy(f_path, newpath)
    except:
        pass

    taxid_str = f"{taxid:0>7}"
    data = _buildRefMetadata(
        path=str(newpath),
        taxid=taxid,
        organism=organism,
        nsequences=len(description_lines),
        sequences=sequences,
        mean=meann,
        minn=minn,
        maxx=maxx,
    )

    logging.info(f"END: {f_path}")
    _updateJson(Path(f_path).parent / "_metadata.json", taxid_str, data)

    # # with open(DIR_REF / "_ncbiTaxonID.json", "w") as f:
    # with open(PATH_TAXID_REF, "w") as f:
    #     json.dump({k: {"taxid": v["taxid"]} for k, v in jsonData.items()}, f, indent=4)

    return taxid_str, data


def _init_child_job(lock_, outfile_, ):
    global lock
    global outfile
    lock = lock_
    outfile = outfile_


def generateReferenceGenomesMetadata(folder: Union[str, Path], extension: List[str] = (".fna",), force: bool = False,
                                     outfile: Union[str, Path] = None) -> dict:
    """
    Generate metadata of reference genomes files contained in folder, having extension and write it inside outfile.
    If metadata already present <force> rewrite.

    @param folder: input folder
    @param extension: extension used for file search inside folder
    @param force: force rewrite of files in folder
    @param outfile: path of metadata file (default to folder/_metadata.json)
    @return: metadata dictionary
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
    logging.debug(f"LIST FILES: {files}")

    # semaphoreJsonUpdate = Semaphore(1)
    lock = Lock()
    with Pool(cpu_count(), initializer=_init_child_job, initargs=(lock, outfile,)) as p:
        for taxid_str, data in p.map(_generate_ref_metadata, files):
            mtdtDict[taxid_str] = data

    return mtdtDict


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    dir_ref = DIR_REF
    path_metadata_ref = PATH_METADATA_REF
    generateReferenceGenomesMetadata(dir_ref, force=True, outfile=path_metadata_ref)
