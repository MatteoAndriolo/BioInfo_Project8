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
DIR_READS_NOSIM = DIR_READS / "nosim"

# FASTA
DIR_FASTA = Path(ROOT_DIR / "fasta" / "fasta_50")
DIR_FASTA_SIMLORD = DIR_FASTA / "simlord"
DIR_FASTA_MASON = DIR_FASTA / "mason"
DIR_FASTA_NOSIM= DIR_FASTA / "nosim"

MASON_SIMULATOR = ROOT_DIR / "tools" / "mason2" / "bin" / "mason_simulator"

# config
MIN_LONG = 1000
MAX_LONG = 10001
STEP_LONG = 1000
# MAX_LONG = MIN_LONG + 1 #+ STEP_LONG
RANGE_LONG = range(MIN_LONG, MAX_LONG, STEP_LONG)

MIN_SHORT = 100
MAX_SHORT = 1001
STEP_SHORT = 100
# MAX_SHORT = MIN_SHORT + 1 # + STEP_SHORT
RANGE_SHORT = range(MIN_SHORT, MAX_SHORT, STEP_SHORT)

RANGE = [50, 75, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 3000, 5000, 7500, 1000, 12500, 15000, 20000,
         30000, 45000]
COVERAGE = 20
TEMP = ROOT_DIR / "temp"
'''
Mason2 Config
'''

if __name__ == "__main__":
    for n in RANGE:
        (DIR_READS_NOSIM / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_NOSIM/ str(n)).mkdir(parents=True, exist_ok=True)
    for n in RANGE_LONG:
        (DIR_READS_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
    for n in RANGE_SHORT:
        (DIR_READS_MASON / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_MASON / str(n)).mkdir(parents=True, exist_ok=True)
    # TODO possible implementation of file that automaticaly generate simulator configs
