#!/bin/bash

#SBATCH --job-name kraken2_BioInfo8
#SBATCH --output out_kraken2_BioInfo8
#SBATCH --error error_kraken2_BioInfo8
#SBATCH --mail-user matteo.andriolo.2@studenti.unipd.it
#SBATCH	--mail-type ALL
#SBATCH --time 10:00:00
#SBATCH --ntasks 1
#SBATCH --cpu-per-task 1
#SBATCH --partition allgroups
#SBATCH --mem 80G

KRAKEN=/nfsd/bcb/bcbg/luciani/Kraken2
MYDIR=/nfsd/bcb/bcbg/bioProject8

cd $MYDIR
mkdir -p report_50/simlord report_50/mason
mkdir -p out_50/simlord out_50/mason
touch std.txt

for file in fasta_50/**/*.fasta
do
  NF=$MYDIR/$file
  NRF=${NF/fasta/report}
  NOF=${NF/fasta/out}
  echo $NF >> std.txt
  echo $NRF >> std.txt
  echo $NOF >> std.txt
  #$KRAKEN --db /nfsd/bcb/bcbg/cavattoni/tools/DBKraken2 --report ${NRF/.report/.txt} --threads 16 $file > ${NOF}
done

