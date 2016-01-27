#!/bin/bash

#~/src/kallisto/kallisto_linux-v0.42.4/kallisto index -i RAT_ens80_cdna_longest_NR RAT_ens80_cdna_longest_NR.fa 
KALLISTO="/home/taejoon/src/kallisto/kallisto_linux-v0.42.4/kallisto"

SPECIES="MOUSE"
DB="../../"$SPECIES"_ens80_cdna_longest_NR.kallisto.idx"
DBNAME=$(basename $DB)
DBNAME=${DBNAME/.kallisto.idx}

for FQ1 in $(ls ../fastq/*$SPECIES*fastq.gz)
do
  OUT=$(basename $FQ1)
  OUT=${OUT/.fastq.gz/}"."$DBNAME
  OUT=${OUT/.called/}
  echo $OUT
  $KALLISTO quant --single -l 200 -s 0.1 -i $DB -t 16 -o $OUT $FQ1
done
