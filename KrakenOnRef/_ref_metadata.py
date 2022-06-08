import code
import glob
import json
import re
from pathlib import Path

from script._config import DIR_REF

jsonData = {}


def getSeqLength(text) -> (int, int, int):
    lengthSeq = []
    somma = 0
    for line in text:
        if ">" in line and somma != 0:
            lengthSeq.append(somma)
            somma = 0
        else:
            somma += len(line)
    if somma != 0:
        lengthSeq.append(somma)
    # print(somma, lengthSeq)
    return (min(lengthSeq), max(lengthSeq), int(sum(lengthSeq) / len(lengthSeq)))


if __name__ == "__main__":
    # parse files

    mtdt_manual = json.load(open("_taxidManual.json", "r"))
    files_path = glob.glob('*.fna')
    for f_path in files_path:
        name = Path(f_path).stem
        if name[-4:] == "_Ref":
            name = name[:-4]

        p_description_line = re.compile(r'^\>(.*)', re.M)
        description_lines = re.findall(p_description_line, open(f_path).read())
        p_codename = "N\w_[\w\d]*.[\w\d]?"
        codename = re.findall(p_codename, open(f_path).read())
        p_cut = "S0R\d*\t(.*)"
        taxid_kraken = re.findall(p_cut, open(f_path.replace(".fna", ".cut").replace("_Ref", ""), "r").read())

        # print(f_path)
        # print(len(description_lines))
        # print(codename)
        # print("\n\n")

        minn, maxx, meann = getSeqLength(open(f_path).readlines())
        temp_manual_taxids = set(mtdt_manual[name]["names"])
        jsonData[name] = {
            "path": f_path,
            "n_sequences": len(description_lines),
            "manual_taxid": list(temp_manual_taxids),
            "taxid": sorted([[t, taxid_kraken.count(t) / len(taxid_kraken)] for t in set(taxid_kraken)],
                            key=lambda x: x[1], reverse=True),
            "id": [[a, c] for a, c in zip(taxid_kraken, description_lines)] if len(set(taxid_kraken)) != 1 else
            taxid_kraken[0]
            # "mean_length_sequence": meann,
            # "min": minn,
            # "max": maxx
        }



    # with open(mtdt_seq, "w") as f:
    #     json.dump(jsonData, f, indent=4)

    with open("_metadata_test.json", "w") as f:
        json.dump(jsonData, f, indent=4)
    with open("_id.json", "w") as f:
        json.dump({k:{"id":v["id"]} for k,v in jsonData},f,indent=4)


