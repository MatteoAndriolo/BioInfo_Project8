import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

from _config import PATH_METADATA_REF, MASON_SIMULATOR, DIR_READS_SIMLORD, DIR_READS_MASON, MAX_LONG, \
    MIN_LONG, STEP_LONG, RANGE_SHORT, COVERAGE, MAX_SHORT, DIR_TEMP

path_metadata_ref = PATH_METADATA_REF
dir_reads_simlord = DIR_READS_SIMLORD
dir_reads_mason = DIR_READS_MASON


def getNumberReads(coverage, read_lenghts, genome_size) -> int:
    '''coverage=read_length*number_reads/genome_size'''
    return int(coverage * genome_size / read_lenghts)


def count_reads(path: Path) -> int:
    with open(path, "r") as f:
        reads_metadata = f.read().count("@")  # simlord
    return reads_metadata


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
    for nreads in range(MIN_LONG, MAX_LONG, STEP_LONG):
        fread = dir_reads_simlord / str(n) / name
        command = f'simlord ' \
                  f'--fixed-readlength {nreads}' \
                  f'--read-reference {fref}' \
                  f'-c {c}' \
                  f'-pi {pi}' \
                  f'-pd {pd}' \
                  f'-ps {ps}' \
                  f'--no-sam {fread}'
        os.system(f'echo "{command}"')
        os.system(command)

        out.append([name + '.fastq', {
            "path": str(fread) + ".fastq",
            'path_ref': str(fref)
        }])
    return out


def generateTempFileWithMinimumFragmentLenghts(path: Path, nreads: int) -> Path:
    path_temp = DIR_TEMP / (Path(path).name)
    min_lines = nreads / 80
    with open(path, "r") as file, open(path_temp, "w") as tempfile:
        frag = []
        for line in file:
            if line[0] != ">":
                frag.append(line)
            elif len(frag) > min_lines:
                tempfile.writelines(frag)
                frag = []
            else:
                frag = []
    return path_temp


def gen_read_mason(data) -> list:
    out = []
    name: str = data[0]
    metadata: dict = data[1]
    fref: str = metadata["path"]
    # path_temp = DIR_TEMP / (Path(fref).name)

    for nreads in RANGE_SHORT:
        fread = dir_reads_mason / str(nreads) / (name + ".fq")
        c = getNumberReads(COVERAGE, nreads, metadata["mean_length_sequence"])
        command = f'{MASON_SIMULATOR}' \
                  f' -seed 0 ' \
                  f'--num-threads {int(cpu_count() / 2)} ' \
                  f'--num-fragments {c} ' \
                  f'--illumina-read-length {nreads} ' \
                  f'-ir {generateTempFileWithMinimumFragmentLenghts(Path(fref), nreads)} ' \
                  f'-o {fread} '

        os.system(f'echo "{command}"')
        os.system(command)

        out.append([name + '.fastq', {
            "path": str(fread),
            'path_ref': str(fref),
            "nreads": count_reads(str(fread))
        }])

    return out


if __name__ == "__main__":
    with open(path_metadata_ref) as file_metadata:
        metadata_ref = json.load(file_metadata)

    # # multitread read simiojn
    # with Pool(cpu_count() * 2) as p:
    #     jsonDataSimlord = [{} for i in RANGE_LONG]
    #     for par in p.map(gen_read_simlord, metadata_ref.items()):
    #         for i, pa in enumerate(par):
    #             jsonDataSimlord[i][pa[0]] = pa[1]
    #
    # for i, n in enumerate(RANGE_LONG):
    #     with open(dir_reads_simlord / str(n) / "metadata.json", "w") as f:
    #         json.dump(jsonDataSimlord[i], f, indent=4)

    with Pool(cpu_count()) as p:
        jsonDataMason = [{} for i in RANGE_SHORT]
        for par in p.map(gen_read_mason, metadata_ref.items()):
            for i, pa in enumerate(par):
                jsonDataMason[i][pa[0]] = pa[1]

    for i, n in enumerate(RANGE_SHORT):
        with open(dir_reads_mason / str(n) / "metadata.json", "w") as f:
            json.dump(jsonDataMason[i], f, indent=4)
