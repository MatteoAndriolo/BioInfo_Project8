[wiki](https://en.wikipedia.org/wiki/FASTA_format)

# Extension
|Extension| content                        |
|-------|----------------------------------|
| fasta | generic Fasta                    |
| fna   | FASTA nucleic acid               |
| ffn   | FASTA nucleotide of gene regions |
| faa   | FASTA amino acid                 |
| frn   | FASTA non-coding RNA             |

# Format
At the begining of each genome there must be a description line:
```
>NCBI_Identifiers, name and description 
SEQUENCE
```
Each file can have multiple sequences, each one must be introduced by a description line starting with 
```
>
```