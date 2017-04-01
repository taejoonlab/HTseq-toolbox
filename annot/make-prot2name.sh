#!/bin/bash
DIRNAME_ENS="/work/project/pub/ens/70"
echo ""> ens70.prot2name

for FILENAME_GTF in $(ls $DIRNAME_ENS/*gtf.gz)
do
  SP_NAME=$(basename $FILENAME_GTF|awk -F"." '{print $1}')
  echo $FILENAME_GTF $SP_NAME
  zgrep 'P0' $FILENAME_GTF | grep 'protein_coding' | awk -F"\t" '{print $9}' | awk -v SP=$SP_NAME -F";" '{print $4"\t"$7"\t"SP}' | sort -u >> ens70.prot2name
done
