import json
import logging
import os
import subprocess
import time
from multiprocessing import Semaphore

from config import DIR_FASTA_MASON, DIR_FASTA_SIMLORD, DIR_READS, DIR_FASTA, RANGE

dir_reads = DIR_READS
dir_fasta = DIR_FASTA
dir_fasta_mason = DIR_FASTA_MASON
dir_fasta_simlord = DIR_FASTA_SIMLORD


def _updateJsonRead(taxid_str: str, lread_str: str, data: dict):
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
            mtdt: dict = json.load(open(path_metadata_empty, "r"))
            if lread_str in mtdt.keys():
                mtdt[lread_str][taxid_str] = data["empty"]
            else:
                mtdt[lread_str] = {taxid_str: data["empty"]}
            json.dump(mtdt, open(path_metadata_empty, "w"), indent=4, sort_keys=True)
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


def _generateFastaAndTruth(lreads):
    lreads_str = f"{lreads:0>6}"
    mtdt = json.load(open(dir_reads / "_metadata.json"))
    read_counter = 0
    empty = []
    path_fasta = dir_fasta / f"{lreads_str}.fasta"
    path_truth = dir_fasta / f"{lreads_str}.truth"
    bufferTruth = []
    bufferFasta = []
    with open(path_fasta, "w") as outfile, open(path_truth, "w") as truthfile:
        next = False
        # 0 based indexes
        dictPaths = {}
        paths = []
        counter = 1
        # logging.info(f"{lreads_str}: START")
        for taxid_str, data in mtdt.items():
            # logging.info(f"{taxid_str}: {lreads}, {counter} START")
            data: dict = data[lreads_str]
            if data["nreads"] == 0:
                empty.append(taxid_str)
                continue
            else:
                paths.append(data["path"])
                dictPaths[str(data["path"])] = [taxid_str, lreads_str]

            # with open(data["path"], "r") as f:
            #     for line in f.readlines():
            #         if line[0] == "@":
            #             next = True
            #         elif next and line[0] in ["A", "C", "G", "T"]:
            #             if len(bufferFasta)<1000000:
            #                 bufferFasta.append(f">S0R{read_counter}\n{str(line)}")
            #                 bufferTruth.append(f"S0R{read_counter}\t{int(taxid_str)}\n")
            #             else:
            #                 outfile.writelines(bufferFasta)
            #                 bufferFasta=[]
            #                 truthfile.writelines(bufferTruth)
            #                 bufferTruth=[]
            #             read_counter += 1
            #             next = False
            #         else:
            #             next = False
            #     # flush buffers
            #     if len(bufferFasta):
            #         outfile.writelines(bufferFasta)
            #         bufferFasta = []
            #         truthfile.writelines(bufferTruth)
            #         bufferTruth = []
            #     counter+=1

        nonrelPaths = paths.copy()
        paths = [os.path.relpath(a) for a in paths]
        command = f"sed -n '2~4p' {' '.join(paths)} | awk " + "'{print \">S0R\" NR \"\\n\" $s}' > " + f"{os.path.relpath(path_fasta)}"
        print(command)
        start_time = time.time()
        os.system(command)
        print(time.time() - start_time)
        start_time = time.time()
        os.system(f"touch {os.path.relpath(path_fasta)}")
        with open(path_truth, "w") as fout:
            for p, nrp in zip(paths, nonrelPaths):
                number = int(subprocess.check_output(["wc", "-l", p]).decode("utf-8").split(" ")[0]) / 4
                command = '''awk 'BEGIN{ for(i=0;i<number;i++) print "S0R" i "\\ttaxid"}' >> out''' \
                    .replace("number", str(number)) \
                    .replace("taxid", str(int(dictPaths[str(nrp)][0]))) \
                    .replace("out", os.path.relpath(path_truth))
                print(command)
                os.system(command)
                fout.write("\n".join(bufferTruth))
        print(time.time() - start_time)
        print(counter)

        # with Pool(cpu_count()) as p:
        #     read_counter=0
        #     for a in p.map(_readfiles, paths):
        #         a=[f">S0R{counter+i}\n{str(aa)}" for i,aa in enumerate(a)]
        #         t=[f"S0R{counter+i}\t{str(int(taxid_str))}" for i in range(len(a))]
        #         read_counter+=len(a)
        #     truthfile.writelines(t)
        #     outfile.writelines(a)

    # _updateJsonRead(taxid_str, lreads_str, {"empty": {"n": len(empty), "list": empty},
    #                                         "generated": {"path_fasta": str(path_fasta), "path_truth": str(path_truth),
    #                                                       "nreads": read_counter + 1}})


def generateFastaAndTruth():
    # with Pool(cpu_count() ) as p:
    #     p.map(_generateFastaAndTruth, RANGE)
    start_time = time.time()
    for a in RANGE:
        _generateFastaAndTruth(a)
    print(time.time() - start_time)


if __name__ == "__main__":
    semaphore_jsonReadsMTDT = Semaphore(1)
    logging.basicConfig(level=logging.DEBUG)
    path_metadata_fasta = dir_fasta / "_metadata.json"
    path_metadata_empty = dir_fasta / "_empty.json"
    generateFastaAndTruth()
