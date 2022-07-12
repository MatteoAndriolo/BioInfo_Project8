import json
import json
import logging
import os
import shutil
import time
from multiprocessing import cpu_count, Pool, Lock
from pathlib import Path
from threading import Semaphore

from config import PATH_METADATA_REF, MASON_SIMULATOR, DIR_READS_SIMLORD, DIR_READS_MASON, COVERAGE, DIR_REF, \
    PATH_METADATA_READS, RANGE
from utils import _count_lines, _getNumberReads, _raiseParameterError


def _updateJsonRead(taxid_str, lread_str, data):
    with lock:
        shutil.copy2(path_metadata_reads, path_metadata_reads.parent / f"{path_metadata_reads.name}.bkp")
        try:
            mtdt: dict = json.load(open(path_metadata_reads, "r"))
            if taxid_str in mtdt.keys():
                mtdt[taxid_str][lread_str] = data
            else:
                mtdt[taxid_str] = {lread_str: data}
            json.dump(mtdt, open(path_metadata_reads, "w"), indent=4, sort_keys=True)
            logging.info(f"updateJson: {taxid_str} {lread_str}")
            logging.info(
                f"updateJson: {len([k for kt in mtdt.keys() for k in mtdt[kt].keys()])}"
            )
        except Exception as e:
            logging.error(f"updateJsonRead ERROR {taxid_str}, {lread_str}, {data}")
            logging.error(f"updateJsonRead ERROR: {e}")
        time.sleep(0.05)


def _gen_read_simlord(data: dict) -> None:
    path: str = data["path"].replace("(", "\(").replace(")", "\)")
    taxid: int = int(data["taxid"])
    taxid_str = f"{taxid:0>7}"
    lread: int = data["lread"]
    lread_str = f"{lread:0>6}"
    # SimLoRD parameters
    c = COVERAGE
    # pi = 0.11
    # pd = 0.04
    # ps = 0.01
    pi = 0.001
    pd = 0.001
    ps = 0.004

    (dir_reads_simlord / lread_str).mkdir(parents=True, exist_ok=True)
    fread = dir_reads_simlord / lread_str / f"{taxid_str}"

    command = f'simlord --fixed-readlength {lread} --read-reference "{path}" -c {c} -pi {pi} -pd {pd} -ps {ps} --no-sam "{fread}"'

    if data["togenerate"]:
        # execute SimLoRD
        logging.info(f"SIMLORD_START: {lread_str}-{taxid_str}")
        logging.debug(f"{command}")
        os.system(command)
        logging.info(f"SIMLORD_END: {lread_str}-{taxid_str}")

    fread = f"{fread}.fastq"
    count_reads = int(_count_lines(Path(fread)) / 4)
    _updateJsonRead(
        taxid_str,
        lread_str,
        {"path": str(fread), "nreads": count_reads, "command": str(command)},
    )


def _gen_read_mason(data: dict) -> None:
    fref: str = data["path"]
    taxid: int = int(data["taxid"])
    taxid_str = f"{taxid:0>7}"
    lread: int = data["lread"]
    lread_str = f"{lread:0>6}"

    (dir_reads_mason / lread_str).mkdir(parents=True, exist_ok=True)
    fread = dir_reads_mason / lread_str / f"{taxid_str}.fq"
    c = _getNumberReads(
        coverage=COVERAGE,
        read_lenghts=lread,
        genome_size=data["mean"] * data["nsequences"],
    )
    command = f'{MASON_SIMULATOR} -seed 0 --num-threads {cpu_count()} --fragment-mean-size {lread * 3} --illumina-read-length {lread} -ir "{fref}" --num-fragments {c} -o "{fread}" '

    if data["togenerate"]:
        os.system(f'echo "{command}"')
        logging.debug(f"MAVEN_END: lread {lread}, taxid {taxid}")
        try:
            os.system(command)
            out = [
                taxid_str,
                lread_str,
                {
                    "path": str(fread),
                    "nreads": _count_lines(fread) / 4,
                    "command": str(command),
                },
            ]
            if out[2]["nreads"] == 0:
                os.remove(fread)
            logging.debug(f"MAVEN_END: {lread_str}-{taxid_str}")
        except:
            try:
                os.remove(fread)
            except:
                logging.debug("already removed")
            out = [
                taxid_str,
                lread_str,
                {"path_ref": str(fref), "nreads": 0, "command": str(command)},
            ]
            logging.debug(f"MAVEN_UNSUCCESSFUL: {lread_str}-{taxid_str}")
    else:
        out = [
            taxid_str,
            lread_str,
            {
                "path": str(fread),
                "nreads": _count_lines(fread) / 4,
                "command": str(command),
            },
        ]

    _updateJsonRead(*out)


