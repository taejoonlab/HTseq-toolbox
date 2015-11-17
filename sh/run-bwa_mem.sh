#!/bin/bash

SAMTOOLS="$HOME/src/samtools/samtools-1.2/samtools"
BWA="$HOME/src/bwa/bwa-0.7.12/bwa"

DB="$HOME/project/xenopus.db/bwadb/XENLA_JGIv18pV2_cdna_final"
DBNAME=$(basename $DB)

for FQ1 in $(ls ../fastq/*.untie_1.fastq.gz)
do
  FQ2=${FQ1/_1/_2}
  gunzip $FQ1
  gunzip $FQ2
  FQ1=${FQ1/.gz/}
  FQ2=${FQ2/.gz/}

  SAM=$(basename $FQ1)
  SAM=${SAM/.untie_1.fastq/_paired}"."$DBNAME".bwa_mem.sam"
  BAM=${SAM/.sam/}".bam"

  $BWA mem -t 12 $DB $FQ1 $FQ2 > $SAM
  $SAMTOOLS view -Sb -o $BAM $SAM
done
