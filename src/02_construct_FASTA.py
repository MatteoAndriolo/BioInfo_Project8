import json
import logging
import os
import subprocess
import time
from multiprocessing import Semaphore, Pool

from config import DIR_FASTA_MASON, DIR_FASTA_SIMLORD, DIR_READS, DIR_FASTA, RANGE

dir_reads = DIR_READS
dir_fasta = DIR_FASTA
dir_fasta_mason = DIR_FASTA_MASON
dir_fasta_simlord = DIR_FASTA_SIMLORD


def _updateJsonRead(taxid_str: str, lread_str: str, data: dict):
    global semaphore_jsonReadsMTDT
    semaphore_jsonReadsMTDT.acquire()
    try:
        mtdt: dict = json.load(open(path_metadata_fasta, "r"))
        if lread_str in mtdt.keys():
            mtdt[lread_str][taxid_str] = data["generated"]
        else:
            mtdt[lread_str] = {taxid_str: data["generated"]}
        json.dump(mtdt, open(path_metadata_fasta, "w"), indent=4, sort_keys=True)
    except:
        logging.error(f"updateJsonRead ERROR {taxid_str}, {lread_str}, {data}")

    if data["empty"]["n"] != 0:
        try:
            mtdt2: dict = json.load(open(path_metadata_empty, "r"))
            if lread_str in mtdt2.keys():
                mtdt2[lread_str][taxid_str] = data["empty"]
            else:
                mtdt2[lread_str] = {taxid_str: data["empty"]}
            json.dump(mtdt2, open(path_metadata_empty, "w"), indent=4, sort_keys=True)
        except:
            logging.error(f"updateJsonRead2 ERROR {taxid_str}, {lread_str}, {data}")
    time.sleep(0.02)
    semaphore_jsonReadsMTDT.release()


def _readfiles(path):
    logging.info(f"{path}: START")
    listfasta = []
    listtruth = []
    with open(path, "r") as f:
        for line in f:
            if line[0] == "@":
                next = True
            elif next and line[0] in ["A", "C", "G", "T"]:
                listfasta.append(f"{str(line)}")
                next = False
            else:
                next = False
        # flush buffers
    logging.info(f"{path}: END")
    return listfasta


def _generateFastaAndTruth(lreads: int) -> None:
    """
    Generate fasta and truth file starting from reads
    Format fasta: ">S0R<nr>\n<sequence>"
    Format truth: "S0R<nr>\t<taxid>"
    :param lreads: read length of simulation
    :return: None
    """
    lreads_str = f"{lreads:0>6}"
    mtdt = json.load(open(dir_reads / "_metadata.json"))
    read_counter = 0
    empty = []
    path_fasta = str(dir_fasta / f"{lreads_str}.fasta")
    path_truth = str(dir_fasta / f"{lreads_str}.truth")
    bufferTruth = []
    with open(path_fasta, "w") as outfile, open(path_truth, "w") as truthfile:
        next = False
        dictPaths = {}
        paths = []
        counter = 1
        for taxid_str, data in mtdt.items():
            data: dict = data[lreads_str]
            if data["nreads"] == 0:
                empty.append(taxid_str)
                continue
            else:
                paths.append(data["path"])
                dictPaths[str(data["path"])] = [taxid_str, lreads_str]

        # nonrelPaths = paths.copy()
        # paths = [os.path.relpath(a) for a in paths]

        # logging.info(f"START: merge {lreads} reads")
        # start_time = time.time()
        # os.system("echo '' > .temp/outlen".replace("len", lreads_str))
        # for i, path in enumerate(paths, start=0):
        #     if i == 0:
        #         comamnd_merge_files = '''sed -n '2~4p' pathin | awk '{print $s "\\ttaxid"}' > .temp/outlen''' \
        #             .replace("pathin", path) \
        #             .replace("taxid", str(int(dictPaths[path][0]))) \
        #             .replace("len", lreads_str)
        #     else:
        #         comamnd_merge_files = '''sed -n '2~4p' pathin | awk '{print $s "\\ttaxid"}' >> .temp/outlen''' \
        #             .replace("pathin", path) \
        #             .replace("taxid", str(int(dictPaths[path][0]))) \
        #             .replace("len", lreads_str)
        #     logging.info(comamnd_merge_files)
        #
        #     os.system(comamnd_merge_files)        ######
        #
        # logging.info(f"ENDED merge: {lreads} in {time.time() - start_time}")
        # '''<sequence>\t<taxid>'''

        # logging.info(f"START: prefix {lreads} ")
        # start_time = time.time()
        # command_add_prefix = '''awk '{print ">S0R" NR "\\t" $s}' .temp/outlen > .temp/outlen2''' \
        #     .replace("len", lreads_str)
        # logging.info(command_add_prefix)

        # os.system(command_add_prefix)             ######
        # logging.info(f"ENDED: prefix {lreads} in {time.time() - start_time}")
        # '''>S0R<nr>\t<sequence>\t<taxid>'''

        logging.info(f"START: generate truth file {lreads} ")
        start_time = time.time()
        logging.info(f" {lreads} ")
        command_add_prefix = """cut -f 1,3 .temp/outlen2 |sed 's/^.//'  > pathtruth""".replace(
            "pathtruth", path_truth
        ).replace(
            "len", lreads_str
        )
        logging.info(command_add_prefix)

        os.system(command_add_prefix)
        logging.info(
            f"ENDED: generate truth file {lreads} in {time.time() - start_time}"
        )
        """ truth
        S0R<nr>\n<taixd>
        """

        # start_time = time.time()
        # logging.info(f"START: generate fasta file {lreads} ")
        # command_add_prefix = '''cut -f 1,2 .temp/outlen2 | sed 's/\\t/\\n/' > pathfasta''' \
        #     .replace("pathfasta", path_fasta) \
        #     .replace("len", lreads_str)
        # logging.info(command_add_prefix)
        #
        # os.system(command_add_prefix)             ######
        # logging.info(f"ENDED: generate fasta file {lreads} in {time.time() - start_time}")
        # ''' fasta
        # >S0R<nr>\n<sequence>
        # '''

    # lenTruth = int(subprocess.check_output(["wc", "-l", path_truth]).decode("utf-8").split(" ")[0])
    # _updateJsonRead(taxid_str, lreads_str, {"empty": {"n": len(empty), "list": empty},
    #                                         "generated": {"path_fasta": str(path_fasta), "path_truth": str(path_truth),
    #                                                       "nreads": lenTruth}})


def generateFastaAndTruth():
    os.system("mkdir .temp")
    with Pool(2) as p:
        start_time = time.time()
        p.map(_generateFastaAndTruth, RANGE)
        print(time.time() - start_time)


if __name__ == "__main__":
    semaphore_jsonReadsMTDT = Semaphore(1)
    logging.basicConfig(level=logging.DEBUG)
    path_metadata_fasta = dir_fasta / "_metadata.json"
    path_metadata_empty = dir_fasta / "_empty.json"
    generateFastaAndTruth()
