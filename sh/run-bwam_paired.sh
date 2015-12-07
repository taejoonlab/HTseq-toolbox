#!/bin/bash
NUM_THREADS=6

SAMTOOLS="/work/src/samtools/samtools-1.2/samtools"
BWA="/work/src/bwa/bwa-0.7.12/bwa"

DB="/work/taejoon/xenopus.db/bwadb/XENLA_JGIv18pV3_cdna_final"
DBNAME=$(basename $DB)

for FQ1 in $(ls ../fastq/*.untie_1.fastq)
do
  FQ2=${FQ1/_1/_2}

  SAM=$(basename $FQ1)
  SAM=${SAM/.untie_1.fastq/_paired}"."$DBNAME".bwa_mem.sam"
  BAM=${SAM/.sam/}".bam"

  $BWA mem -t 12 $DB $FQ1 $FQ2 > $SAM
  $SAMTOOLS view -Sb -o $BAM $SAM
done