def _generateReads(data: dict):
    """
    Manages generation reads starting from metadata containing lenght reads to be generated
    :param data: dictionay file containing info reguarding ref genome e lenght reads
    :return: list containing dictionary of reads metadata
    """
    logging.debug("in generate reads")
    lread: int = data["lread"]
    lread_str: str = f"{lread:0>6}"
    taxid: int = data["taxid"]
    taxid_str: str = f"{taxid:0>7}"
    assert (lread > 0)
    if lread < 1000:
        logging.info(f"{lread_str}-{taxid_str}: start simlord")
        _gen_read_simlord(data)
    elif lread > 1000:
        logging.info(f"{lread_str}-{taxid_str}: start mason")
        _gen_read_mason(data)
    else:
        logging.info(f"{lread_str}-{taxid_str}: read lenght is 1000, start both simlord and mason")
        data["lread"] = 999
        _gen_read_simlord(data)
        data["lread"] = 1001
        _gen_read_mason(data)


def _yetToGenerate(nmtdt: dict, oldmtdt: dict) -> bool:
    taxid_str = f"{nmtdt['taxid']:0>7}"
    try:
        if oldmtdt[taxid_str][f"{nmtdt['lread']:0>6}"]["nreads"] != 0:
            logging.debug(f"{taxid_str}-{nmtdt['lread']} skipped because")
            logging.debug(oldmtdt[taxid_str][f"{nmtdt['lread']:0>6}"]["nreads"])
            return False
    except:
        logging.error(f"yetToGenerate: uncached {taxid_str}")
    logging.debug(f"{taxid_str}-{nmtdt['lread']} todo")
    return True


def _calculate_range(minlenght: int = None, maxlenght: int = None):
    if not (minlenght and maxlenght):
        _raiseParameterError("generateReads: Unexpected input")
    assert minlenght <= maxlenght
    if minlenght < 1000 and maxlenght > 1000:
        return [
            *[i for i in range(100, 1000, 100)],
            *[i for i in range(1000, maxlenght + 1, 1000)],
        ]
    elif minlenght >= 1000:
        return list(range(minlenght, maxlenght + 1, 1000))
    elif maxlenght <= 1000:
        return list(range(minlenght, maxlenght + 1, 100))
    else:
        _raiseParameterError("generateReads: Unexpected input")


def _init_child_job(lock_):
    global lock
    lock = lock_


def generateReads(dir_ref: Path, rangelenght: list = None, minlenght: int = None, maxlenght: int = None, ):
    if not rangelenght:
        rangelenght = _calculate_range(minlenght, maxlenght)

    logging.info(f"start generation reads with min:{minlenght} ; max:{maxlenght}")
    logging.info(f"in range {rangelenght}")

    filesPath_ref = [Path(p) for p in dir_ref.glob("*.fna")]
    logging.debug(f"filepaths for reference files: {filesPath_ref}")

    mtdtref = json.load(open(path_metadata_ref, "r"))
    mtdtreads = json.load(open(path_metadata_reads, "r"))
    listReadToDo = []
    for mtdt in mtdtref.values():
        for rl in rangelenght:
            nmtdt: dict = mtdt.copy()
            nmtdt["lread"] = rl
            try:
                del nmtdt["sequences"]
            except:
                pass
            nmtdt["togenerate"] = _yetToGenerate(nmtdt, mtdtreads)
            listReadToDo.append(nmtdt)

    listReadToDo.sort(key=lambda x: x["lread"], reverse=True)

    lock = Lock()
    with Pool(cpu_count(), initializer=_init_child_job, initargs=(lock,)) as p:
        p.map(_generateReads, listReadToDo)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    path_metadata_ref = PATH_METADATA_REF
    path_metadata_reads = PATH_METADATA_READS
    dir_reads_simlord = DIR_READS_SIMLORD
    dir_reads_mason = DIR_READS_MASON
    # semaphore_jsonReadsMTDT = Semaphore(1)
    generateReads(dir_ref=Path(DIR_REF), rangelenght=list(RANGE))
