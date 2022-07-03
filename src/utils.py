import logging
import subprocess
from pathlib import Path


def _getNumberReads(coverage, read_lenghts, genome_size) -> int:
    """coverage=read_length*number_reads/genome_size"""
    return int(coverage * genome_size / read_lenghts)


def _raiseParameterError(msg: str):
    logging.getLogger().error(msg)
    raise Exception(f"ParameterError: {msg}")


def _count_reads(path: Path) -> int:
    print(str(path))
    try:
        count = int(
            subprocess.check_output(["wc", "-l", path]).decode("utf-8").split(" ")[0]
        )
        return int(count / 4)
    except:
        print(f"{path} not opened")
        return 0
