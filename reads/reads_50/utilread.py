import json

if __name__ == "__main__":
    counter = 0
    mtdt = json.load(open("_metadata.json", "r"))

    dictOut = {}
    for taxid in mtdt:
        print("_________________________________________________")
        for lread in mtdt[taxid]:
            if mtdt[taxid][lread]["nreads"] == 0:
                counter += 1
                print(taxid, lread)
                try:
                    dictOut[taxid][lread] = mtdt[taxid][lread]
                except:
                    dictOut[taxid] = {}
                    dictOut[taxid][lread] = mtdt[taxid][lread]

    json.dump(dictOut, open("_0reads.json", "w"), indent=4)
    print(len(dictOut))
    print(counter)
