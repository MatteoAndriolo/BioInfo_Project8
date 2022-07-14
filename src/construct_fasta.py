import json
import logging
import os
import shutil
import subprocess
import time
from multiprocessing import Pool, Lock
from pathlib import Path

from config import DIR_FASTA_MASON, DIR_FASTA_SIMLORD, DIR_READS, DIR_FASTA, RANGE, PATH_METADATA_FASTA


def _updatejsonfasta(lread_str: str, data: dict):
    """
    Util for multithread update of JSON files
    @param lread_str: key dictionary
    @param data: value
    @return:
    """
    with lock:
        if not os.path.exists(path_metadata_fasta):
            json.dump({},open(path_metadata_fasta,"w"))
        if not os.path.exists(path_metadata_empty):
            json.dump({},open(path_metadata_empty,"w"))
        shutil.copy2(path_metadata_fasta, path_metadata_fasta.parent / f"{path_metadata_fasta.name}.bkp")
        shutil.copy2(path_metadata_empty, path_metadata_empty.parent / f"{path_metadata_empty.name}.bkp")

        try:
            mtdt: dict = json.load(open(path_metadata_fasta, "r"))
            mtdt[lread_str] = data["generated"]
            json.dump(mtdt, open(path_metadata_fasta, "w"), indent=4, sort_keys=True)
        except Exception as e:
            logging.error(f"updateJsonFasta {lread_str}: {e} -> {data}")

        if data["empty"]["n"] != 0:
            try:
                mtdt2: dict = json.load(open(path_metadata_empty, "r"))
                mtdt2[lread_str] = data["empty"]
                json.dump(mtdt2, open(path_metadata_empty, "w"), indent=4, sort_keys=True)
            except Exception as e:
                logging.error(f"updateJsonEmptyRead {lread_str}: {e} -> {data}")
        time.sleep(0.01)


def _generateFastaAndTruth(lreads: int) -> None:
    """
    Generate one fasta and truth file starting from reads
    Format fasta: ">S0R<nr>\n<sequence>"
    Format truth: "S0R<nr>\n<taxid>"
    @param lreads: read length of sequences to be inserted in fasta file
    @return: None
    """
    lreads_str = f"{lreads:0>6}"
    path_fasta = str(dir_fasta / f"{lreads_str}.fasta")
    path_truth = str(dir_fasta / f"{lreads_str}.truth")
    paths = []

    # generate list files to merge for each lenght
    empty = []
    dictPaths = {}
    mtdt = json.load(open(dir_reads / "_metadata.json"))
    for taxid_str, data in mtdt.items():
        data: dict = data[lreads_str]
        if data["nreads"] == 0:
            empty.append(taxid_str)
            # continue
        else:
            paths.append(data["path"])
            dictPaths[str(data["path"])] = [taxid_str, lreads_str]

    # nonrelPaths = paths.copy()
    # paths = [os.path.relpath(a) for a in paths]

    # START ACTUAL WORK
    '''merge reads
        <sequence>\t<taxid>
    '''
    logging.info(f"START: merge {lreads} reads")
    start_time = time.time()
    os.system("echo '' > .temp/outlen".replace("len", lreads_str))
    for i, path in enumerate(paths, start=0):
        # keep only the line containing the simulated reads (1 live every 4, strarting from line 2) and pair it with his true taxid
        if i == 0:
            comamnd_merge_files = '''sed -n '2~4p' pathin | awk '{print $s "\\ttaxid"}' > .temp/outlen''' \
                .replace("pathin", path) \
                .replace("taxid", str(int(dictPaths[path][0]))) \
                .replace("len", lreads_str)
        else:
            comamnd_merge_files = '''sed -n '2~4p' pathin | awk '{print $s "\\ttaxid"}' >> .temp/outlen''' \
                .replace("pathin", path) \
                .replace("taxid", str(int(dictPaths[path][0]))) \
                .replace("len", lreads_str)
        logging.debug(comamnd_merge_files)
        os.system(comamnd_merge_files)  ######

    logging.info(f"ENDED merge: {lreads} in {time.time() - start_time}")

    '''add fasta prefix 
        >S0R<nr>\t<sequence>\t<taxid>
    '''
    logging.info(f"START: prefix {lreads} ")
    start_time = time.time()
    # add at the beginning of each line prefix S0R with read number
    command_add_prefix = '''awk '{print ">S0R" NR "\\t" $s}' .temp/outlen > .temp/outlen2''' \
        .replace("len", lreads_str)
    logging.debug(command_add_prefix)
    os.system(command_add_prefix)  ######
    logging.info(f"ENDED: prefix {lreads} in {time.time() - start_time}")

    ''' generate fasta file
        >S0R<nr>\n<sequence>
    '''
    start_time = time.time()
    logging.info(f"START: generate fasta file {lreads} ")
    # extraxt first and second columns, replace tab modulator with new line
    command_add_prefix = f"cut -f 1,2 .temp/out{lreads_str}2 | sed 's/\\t/\\n/' > {path_fasta}"
    logging.info(command_add_prefix)
    os.system(command_add_prefix)  ######
    logging.info(f"ENDED: generate fasta file {lreads} in {time.time() - start_time}")

    ''' generate truth file
        S0R<nr>\t<taixd>
    '''
    logging.info(f"START: generate truth file {lreads} ")
    start_time = time.time()
    logging.info(f" {lreads} ")
    # extract first and third columns, keep tab modulator, remove > in prefix
    command_add_prefix = f"cut -f 1,3 .temp/out{lreads_str}2 |sed 's/^.//'  > {path_truth}"
    logging.info(command_add_prefix)
    os.system(command_add_prefix)  ######
    logging.info(f"ENDED: generate truth file {lreads} in {time.time() - start_time}")

    # generate metadata
    lenTruth = int(subprocess.check_output(["wc", "-l", path_truth]).decode("utf-8").split(" ")[0])
    _updatejsonfasta(lreads_str, {"empty": {"n": len(empty), "list": empty},
                                  "generated": {"path_fasta": str(path_fasta), "path_truth": str(path_truth),
                                                "nreads": lenTruth}})


