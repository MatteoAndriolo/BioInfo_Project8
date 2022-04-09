
# Overview over all parameters #


| parameter / option (long)           | short                  | description  [default value]  |
|-------------------------------------|------------------------|-----------------------------|
| --num-reads                         | -n                     | number of reads to simulate [1000]                         |
| --coverage                          | -c                     | desired read coverage, used to calculate number of reads                        |
| --read-reference PATH               | -rr                    | read reference from FASTA file                             |
| --generate-reference GC LEN         | -gr                    | generate reference with given GC content and length        |
| --save-reference PATH               | -sr                    | path for generated reference                               | 
| --lognorm-readlength PARAMS         | -ln                    | draw read length from log-normal distribution [0.2001, -10075.4364, 17922.611]             |
| --min-readlength LEN                | -mr                    | minimum log-normal read length [50]                        | 
| --fixed-readlength LEN              | -fl                    | constant read length for all reads                         |
| --sample-readlength-from-fastq PATH | -sf                    | draw read length from given FASTQ file                     |
| --sample-readlength-from-text PATH  | -st                    | draw read length from given numbers (one per line)         |
| --max-passes N                      | -mp                    | maximum number of passes over a read [40]                  |
| --chi2-params-n PARAMS              | -xn                    | parameters to calculate n (df) for chi^2 distribution [1.8923e-03, 2.5394e+00, 5500]      |
| --chi2-params-s PARAMS              | -xs                    | parameters to calculate s for chi^2 distribution [0.0121, -5.12, 675, 48303.073, 1.469]      |
| --sqrt-params PARAMS                | -sq                    | parameters for quality increase square root function [0.5, 0.2247]  |
| --prob-ins P                        | -pi                    | insertion prob. for one-pass reads [0.11]                 |
| --prob-del P                        | -pd                    | deletion prob. for one-pass reads [0.04]                  |
| --prob-sub P                        | -ps                    | substitution prob. for one-pass reads [0.01]              |
| --sam-output PATH                   | -so                    | custom path for SAM file                                  |
| --no-sam                            |                        | do not create SAM file |
| --without-ns                        |                        | skip regions containing Ns and sample reads only from parts completly without Ns  |
| --uniform-chromosome-probability    |                        | sample chromosomes for reads equally distributed instead of weighted by their length. (Was default behaviour up to version 1.0.1) |

Warning: Using --without-ns may lead to biased read coverage depending on the size of contigs without Ns and the expected readlength.
