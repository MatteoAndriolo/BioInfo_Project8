<style>
h1{
    font-weight: bold
}
dt>code{
    font-weight: bold;
    margin-left: 1em
}
h2>code{
    font-weight: bold;
}
dd {
    margin-left: 3em
}
code {
  white-space : pre-wrap !important;
}
href > code{
    font-weight: bold
}
</style>

<title>Project 8 -- BioInformatics -- Andriolo M., Pisacreta G.</title>

# Metagenomics classification: long reads vs short reads

One of the most important problem in metagenomic is the analysis of a sample in order to detect all the species (human,
bacteria, virus etc) that are contained in the sample.

Several tools exist for the classification of metagenomic reads extracted from the sample
and [Kraken2](https://ccb.jhu.edu/software/kraken2/) is one of the best performing (already installed in the BCB server)
.

However the __classification accuracy may vary and it can depend on the length of reads__.

The idea of the project is to compare the performance of Kraken2 when used with reads of different technologies.

[mason2](https://github.com/seqan/seqan/tree/master/apps/mason2):
Short reads simulator

[SimLoRD](https://bitbucket.org/genomeinformatics/simlord/src/master/):
Long reads Simulator

# Structure directory

* **docs**
    * contains general, usefull informations
* **fasta**
    * Directory containing all fasta files generate from the reads simulated with Mason and Simlord simulators
    * Fasta file are created concatenating all reads with a specific format
    * Automation done with scipt [02_construct_fasta.py](#s02)
* **KrakenOnRef**
    * Directory containing specific study on the accuracy of kraken given ??complete, correct, unmodified,
      genomes??.<br>
      <dl> Contains in particular:
          <dt><code>_krakenTaxonID.json</code></dt>
          <dd>Taxonomy id given by kraken (partially manually manipulated because of some conflicts)</dd>
          <dt><code>_uncertainTaxonID.json</code></dt>
          <dd>List of genomes file where different taxonId where attribuited for different contigs of the same genome</dd>
          <dt><code>results.json</code></dt>
          <dd>Results of evaluation results krakenID vs trueID</dd>
      </dl>
* **reads**
    * Directory containing _reads_ produced by [Simlord]() and [Mason]() simulators.
        * input genomes stored in ` ref\ ` folder <br>
        * <dl> Contains in particular:
            <dt><code>metadata.json</code></dt>
            <dd>For each read length simulation is present a folder. In each folder there is a metadata.json file with contains paths, command used for the simulation and number of reads generated </dd>
            <dt><code>**/mason/missing.json</code></dt>
            <dd>Mason cannot generate reads for some genomes. This file is used to store list of cases for which this errors happens. Cause are at the moment unknown (various hypothesis have been made nut it's been impossible to fix this error in time)</dd>
          </dl>
* **ref**
    * Directory containing the reference genomes used for the simulation
* **script**
  * look at [Scripts](#scripts) section
* *enviroment.yml*
    * File usefull to reconstruct enviroment using ***conda*** package manager. <br> (_tested only on linux_)


<h1 id="scripts">Scripts</h1>

## <code>_config.py</code>
[Link to script](script/_config.py)

Contains parameters required by the others script<br>
Manages directory organizations

<h2 id="mtdt"><code> _ref_metadata.py </code></h2>
[Link to script](script/_ref_metadata.py)

Generate metadata file `_metadata.json`  of the input genomes.<br> Used by the other scripts and for a fast overview of main specifics. 
[metadata example](ref/ref_50/_metadata.json)

<h2 id="s01"><code>01_sim_reads.py</code></h2>
[Link to script](script/01_sim_reads.py)

Script that automates reads generation via Mason and Simlord simulators.  <br>
For each read length there is a `metadata.json` file which contains paths, command used for the simulation and number of reads generated. [metadata example](reads/reads_50/mason/100/metadata.json)

### Command samples
* mason example
    ```commandline
    tools/mason2/bin/mason_simulator -seed 0 --num-threads 4 --fragment-mean-size 300 --illumina-read-length 100 -ir ref/ref_50/Amycolatopsis_mediterranei_Ref.fna --num-fragments 207294 -o reads/reads_50/mason/100/Amycolatopsis_mediterranei.fq
    ```
* simlord example
    ```commandline
    simlord --fixed-readlength 1000 --read-reference ref/ref_50/Amycolatopsis_mediterranei_Ref.fna -c 20 -pi 0.11 -pd 0.4 -ps 0.01 --no-sam reads/reads_50/simlord/1000/Amycolatopsis_mediterranei
    ```

<h2 id="s02"><code> 02_construct_fasta.py</code></h2>

[Link to script](script/02_construct_fasta.py)

For each collection of files of specific "read leangth" reads, concatenate them using the `.fasta` format:

```text
>S0R[number_read] 
read_sequence
```
where  
- read_sequence: read generated 
- number_read: counter of reads inserted

At the same time is also generated file with the correct taxonomy ID of read_sequence.

<h2 id="s03"><code>03_study.py</code></h2>
[Link ot script](script/03_study.py)

Automate evaluation of results using `evaluation` builded from `evaluation.cc` 
Generate [result.json](results/results_50/results.json) file which summarize all evaluations

Then generate plot for the results




# SETUP

## SIMLORD
```commandline
simlord --fixed-readlength 1000--read-reference ref/ref_50/Amycolatopsis_mediterranei_Ref.fna --coverage 20 -pi 0.11 -pd 0.4 -ps 0.01 --no-sam reads/reads_50/simlord/1000/Amycolatopsis_mediterranei
```
<dl>
    <dt>--fixed-readlength LEN</dt>
    <dd>constant read length for all reads</dd>
    <dt>--read-reference PATH</dt>
    <dd>read reference from FASTA file</dd>
    <dt>--coverage 20</dt>
    <dd>desired read coverage, used to calculate number of reads</dd>
    <dt></dt>
     <dt>--prob-ins 0.11</dt>
    <dd>insertion prob. for one-pass reads [default=0.11][short -pi]</dd>
     <dt>--prob-del P</dt>
    <dd>deletion prob. for one-pass reads [default=0.04][short -pd]</dd>
     <dt>--prob-sub P</dt>
    <dd>substitution prob. for one-pass reads [default=0.01][short -ps]</dd>
    <dt>--no-sam</dt>
    <dd>do not create SAM file</dd>
</dl>

### Outputs
Files in `.fastq` format

## MASON
```commandline
tools/mason2/bin/mason_simulator -seed 0 --num-threads 4 --fragment-mean-size 300 --illumina-read-length 100 -ir ref/ref_50/Amycolatopsis_mediterranei_Ref.fna --num-fragments 207294 -o reads/reads_50/mason/100/Amycolatopsis_mediterranei.fq
```
<dl>
    <dt> --seed INTEGER</dt>
    <dd> Seed to use for random number generator. Default: 0. </dd>
    <dt> --num-threads NUM</dt>
    <dt>-num-threads INTEGER</dt>
    <dd>Number of threads to use. In range [1..inf]. Default: 1.</dd>
    <dt>--fragment-mean-size INTEGER</dt>
    <dd> Mean fragment size for normally distributed fragment size simulation. In range [1..inf]. Default: 300.</dd>
    <dt>--illumina-read-length INTEGER</dt>
    <dd> Read length for Illumina simulation. In range [1..inf]. Default: 100</dd>
    <dt>-ir, --input-reference INPUT_FILE</dt>
    <dd>Path to FASTA file to read the reference from. Valid filetypes are: .sam[.*], .raw[.*], .gbk[.*], .frn[.*], .fq[.*], .fna[.*], .ffn[.*], .fastq[.*], .fasta[.*], .faa[.*], .fa[.*], .embl[.*], and .bam, where * is any of the following extensions: gz and bgzf for transparent (de)compression.</dd>
    <dt>-n, --num-fragments INTEGER</dt>
    <dd>Number of reads/pairs to simulate. In range [1..inf].</dd>
    <dt>-o, --out OUTPUT_FILE</dt>
    <dd> Output of single-end/left end reads. Valid filetypes are: .sam[.*], .raw[.*], .frn[.*], .fq[.*], .fna[.*], .ffn[.*], .fastq[.*], .fasta[.*], .faa[.*], .fa[.*], and .bam, where * is any of the following extensions: gz and bgzf for transparent (de)compression </dd>
</dl>

## COVERAGE
The coverage value ha been set at _20x_.
Simlord calculates autonomaly the number of reads to generate.
On the contrary Mason have to receive explicitly the number reads. It has been calculate using indicativelly the (rough) formula for coverage $coverage=(reads_lenght*number_reads)/(genome_size)$

## ENTERZ

[ncbi doc](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
Utility used for query automation on ncbi databases.

It has been used for fetching the correct taxonomy ID of the genomes.

There were some problems with taxid of reference file. Taxonomi ID has been queryed searching for taxid of each contigs inside the genomes but happened that the same genomes contained contigs appartaining to different species.
(only in Saccharomyces cerevisiae there is sequence _NC_001136.1_ that has got taxid (_4932_) different from the other 16 (_559292_))