def regenerateMetadata():
    """
    Generate only metadata from fasta files

    @return:
    """
    if 1000 in range:
        range.pop(range.index(1000))
        range.extend([999, 1001])

    for lreads in range:
        lreads_str = f"{lreads:0>6}"
        path_fasta = str(dir_fasta / f"{lreads_str}.fasta")
        path_truth = str(dir_fasta / f"{lreads_str}.truth")
        paths = []
        logging.info(f"START {lreads_str}: generation metadata")

        # generate list files to merge for each lenght
        empty = []
        dictPaths = {}
        mtdt = json.load(open(dir_reads / "_metadata.json"))
        for taxid_str, data in mtdt.items():
            data: dict = data[lreads_str]
            if data["nreads"] == 0:
                empty.append(taxid_str)
                # continue
            else:
                paths.append(data["path"])
                dictPaths[str(data["path"])] = [taxid_str, lreads_str]

        # generate metadata
        lenTruth = int(subprocess.check_output(["wc", "-l", path_truth]).decode("utf-8").split(" ")[0])
        _updatejsonfasta(lreads_str, {"empty": {"n": len(empty), "list": empty},
                                      "generated": {"path_fasta": str(path_fasta), "path_truth": str(path_truth),
                                                    "nreads": lenTruth}})


def _init_child_job(lock_):
    global lock
    lock = lock_


def generateFastaAndTruth():
    """
    Starting point for multithread generation of fasta and truth files.
    @return:
    """
    os.system("mkdir .temp")
    datareads:dict=json.load(open(dir_reads/"_metadata.json","r"))
    datareads=datareads[list(datareads.keys())[0]]
    range_reads:list=list(datareads.keys())
    lock = Lock()
    with Pool(5, initializer=_init_child_job, initargs=(lock,)) as p:
        start_time = time.time()
        if 1000 in range_reads:
            range_reads.pop(range_reads.index(1000))
            range_reads.extend([999, 1001])
        p.map(_generateFastaAndTruth, range_reads)
        print(time.time() - start_time)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    dir_reads: Path = DIR_READS
    dir_fasta: Path = DIR_FASTA
    dir_fasta_mason: Path = DIR_FASTA_MASON
    dir_fasta_simlord: Path = DIR_FASTA_SIMLORD
    path_metadata_fasta: Path = PATH_METADATA_FASTA
    path_metadata_empty: Path = dir_fasta / "_empty.json"
    # range_reads = RANGE
    # semaphore_jsonReadsMTDT = Semaphore(1)


    generateFastaAndTruth()
    regenerateMetadata()
