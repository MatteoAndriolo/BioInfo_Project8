import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

from _config import PATH_METADATA_REF, MASON_SIMULATOR, DIR_READS_MASON, RANGE_SHORT, COVERAGE

path_metadata_ref = PATH_METADATA_REF
dir_reads_mason = DIR_READS_MASON


def getNumberReads(coverage, read_lenghts, genome_size) -> int:
    '''coverage=read_length*number_reads/genome_size'''
    return int(coverage * genome_size / (read_lenghts * 10))


def count_reads(path: Path) -> int:
    try:
        with open(path, "r") as f:
            reads_metadata = f.read().count("@")  # simlord
            return reads_metadata
    except:
        return 0


def _gen_read_mason(data) -> list:
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
                  f'--fragment-mean-size {nreads * 3} ' \
                  f'--illumina-read-length {nreads} ' \
                  f'-ir {fref} ' \
                  f'--num-fragments {c} ' \
                  f'-o {fread} '

        os.system(f'echo "{command}"')
        try:
            os.system(command)

            out.append([name + '.fastq', {
                "path": str(fread),
                'path_ref': str(fref),
                "nreads": count_reads(fread),
                "command": command
            }])
            if count_reads(fread) == 0:
                os.remove(fread)
        except:
            try:
                os.remove(fread)
            except:
                print("already removed")
            out.append([name + '.fastq', {
                "path": str(fread),
                'path_ref': str(fref),
                "nreads": 0,
                "command": command
            }])
    return out


if __name__ == "__main__":
    with open(path_metadata_ref) as file_metadata:
        metadata_ref = json.load(file_metadata)

    with Pool(cpu_count()) as p:
        jsonDataMason = [{} for i in RANGE_SHORT]
        for par in p.map(gen_read_mason, metadata_ref.items()):
            for i, pa in enumerate(par):
                jsonDataMason[i][pa[0]] = pa[1]

    for i, n in enumerate(RANGE_SHORT):
        with open(dir_reads_mason / str(n) / "metadata.json", "w") as f:
            print(i, pa)
            json.dump(jsonDataMason[i], f, indent=4)
