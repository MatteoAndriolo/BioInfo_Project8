MYDIR=/nfsd/bcb/bcbg/bioProject8
FASTADIR=$MYDIR/fasta/fasta_50
KRAKEN=/nfsd/bcb/bcbg/luciani/Kraken2/kraken2

mkdir -p $MYDIR/out/simlord $MYDIR/out/maven

for file in fasta_50/**/*.fasta
do
	echo $file
	nf=$FASTADIR/$file

done
