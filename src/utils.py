import json
import logging
from multiprocessing import Semaphore
import shutil
import subprocess
from pathlib import Path


def _getNumberReads(coverage, read_lenghts, genome_size) -> int:
    """coverage=read_length*number_reads/genome_size"""
    return int(coverage * genome_size / read_lenghts)


def _raiseParameterError(msg: str):
    logging.getLogger().error(msg)
    raise Exception(f"ParameterError: {msg}")


def _count_lines(path: Path) -> int:
    '''
    Count lines of a file
    :param path: path of file
    :return: int number of lines
    '''
    print(str(path))
    try:
        count = int(
            subprocess.check_output(["wc", "-l", path]).decode("utf-8").split(" ")[0]
        )
        return count
    except:
        print(f"{path} not opened")
        return 0

def updateJson(file:str|Path, key:int|str, value:dict|list, semaphore:Semaphore)-> None:
    """Safely update json files

    Args:
        file (str | Path): path Json file to update 
        key (int | str): key
        value (dict | list): value 
        semaphore (Semaphore): semaphore for safe multithreading 
    """
    semaphore.acquire()
    shutil.copy2(file, file.parent/f"{file.name}.bkp")
    try:
        mtdt:dict=json.load(open(file,"r"))
        mtdt[key]=value
        json.dump(mtdt,open(file,"w"),indent=4)
    except:
        shutil.move(file.parent/f"{file.name}.bkp",file)
    semaphore.release()


