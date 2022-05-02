def gen_read_simlord(data):
    name=data[0]
    metadata=data[1]
    conf=data[3]
    # SimLoRD parameters
    for c in conf:
        locals().update(c)
        fref=metadata["path"]
        fread=metadata["dir_reads"]/name
        # execute SimLoRD
        #os.system(f'echo "simlord --read-reference {fref} -c {c} -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}"')
        #os.system(f'simlord --read-reference {fref} -c 20 -pi {pi} -pd {pd} -ps {ps} --no-sam {fread}')
