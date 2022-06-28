#!/bin/bash

#SBATCH --job-name kraken2_BioInfo8
#SBATCH --output out_kraken2_BioInfo8
#SBATCH --error error_kraken2_BioInfo8
#SBATCH --mail-user matteo.andriolo.2@studenti.unipd.it
#SBATCH	--mail-type ALL
#SBATCH --time 2:00:00
#SBATCH --ntasks 1
#SBATCH --partition allgroups
#SBATCH --mem 100G

KRAKEN=/nfsd/bcb/bcbg/luciani/Kraken2/kraken2
MYDIR=/nfsd/bcb/bcbg/bioProject8

cd $MYDIR
mkdir -p report/simlord report/mason
mkdir -p out/simlord out/mason
touch std.txt

echo "started" > out_kraken2_BioInfo8

for file in fasta_50/**/*.fasta
do
  NF=$MYDIR/$file
  NRF=${NF/fasta/report}
  NOF=${NF/fasta/out}
  echo $NF >> out_kraken2_BioInfo8
  echo ${NRF/.fasta/.txt}>> out_kraken2_BioInfo8
  echo ${NOF/.fasta/.out} >> out_kraken2_BioInfo8
  $KRAKEN --db /nfsd/bcb/bcbg/cavattoni/tools/DBKraken2 --report ${NRF/.fasta/.txt} --threads 16 $file > ${NOF/.fasta/.out}
  echo "end" >> std.txt
done