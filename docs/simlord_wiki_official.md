[simlord - bitbucket](https://bitbucket.org/genomeinformatics/simlord/src/master/)
[simlord official wiki - bitbucket](https://bitbucket.org/genomeinformatics/simlord/wiki/Home)
# SimLoRD - Simulation of Long Read Data #

SimLoRD is a Python command line program for the simulation of long reads from third generation sequencing technologies. 

Currently only the error model of Pacific Biosciences SMRT-sequencing is supported.
The identified error model is based on the analysis of two freely available datasets from Pacific Biosciences ([D1], [D2]) and was then validated with two different datasets ([D3], [D4]).

[D1]:https://github.com/PacificBiosciences/DevNet/wiki/Neurospora-Crassa-(Fungus)-Genome,-Epigenome,-and-Transcriptome
[D2]:http://blog.pacificbiosciences.com/2014/10/data-release-whole-human-transcriptome.html
[D3]:http://blog.pacificbiosciences.com/2013/12/data-release-human-mcf-7-transcriptome.html
[D4]:https://github.com/PacificBiosciences/DevNet/wiki/C.-elegans-data-set

| ID   | type | organism               |     #CCSs | CCS bases |  #subreads | subreads bases | chemistry |
|------|------|------------------------|----------:|-----------|-----------:|----------------|-----------|
| [D1] | DNA  | Neurospora Crassa      |    12 566 | 103 Mbp   |    176 075 | 982 Mbp        | P4-C3     |
| [D2] | RNA  | Homo sapiens - brain   |   161 948 | 481 Mbp   |  2 334 092 | 6 Gbp          | P5-C3     |
| [D3] | RNA  | Homo sapiens - MCF7    | 1 134 517 | 1.9 Gbp   | 10 029 360 | 15 Gbp         | P4-C2     |
| [D4] | DNA  | Caenorhabditis elegans |    21 426 | 350 Mbp   |    461 333 | 5 Gbp          | P6-C4     |



## Description of data characteristics and error model ##

There are two different types of reads resulting from SMRT sequencing: subreads and circular consensus sequence reads (CCSs).
Because of the circular form of the DNA fragments with adapter sequences between forward and backward strand, a DNA fragment may be sequenced multiple times in a single run.
For a single pass through the sequencer, the error rate is high (subreads), but it is possible to calculate a consensus after multiple passes (CCSs).

### Read lengths ###

We found that DNA reads (subreads as well as CCSs) show a lognormal distribution of the read length, while RNA reads are usually size selected and show peaks in the read length distribution.

Examples for real datasets:

  - [Read length distribution of the subreads from N. crassa ][read_length_distribution_subreads_neuro.png] (D1)
  - [Read length distribution of the CCSs from N. crassa ][read_length_distribution_ccs_0fp_neuro.png] (D1)
  - [Size selected read length distribution of the CCSs from HG brain  ][read_length_distribution_ccs_0fp_brain.png] (D2)
  - [Read length distribution of the size selected CCSs (15-20 KBp) from C. elegans] [read_length_distribution_ccs_0fp_elegans.png] (D4)

[read_length_distribution_subreads_neuro.png]: https://bitbucket.org/repo/EdMgxB/images/2947525520-read_length_distribution_subreads_neuro.png
[read_length_distribution_ccs_0fp_neuro.png]: https://bitbucket.org/repo/EdMgxB/images/3068675482-read_length_distribution_ccs_0fp_neuro.png
[read_length_distribution_ccs_0fp_brain.png]: https://bitbucket.org/repo/EdMgxB/images/3028278726-read_length_distribution_ccs_0fp_brain.png
[read_length_distribution_ccs_0fp_elegans.png]: https://bitbucket.org/repo/EdMgxB/images/336006915-read_length_distribution_ccs_0fp_elegans.png

Results with SimLoRD:

  - [Calling SimLoRD with (0.2001, -10075, 17923) as  lognorm-params (according to the N. crassa dataset, parameter set S1)][read_length_distribution_dna_12566_0.15_0.09_0.4.png]


[read_length_distribution_dna_12566_0.15_0.09_0.4.png]:https://bitbucket.org/repo/EdMgxB/images/374112958-read_length_distribution_dna_12566_0.15_0.09_0.4.png


### Number of passes for one molecule ###

Within one sequencer run the DNA molecules may be sequenced multiple times depending on their length. Shorter molecules have a tendency for more passes than longer molecules. The following plots show that the different datasets follow a similar distribution.

- [Correlation between read length and number of passes for N. crassa CCS][lengths_passes_filtered_ccs_0fp_neuro.png] (D1)
- [Correlation between read length and number of passes for HG brain CCS][lengths_passes_filtered_ccs_0fp_brain.png] (D2)
- [Correlation between read length and number of passes for HG MCF 7][lengths_passes_subreads_mcf7_x.png] (D3)
- [Correlation between read length and number of passes for C. elegans][lengths_passes_subreads_elegans_x.png] (D4)


[lengths_passes_filtered_ccs_0fp_neuro.png]:https://bitbucket.org/repo/EdMgxB/images/2781650630-lengths_passes_filtered_ccs_0fp_neuro.png
[lengths_passes_filtered_ccs_0fp_brain.png]: https://bitbucket.org/repo/EdMgxB/images/1156851106-lengths_passes_filtered_ccs_0fp_brain.png
[lengths_passes_subreads_mcf7_x.png]:https://bitbucket.org/repo/EdMgxB/images/2971284744-lengths_passes_subreads_mcf7_x.png
[lengths_passes_subreads_elegans_x.png]:https://bitbucket.org/repo/EdMgxB/images/1844118380-lengths_passes_subreads_elegans_x.png

Using the paramters obtained from (D2) SimLoRD leads to the following results for the lengths passes correlation:

  - [SimLoRD results for parameter set S1][lengths_passes_dna_12566_0.15_0.09_0.4_x.png]

[lengths_passes_dna_12566_0.15_0.09_0.4_x.png]:https://bitbucket.org/repo/EdMgxB/images/842840856-lengths_passes_dna_12566_0.15_0.09_0.4_x.png


If you take a look at the profile of the plots, you can see that the number of passes is chi-square distributed with the parameter depending on the read length.

- [chi^2 distribution for CCSs of HG brain with read length from 2050 to 2100][filtered_hist_ccs_0fp_brain_2050_2100_chi2.png] (D2)
- [chi^2 distribution for CCSs of HG brain with read length from 3050 to 3100][filtered_hist_ccs_0fp_brain_3050_3100_chi2.png] (D2)

[filtered_hist_ccs_0fp_brain_2050_2100_chi2.png]: https://bitbucket.org/repo/EdMgxB/images/366187672-filtered_hist_ccs_0fp_brain_2050_2100_chi2.png
[filtered_hist_ccs_0fp_brain_3050_3100_chi2.png]: https://bitbucket.org/repo/EdMgxB/images/2798568977-filtered_hist_ccs_0fp_brain_3050_3100_chi2.png

After obtaining the parameters of the chi² distribution for all read length ranges it is possible to fit functions for the parameter calculation:

  - [Parameter *n* of chi² distribution][filtered_fitted_values_alpha_chi2_ccs_0fp_brain.png]
  - [Parameter *s* of chi² distribution][filtered_fitted_values_scale_chi2_ccs_0fp_brain.png]

[filtered_fitted_values_alpha_chi2_ccs_0fp_brain.png]:https://bitbucket.org/repo/EdMgxB/images/3150443942-filtered_fitted_values_alpha_chi2_ccs_0fp_brain.png
[filtered_fitted_values_scale_chi2_ccs_0fp_brain.png]:https://bitbucket.org/repo/EdMgxB/images/788888501-filtered_fitted_values_scale_chi2_ccs_0fp_brain.png


### Correlation of quality increase and number of passes ####

A FASTQ quality *Q* describes the error probability *p* of that base on the logarithmic PHRED scale.
```
Q = -10 * log10(p)
p = 10**(-Q/10)
```

Subreads have a mean quality of 5 to 10 which means an error probability between 31% and 10%:

  - [Mean quality of a read vs.read length - subreads N. crassa (D1)][lengths_accuracies_subreads_neuro.png]
  - [Mean quality of a read vs.read length - subreads HG brain (D2)][lengths_accuracies_subreads_brain.png]
  - [Mean quality of a read vs.read length - subreads C. elegans (D4)][lengths_accuracies_subreads_elegans.png]


[lengths_accuracies_subreads_neuro.png]:https://bitbucket.org/repo/EdMgxB/images/820484385-lengths_accuracies_subreads_neuro.png
[lengths_accuracies_subreads_brain.png]: https://bitbucket.org/repo/EdMgxB/images/601092481-lengths_accuracies_subreads_brain.png
[lengths_accuracies_subreads_elegans.png]:https://bitbucket.org/repo/EdMgxB/images/3518133071-lengths_accuracies_subreads_elegans.png


For CCS reads the quality increases depending on the number of passes for each read.
A quality of 25 for example represents a error probability of 0.31%: 

  - [Passes vs. mean quality N. crassa (D1)][passes_accuraciesccs_0fp_neuro.png]
  - [Passes vs. mean quality HG brain (D2)][passes_accuraciesccs_0fp_brain.png]

[passes_accuraciesccs_0fp_neuro.png]:https://bitbucket.org/repo/EdMgxB/images/1001370713-passes_accuraciesccs_0fp_neuro.png
[passes_accuraciesccs_0fp_brain.png]: https://bitbucket.org/repo/EdMgxB/images/667582370-passes_accuraciesccs_0fp_brain.png

If you look at the increase of quality as a function of the number of passes, you see a distribution following a noisy square root function:

  - [Increase vs. passes HG brain (D2)][qualitiy_increase_ccs_0fp_brain.png])

[qualitiy_increase_ccs_0fp_brain.png]: https://bitbucket.org/repo/EdMgxB/images/3610139675-qualitiy_increase_ccs_0fp_brain.png


### Simulation of base qualities ###

Putting these results together:

  - The read length is drawn from a lognormal distribution (or specified otherwise).
  - Depending on the read length, the parameters for the chi-square distribution are calculated.
  - The number of passes  is drawn from the chi square distribution.
  - The increase *i* of quality is drawn from a noisy square root.
  - If initial error probabilities p(0) for reads (or basepairs) with one pass are given, we adjust them as follows to *p(i)* for quality increase *i*:
```
p(i) = p(0)**i

```
  - With the adjusted error probabilities, the read can be simulated.


## Parameters of SimLoRD ##

SimLoRD needs a path to an output file for the simulated reads.

Optionally, different names than the defaults may be set for the SAM alignment output, or to save a generated reference.

There are four possibilities to specify the read length:

 - give three parameter for lognormal distribution to draw read length from (-ln)
 - set fixed read length for all reads (-fl)
 - give a FASTQ-file with reads to draw the read length from (-sf)
 - give a file containing only read lengths (one int per line) to draw from (-st)


The parameters *n* and *s* for the chi² distribution are calculated with the following functions, where x is the read length and the parameters m, b, z and m, b, z, c, a are defined with `-xn` and `-xs`, respectively:

- n(x) =
    - = m*x + b if x < z,
    - = m*z + b if x >=z;
- s(x) =
    - = m*x + b     if x <= z,
    - = c * x**(-a) if x > z.


The quality increase is calculated as sqrt(p + a) - b + N with number of passes p, parameter a and b (-sq) and normally distributed noise N with additional parameters.

# Overview over all parameters #

The table shows all parameters of SimLoRD as well as the used parameter sets S1 and S2.


| parameter / option (long)           | short                  | description  [default value]  |parameter set S1| parameter set S2 |
|-------------------------------------|------------------------|-----------------------------|------|---|
| --num-reads                         | -n                     | number of reads to simulate [1000]                         | 12566|- |
| --coverage                          | -c                     | desired read coverage, used to calculate number of reads                        | -|- |
| --read-reference PATH               | -rr                    | read reference from FASTA file                             | neurospora_crassa.fa | -|
| --generate-reference GC LEN         | -gr                    | generate reference with given GC content and length        |-  | -|
| --save-reference PATH               | -sr                    | path for generated reference                               | -| -|
| --lognorm-readlength PARAMS         | -ln                    | draw read length from log-normal distribution [0.2001, -10075.4364, 17922.611]             |0.2001, -10075.4364, 17922.611 | -|
| --min-readlength LEN                | -mr                    | minimum log-normal read length [50]                         | 50|- |
| --fixed-readlength LEN              | -fl                    | constant read length for all reads                         |- |- |
| --sample-readlength-from-fastq PATH | -sf                    | draw read length from given FASTQ file                     |- | -|
| --sample-readlength-from-text PATH  | -st                    | draw read length from given numbers (one per line)         |- |- |
| --max-passes N                      | -mp                    | maximum number of passes over a read [40]                  | 40| -|
| --chi2-params-n PARAMS              | -xn                    | parameters to calculate n (df) for chi^2 distribution [1.8923e-03, 2.5394e+00, 5500]      |1.8923e-03, 2.5394e+00, 5500 |- |
| --chi2-params-s PARAMS              | -xs                    | parameters to calculate s for chi^2 distribution [0.0121, -5.12, 675, 48303.073, 1.469]      |0.0121, -5.12, 675, 48303.073, 1.469|- |
| --sqrt-params PARAMS                | -sq                    | parameters for quality increase square root function [0.5, 0.2247]  |0.5, 0.2247 |- |
| --prob-ins P                        | -pi                    | insertion prob. for one-pass reads [0.11]                 |0.15 |- |
| --prob-del P                        | -pd                    | deletion prob. for one-pass reads [0.04]                  |0.09 |- |
| --prob-sub P                        | -ps                    | substitution prob. for one-pass reads [0.01]              |0.4 |- |
| --sam-output PATH                   | -so                    | custom path for SAM file                                  |- |- |
| --no-sam                            |                        | do not create SAM file | -|-|
| --without-ns                        |                        | skip regions containing Ns and sample reads only from parts completly without Ns  | -|-|
| --uniform-chromosome-probability    |                        | sample chromosomes for reads equally distributed instead of weighted by their length. (Was default behaviour up to version 1.0.1) | -|-|

Warning: Using --without-ns may lead to biased read coverage depending on the size of contigs without Ns and the expected readlength.

# Comparison of SimLoRD and other simulators #

A comparison of the simulation results of SimLoRD, PBSIM and FASTQSim can be found [here](comparison).
