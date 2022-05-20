import os

dir_reads="./reads/"
output_file = './Sim_50.fastq'

name_file = []
listfile = []
num_file = 0
list_num_reads = []
c = 0
reads_number = 0
print(os.listdir())
directory = os.chdir(dir_reads)
for name_file in os.listdir(dir_reads):
    if name_file.endswith('.fastq'):
        listfile.append(name_file)
        listfile.sort()
        num_file = num_file + 1
        
with open(output_file, mode='w') as out_file:
    for i in range(len(listfile)):
        with open(dir_reads + listfile[i], 'r') as file:
            for line in file:
                if line.startswith("G") or line.startswith("A") or line.startswith("C") or line.startswith("T"):
                    out_file.write(">S0R" + str(reads_number) + "\n" + str(line) + "\n")
                    reads_number = reads_number + 1