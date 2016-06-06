#!/bin/bash
DIR="$( dirname "${BASH_SOURCE[0]}" )"
BEST="$DIR/blast_tbl-to-best_bitscore.py"

TBL_COUNT=`ls -l *_tbl 2>/dev/null | wc -l`
if [ $TBL_COUNT != 0 ]; then
  for TBL in $(ls *_tbl)
  do
    OUT=$TBL"_best"
    if [ ! -e $OUT ]; then
      echo $TBL
      $BEST $TBL
    else
      echo "$OUT exists. Skip."
    fi
  done
else
  echo "NO file ends with *_tbl. Skip."
fi

TBL_COUNT=`ls -l *_tbl.gz 2>/dev/null | wc -l`
if [ $TBL_COUNT != 0 ]; then
  for TBL in $(ls *_tbl.gz)
  do
    OUT=${TBL/.gz$/}"_best"
    if [ ! -e $OUT ]; then
      echo $TBL
      $BEST $TBL
    else
      echo "$OUT exists. Skip."
    fi
  done
else
  echo "NO file ends with *_tbl.gz. Skip."
fi
