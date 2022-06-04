# support data
import os
from pathlib import Path

ROOT_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
MASON_SIMULATOR = ROOT_DIR / "tools" / "mason2" / "bin" / "mason_simulator"
EXTENSION_REF = ".fna"
MIN_FRAG_LENGTH = 15000
############################################### ALL NORMAL
# REF
DIR_TEMP = ROOT_DIR / ".temp"
DIR_REF = ROOT_DIR / "ref" / "ref_50"
PATH_METADATA_REF = DIR_REF / "metadata.json"
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

# ############################################### REDUCED
# # REF
# SUFFIX = "_reduced"
# DIR_TEMP_REDUCED = ROOT_DIR / (".temp" + SUFFIX)
# DIR_REF_REDUCED = ROOT_DIR / "ref" / ("ref_50" + SUFFIX)
# PATH_METADATA_REF_REDUCED = DIR_REF_REDUCED / "metadata.json"
# # READS
# DIR_READS_REDUCED = ROOT_DIR / "reads" / ("reads_50" + SUFFIX)
# DIR_READS_SIMLORD_REDUCED = DIR_READS_REDUCED / "simlord"
# DIR_READS_MASON_REDUCED = DIR_READS_REDUCED / "mason"
# # FASTA
# DIR_FASTA_REDUCED = ROOT_DIR / "fasta" / ("fasta_50" + SUFFIX)
# DIR_FASTA_SIMLORD_REDUCED = DIR_FASTA_REDUCED / "simlord"
# DIR_FASTA_MASON_REDUCED = DIR_FASTA_REDUCED / "mason"

#
# onfig
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

COVERAGE = 20
'''
Mason2 Config
'''

if __name__ == "__main__":
    DIR_RESULTS_MASON.mkdir(parents=True, exist_ok=True)
    DIR_RESULTS_SIMLORD.mkdir(parents=True, exist_ok=True)
    # DIR_TEMP.mkdir(parents=True, exist_ok=True)
    # DIR_REF_REDUCED.mkdir(parents=True, exist_ok=True)
    for n in RANGE_LONG:
        (DIR_READS_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_SIMLORD / str(n)).mkdir(parents=True, exist_ok=True)
        # (DIR_READS_SIMLORD_REDUCED / str(n)).mkdir(parents=True, exist_ok=True)
        # (DIR_FASTA_SIMLORD_REDUCED / str(n)).mkdir(parents=True, exist_ok=True)

    for n in RANGE_SHORT:
        (DIR_READS_MASON / str(n)).mkdir(parents=True, exist_ok=True)
        (DIR_FASTA_MASON / str(n)).mkdir(parents=True, exist_ok=True)
        # (DIR_READS_MASON_REDUCED / str(n)).mkdir(parents=True, exist_ok=True)
        # (DIR_FASTA_MASON_REDUCED / str(n)).mkdir(parents=True, exist_ok=True)
    # TODO possible implementation of file that automaticaly generate simulator configs
