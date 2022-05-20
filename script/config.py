# support data
import os
from pathlib import Path

# support data
ROOT_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
DIR_REF = Path(ROOT_DIR / "ref" / "ref_50")
PATH_METADATA_REF = DIR_REF / "metadata.json"
EXTENSION_REF = ".fna"

# READS
DIR_READS = Path(ROOT_DIR / "reads" / "reads_50")
DIR_READS_SIMLORD = DIR_READS / "simlord"
DIR_READS_MASON = DIR_READS / "mason"

# FASTA
DIR_FASTA = Path(ROOT_DIR / "fasta" / "fasta_50")
DIR_FASTA_SIMLORD = DIR_FASTA / "simlord"
DIR_FASTA_MASON = DIR_FASTA / "mason"

MASON_SIMULATOR = ROOT_DIR / "tools" / "mason2" / "bin" / "mason_simulator"

# config
MIN_LONG = 1000
# MAX_LONG = 10001
STEP_LONG = 1000
MAX_LONG = MIN_LONG + 1 #+ STEP_LONG
RANGE_LONG = range(MIN_LONG, MAX_LONG, STEP_LONG)


MIN_SHORT = 100
# MAX_SHORT = 1001
STEP_SHORT = 100
MAX_SHORT = MIN_SHORT + 1 # + STEP_SHORT
RANGE_SHORT = range(MIN_SHORT, MAX_SHORT, STEP_SHORT)

'''
Mason2 Config
'''

if __name__ == "__main__":
    for n in RANGE_LONG:
        (DIR_READS_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
    for n in RANGE_SHORT:
        (DIR_READS_MASON / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_MASON / str(n)).mkdir(parents=True, exist_ok=True)
    # TODO possible implementation of file that automaticaly generate simulator configs
