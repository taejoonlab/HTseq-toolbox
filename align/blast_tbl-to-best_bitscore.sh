#!/bin/bash
BEST="$HOME/git/HTseq-toolbox/align/blast_tbl-to-best_bitscore.py"
for TBL in $(ls *_{tbl,tbl.gz})
do
  OUT=$TBL"_best"
  if [ ! -e $OUT ]; then
    echo $TBL
    $BEST $TBL
  fi
done
