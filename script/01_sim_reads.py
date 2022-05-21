import json
import os
from multiprocessing import Pool, cpu_count

# support data
from config import PATH_METADATA_REF, MASON_SIMULATOR, DIR_READS_SIMLORD, DIR_READS_MASON, MAX_LONG, \
    MIN_LONG, STEP_LONG, RANGE_SHORT, RANGE_LONG, COVERAGE

metadata_ref = json.load(open(PATH_METADATA_REF))


def getNumberReads(coverage, read_lenghts, genome_size) -> int:
    '''coverage=read_length*number_reads/genome_size'''
    return int(coverage * genome_size / read_lenghts)


# def function multithread
def gen_read_simlord(data) -> list:
    out = []
    name = data[0]
    metadata = data[1]
    # SimLoRD parameters
    c = COVERAGE
    pi = 0.11
    pd = 0.4
    ps = 0.01
    fref = metadata["path"]
    # execute SimLoRD
    for n in range(MIN_LONG, MAX_LONG, STEP_LONG):
        fread = DIR_READS_SIMLORD / str(n) / (name + ".fastq")
        command = f'simlord --fixed-readlength {n} --read-reference {fref} -c {c} -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}'
        os.system(f'echo "{command}"')
        os.system(command)

        out.append([name + '.fastq', {
            "path": str(fread),
            'path_ref': str(fref)
            # "c": c,
            # 'pi': pi,
            # 'pd': pd,
            # 'ps': ps,
        }])
    return out


def gen_read_mason(data) -> list:
    out = []
    name = data[0]
    metadata = data[1]
    fref = metadata["path"]

    for n in range(MIN_LONG, MAX_LONG, STEP_LONG):
        fread = DIR_READS_MASON / str(n) / (name + ".fq")
        command = f'{MASON_SIMULATOR} -seed 0 --num-threads {cpu_count()} -ir {fref} --num-fragments {getNumberReads(COVERAGE, n, metadata["mean_length_sequence"])} -o {fread} '
        os.system(f'echo "{command}"')
        os.system(command)

        out.append([name + '.fastq', {
            "path": str(fread),
            'path_ref': str(fref)
        }])

    return out


if __name__ == "__main__":
    # multitread read simiojn
    with Pool(cpu_count() * 2) as p:
        jsonDataSimlord = [{} for i in RANGE_LONG]
        for par in p.map(gen_read_simlord, metadata_ref.items()):
            for i, pa in enumerate(par):
                jsonDataSimlord[i][pa[0]] = pa[1]
    with Pool(cpu_count() * 2) as p:
        jsonDataMason = [{} for i in RANGE_SHORT]
        for par in p.map(gen_read_mason, metadata_ref.items()):
            for i, pa in enumerate(par):
                jsonDataMason[i][pa[0]] = pa[1]

for i, n in enumerate(RANGE_LONG):
    with open(DIR_READS_SIMLORD / str(n) / "metadata.json", "w") as f:
        json.dump(jsonDataSimlord[i], f, indent=4)
for i, n in enumerate(RANGE_SHORT):
    with open(DIR_READS_MASON / str(n) / "metadata.json", "w") as f:
        json.dump(jsonDataMason[i], f, indent=4)
