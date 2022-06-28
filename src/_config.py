# support data
import os
from pathlib import Path

ROOT_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
MASON_SIMULATOR = ROOT_DIR / "tools" / "mason2" / "bin" / "mason_simulator"
EXTENSION_REF = ".fna"
MIN_FRAG_LENGTH = 15000

# REF
DIR_TEMP = ROOT_DIR / ".temp"
DIR_REF = ROOT_DIR / "ref" / "ref_50"
PATH_METADATA_REF = DIR_REF / "_metadata.json"
PATH_TAXID_REF = DIR_REF / "_ncbiTaxonID.json"

# READS
DIR_READS = ROOT_DIR / "reads" / "reads_50"
DIR_READS_SIMLORD = DIR_READS / "simlord"
DIR_READS_MASON = DIR_READS / "mason"

# FASTA
DIR_FASTA = ROOT_DIR / "fasta" / "fasta_50"
DIR_FASTA_SIMLORD = DIR_FASTA / "simlord"
DIR_FASTA_MASON = DIR_FASTA / "mason"

DIR_RESULTS = ROOT_DIR / "results" / "results_50"
DIR_RES_OUT = DIR_RESULTS / "out"
DIR_OUT_MASON = DIR_RES_OUT / "simlord"
DIR_OUT_SIMLORD = DIR_RES_OUT / "mason"

# FASTA DIRECTLY FROM REF
DIR_FASTA_REF = ROOT_DIR / "fasta" / "fasta_ref"

# onfig
MIN_LONG = 1000
MAX_LONG = 10001
STEP_LONG = 1000
RANGE_LONG = range(MIN_LONG, MAX_LONG, STEP_LONG)

MIN_SHORT = 100
MAX_SHORT = 1001
STEP_SHORT = 100
RANGE_SHORT = range(MIN_SHORT, MAX_SHORT, STEP_SHORT)

COVERAGE = 20

def fNumber(number,length=6):
    return f"{number:0{length}%}"

if __name__ == "__main__":
    DIR_OUT_MASON.mkdir(parents=True, exist_ok=True)
    DIR_OUT_SIMLORD.mkdir(parents=True, exist_ok=True)
    for n in RANGE_LONG:
        (DIR_READS_SIMLORD / fNumber(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_SIMLORD / fNumber(n)).mkdir(parents=True, exist_ok=True)
    for n in RANGE_SHORT:
        (DIR_READS_MASON / fNumber(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_MASON / fNumber(n)).mkdir(parents=True, exist_ok=True)
    DIR_FASTA_REF.mkdir(parents=True, exist_ok=True)
    DIR_TEMP.mkdir(parents=True, exist_ok=True)
