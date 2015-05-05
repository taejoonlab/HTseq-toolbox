#!/bin/bash
BWA="$HOME/local/src/bwa/bwa-0.7.10/bwa"
SAM2HIT="$HOME/git/HTseq-toolbox/sam/sam-to-sam_hit.py"

#DB="$WORK/xenopus.db/bwadb/XENLA_JGIv71_lt1k"
DB="/work/xenopus.db/bwadb/XENLA_BACfull_201501"
DBNAME=$(basename $DB)

#for FQ1 in $(ls ../fastq/*untie_1.fastq.gz)
#for FQ1 in $(ls ../fastq/*S11*notCombined_1.fastq)
for FQ1 in $(ls ../fastq/*untie_1.fastq)
do
  #FQ2=${FQ1/notCombined_1/notCombined_2}
  FQ2=${FQ1/untie_1/untie_2}

  #gunzip $FQ1
  #gunzip $FQ1
  #FQ1=${FQ1/.gz/}
  #FQ2=${FQ2/.gz/}

  SAM=$(basename $FQ1)

  #SAM=${SAM/.notCombined_1.fastq/_paired}"."$DBNAME".bwa_mem.sam"
  SAM=${SAM/.untie_1.fastq/_paired}"."$DBNAME".bwa_mem.sam"

  $BWA mem $DB $FQ1 $FQ2 > $SAM
  $SAM2HIT $SAM
done
