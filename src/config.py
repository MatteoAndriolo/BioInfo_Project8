# support data
import os
from pathlib import Path

ROOT_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
MASON_SIMULATOR = ROOT_DIR / "tools" / "mason2" / "bin" / "mason_simulator"
EXTENSION_REF = ".fna"

DIR_TEMP = ROOT_DIR / "src/.temp"
# TEST
DIR_TEST = ROOT_DIR / ".test"
DIR_TEST_REF = ROOT_DIR / ".test" / "ref_50"
DIR_TEST_READS = ROOT_DIR / ".test" / "reads_50"
DIR_TEST_READS_MASON = DIR_TEST_READS / "mason"
DIR_TEST_READS_SIMLORD = DIR_TEST_READS / "simlord"
DIR_TEST_FASTA = ROOT_DIR / ".test" / "fasta_50"
DIR_TEST_FASTA_MASON = DIR_TEST_FASTA / "mason"
DIR_TEST_FASTA_SIMLORD = DIR_TEST_FASTA / "simlord"
DIR_TEST_RESULTS = ROOT_DIR / ".test" / "out_50"
DIR_TEST_RESULTS_MASON = DIR_TEST_RESULTS / "mason"
DIR_TEST_RESULTS_SIMLORD = DIR_TEST_RESULTS / "simlord"
listDirTest: list = [
    DIR_TEST_READS_SIMLORD,
    DIR_TEST_READS_MASON,
    DIR_TEST_FASTA_SIMLORD,
    DIR_TEST_FASTA_MASON,
    DIR_TEST_RESULTS_SIMLORD,
    DIR_TEST_RESULTS_MASON,
]

DIR_REF = ROOT_DIR / "ref" / "ref_50"
DIR_READS = ROOT_DIR / "reads" / "reads_50"
DIR_READS_SIMLORD = DIR_READS / "simlord"
DIR_READS_MASON = DIR_READS / "mason"
DIR_FASTA = ROOT_DIR / "fasta" / "fasta_50"
DIR_FASTA_SIMLORD = DIR_FASTA / "simlord"
DIR_FASTA_MASON = DIR_FASTA / "mason"
DIR_RESULTS = ROOT_DIR / "results" / "results_50"
DIR_RESULTS_MASON = DIR_RESULTS / "simlord"
DIR_RESULTS_SIMLORD = DIR_RESULTS / "mason"
listDir: list = [
    DIR_READS_SIMLORD,
    DIR_READS_MASON,
    DIR_FASTA_SIMLORD,
    DIR_FASTA_MASON,
    DIR_RESULTS_SIMLORD,
    DIR_RESULTS_MASON,
]

# METADATA
PATH_METADATA_REF = DIR_REF / "_metadata.json"
PATH_TAXID_REF = DIR_REF / "_ncbiTaxonID.json"
PATH_METADATA_READS = DIR_READS / "_metadata.json"

# config
MIN_LONG = 1000
MAX_LONG = 10001
STEP_LONG = 1000
RANGE_LONG = range(MIN_LONG, MAX_LONG, STEP_LONG)

MIN_SHORT = 100
MAX_SHORT = 1001
STEP_SHORT = 100
RANGE_SHORT = range(MIN_SHORT, MAX_SHORT, STEP_SHORT)

# RANGE=RANGE_SHORT
RANGE = [100, 300, 400, 500, 600, 700, 800, 900, 1000]
# RANGE = [*RANGE_SHORT, *RANGE_LONG]
# RANGE = [200]

MIN_FRAG_LENGTH = 15000
COVERAGE = 20

if __name__ == "__main__":
    for a in [*listDir, *listDirTest]:
        a.mkdir(parents=True, exist_ok=True)
