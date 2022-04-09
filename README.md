# Project 8 -- BioInformatics

ASSIGNED to G. Pisacreta, A.  Matteo
# Metagenomics classification: long reads vs short reads 
One of the most important problem in metagenomic is the analysis of a sample in order to detect all the species (human, bacteria, virus etc) that are contained in the sample.

Several tools exist for the classification of metagenomic reads extracted from the sample and [Kraken2](https://ccb.jhu.edu/software/kraken2/) is one of the best performing (already installed in the BCB server).

However the __classification accuracy may vary and it can depend on the length of reads__.

The idea of the project is to compare the performance of Kraken2 when used with reads of different technologies.


[mason2](https://github.com/seqan/seqan/tree/master/apps/mason2):
    Short reads simulator

[SimLoRD](https://bitbucket.org/genomeinformatics/simlord/src/master/):
    Long reads Simulator


# Structure directory
* docs
    * contains general, usefull informations
* src
    * contains all the script and code used
* reads
    * contains all the simulated reads
        * .\reads\reads_50\
* ref
    * contains the reference genomes used for the simulation
        * .\ref\ref_50\
* *enviroment.yml* 
    * list of necessary packages. Useful to reconstruct enviroment using ***conda***.
    * tested only on linux

Both in ***ref*** and in ***reads*** are present files *metadata.json* that contains information about data generated.