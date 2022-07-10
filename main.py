from src.config import DIR_REF
from src.sim_reads import generateReads

if __name__ == "__main__":
    dir_referencefiles = DIR_REF
    files = generateReads(dir_referencefiles, minlenght=100, maxlenght=10000)
    print(files)
