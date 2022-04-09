1) get reference data from NCBI genome databank. 50 species genomed saved in fna files inside ref_50
2) simulate reads with simlord and mason2 introducing errors
    * numerate each reads inside fasta files
3) use Kraken for classification
    * start job in cluster
    * cut output only the 2-3 columns
4) validation
    * check precision... 


look at simlord wiki/comparison and zoreto/software/SimLoRD/SimLoRD_Simulation*.pdf for inspiration
