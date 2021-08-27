# STMLST

STMLST is an effective approach and automatic bioinformatics tool for *serotype identification* of *multiple microbial organisms*.

## Install

### Download program

1. Download program first: ```git clone https://github.com/lyotvincent/STMLST.git```  
2. Install external tools:  
2.1. Install miniconda from *https://docs.conda.io/en/latest/miniconda.html* or anaconda from *https://www.anaconda.com/products/individual*  
2.2. Create python3 environment (because QUAST depends on python3.7) ```conda create -n env_name python=3```     
2.3. Install external tools by running a command in the conda environment ```conda install any2fasta blast```  
*<small>2.supplement. If user want combine the serotype identification result of seqsero, install it by running a command ```conda install seqsero2```</small>*  

### Download database

1.```cd /PATH/TO/stmlst/db```  
2.```python download_publist.py``` could download data used for serotype identification from PUBMLST to local folder.  
3.build blastdb and "key alleles-sequence types-serotypes" association database using```python make_db.py```.  

## Help

simple usage
```python stmlst.py -f XXX.fastq```  

```python stmlst.py -h``` to help.  

parameters in pipeline:  

help:  
-h, --help            show this help message and exit  
-f FILE_NAME, --file_name FILE_NAME  
                    input file  
-n NUM_THREADS, --num_threads NUM_THREADS  
                    number of threads  
--min_id MIN_ID       Percent identity <Real, 0..100> DNA identity of full  
                    allelle to consider 'similar' [~]  
--min_cov MIN_COV     DNA cov to report partial allele at all [?]  
--specified_scheme SPECIFIED_SCHEME  
                    specified a scheme  
-s, --seqsero         fill null serotype with seqsero  
-v, --version         show program's version number and exit  

a example of running stmlst:  

```python stmlst/bin/stmlst.py -f SRR5986253.contigs.fa```  

[INFO] highest probability organism: ['senterica_achtman_2', 100.0, {'dnaN': '169', 'hemD': '48', 'thrA': '4', 'hisD': '16', 'purE': '12', 'aroC': '42', 'sucA': '23'}]  
[INFO] serotype identification result table:
|ST|aroC|dnaN|hemD|hisD|purE|sucA|thrA|serotype|
|----|----|----|----|----|----|----|----|----|
|2041|42|169|48|16|12|23|4|unknown:0.21428571428571427;Abaetetuba:0.7142857142857143;other:0.07142857142857142|

## Data of tests and test records

*test/md_v2/test_on_s_set.xlsx* contains the data used in 3.1 of our paper. It consists of NGS data of single species.  
*test/md_v2/test_on_n_set.xlsx* contains the data used in 3.2 of our paper. It consists of NGS data of single species.  
*test/md_v2/test_on_nanopore_sequencing_data.xlsx* contains the data used in 3.3 of our paper. It consists of nanopore sequencing data of single species.  
*test/md_v2/test_on_multiple_microbial_organisms_set.xlsx* contains the data used in 3.4 of our paper.  It consists of NGS data of multiple microbial organisms.  
