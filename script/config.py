# support data
import json
from pathlib import Path

# support data
dir_ref=Path("../ref/ref_50")
dir_reads=Path("../reads/reads_50/")
dir_reads.mkdir(parents=True, exist_ok=True)
path_metadata="../reads/reads_50/metadata.json"

#mtdt_ref=json.load(open("../ref/ref_50/metadata.json"))
#mtdt_reads=json.load(open("../reads/reads_50/metadata.json"))




'''
Mason2 Config
'''


if __name__=="__main__":
    pass 
    # TODO possible implementation of file that automaticaly generate simulator configs
