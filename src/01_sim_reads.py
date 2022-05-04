from definitions import READS_DIR, REF_DIR
import json
from multiprocessing import Pool
import os
from pathlib import Path

# support data
dir_reads=Path(os.path.join(READS_DIR, "reads50_simlord"))
dir_reads.mkdir(parents=True, exist_ok=True)
path_metadata_reads=os.path.join(dir_reads,"metadata.json")
metadata_ref=json.load(open(os.path.join(REF_DIR,"metadata.json")))
jsonData={}


# def function generate data for multithreading
def gen_read(data):
    name=data[0]
    metadata=data[1]
    # SimLoRD parameters
    c=20
    pi=0.11
    pd=0.4
    ps=0.01
    fref=metadata["path"]
    fread=dir_reads/name
    # execute SimLoRD
    os.system(f'echo "simlord --read-reference {fref} -c {c} -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}"')
    os.system(f'simlord --read-reference {fref} -c 20 -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}')

    return (name+'.fastq', {
        "path":str(fread),
        'path_ref':str(fref),
        "c":c,
        'pi':pi,
        'pi':pi,
        'pd':pd,
        'ps':ps,
    })

# multitread read simiojn
with Pool(os.cpu_count()*2) as p:
    for par in p.map(gen_read, metadata_ref.items()):
        jsonData[par[0]]=par[1]

""" iterative  with no metadata
for name in metadata:
    fref=metadata[name]["path"]
    fread=dir_reads/name
    pi=0.11
    pd=0.4
    ps=0.01
    
    os.system(f'echo "simlord --read-reference {fref} -c 20 -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}"')
    os.system(f'simlord --read-reference {fref} -c 20 -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}')
"""


with open(path_metadata_reads, "w") as f:
    json.dump(jsonData, f, indent=4)
