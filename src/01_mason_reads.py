from distutils.command.config import config

from pyparsing import oneOf
from script.definitions import READS_DIR, ROOT_DIR,MASON_SIMULATOR
import cmd
import os
from multiprocessing import cpu_count


"""
-v              verbose
--seed 0        seed for random generator
--num-threads   number threads
--num-fragments number of read pairs to simulate
-o              output file

"""
inf=os.path.join(READS_DIR,"reads_50","Halobacterium.fastq")
command=f'{MASON_SIMULATOR} -v \
        --seed 0\
        --num-threads {cpu_count()}\
        -ir {inf}/
        --num-fragments 10000 \
        -o LEFT.fq '



os.system(command)