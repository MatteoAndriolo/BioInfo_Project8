#!/bin/bash

#SBATCH --job-name kraken2_BioInfo8
#SBATCH --output out_kraken2_BioInfo8
#SBATCH --error error_kraken2_BioInfo8
#SBATCH --mail-user matteo.andriolo.2@studenti.unipd.it
#SBATCH --mail-user matteo.andriolo.2@studenti.unipd.it
#SBATCH	--mail-type ALL
#SBATCH --time 10:00:00
#SBATCH --ntasks 1
#SBATCH --cpu-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 80G

cd /nfsd/bcb/bcbg/luciani/Kraken2

./kraken2 --db /nfsd/bcb/bcbg/cavattoni/tools/DBKraken2 --report k2_report_Sim_50_DBKraken2.txt --threads 16 /nfsd/bcb/bcbg/luciani/dataset/data/Sim_50/Sim_50.fasta > /nfsd/bcb/bcbg/luciani/Kraken2/Results/kraken2_Sim_50_DBKraken2.out

