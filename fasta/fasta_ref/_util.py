import glob
import json
import re

p_taxid = ".?(\d{1,})\)"
p_initfasta = "S.*\t"


def uncertainTaxidsFromKraken():
    uncertainJson = {}
    for file in glob.glob("*.cut"):
        name = file[:-4]
        taxid = list(map(int, re.findall(p_taxid, open(file, "r").read())))
        settaxid = set(taxid)

        if len(settaxid) == 1:
            continue

        uncertainJson[name] = []
        for tid in settaxid:
            for line in open(file, "r").readlines():
                if f"(taxid {tid})" in line:
                    tname = re.sub(p_initfasta, "", line)[:-1]
                    uncertainJson[name].append({tid: {"name": tname, "acc": taxid.count(tid) / len(taxid)}})
                    # uncertainJson[name].append({"taxId": int(tid), "taxName": tname})
                    break

    #############################
    json.dump(uncertainJson, open("_uncertainTaxonIDs.json", "w"), indent=4)


def taxid_finals():
    forcednames = json.load(open("supporto/_forcedTaxID.json", "r"))
    jsonData = {}
    for file in glob.glob("*.cut"):
        name = file[:-4]
        taxid = list(map(int, re.findall(p_taxid, open(file, "r").read())))
        settaxid = set(taxid)

        if len(settaxid) == 1:
            tid = settaxid.pop()
        elif name.replace(" ", "_") in forcednames:
            tid = forcednames[name]["taxId"]
        elif len(settaxid) == len(taxid):
            # print("######################################################")
            tid = settaxid
        else:
            exit(5)

        for line in open(file, "r").readlines():
            if f"(taxid {tid})" in line:
                tname = re.sub(p_initfasta, "", line)[:-1]
                break
        jsonData[name] = {"taxId": int(tid), "taxName": tname}

    #############################
    json.dump(jsonData, open("_krakenTaxonID.json", "w"), indent=4)
    print(len(jsonData))


if __name__ == "__main__":
    uncertainTaxidsFromKraken()
    taxid_finals()
