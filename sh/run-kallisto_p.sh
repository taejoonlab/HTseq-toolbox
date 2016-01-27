#!/bin/bash

#~/src/kallisto/kallisto_linux-v0.42.4/kallisto index -i RAT_ens80_cdna_longest_NR RAT_ens80_cdna_longest_NR.fa 
KALLISTO="/home/taejoon/src/kallisto/kallisto_linux-v0.42.4/kallisto"
DB="RAT_ens80_cdna_longest_NR"

for FQ1 in $(ls ../fastq/*R1.raw.fastq.gz)
do
  FQ2=${FQ1/_R1/_R2}
  OUT=$(basename $FQ1)
  OUT=${OUT/_R1.raw.fastq.gz/}"."$DB
  echo $OUT
  $KALLISTO quant -i $DB -t 16 $FQ1 $FQ2 -o $OUT
done
