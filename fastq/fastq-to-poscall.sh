#!/bin/bash
DIR="$( dirname "${BASH_SOURCE[0]}" )"
POS_CALL="$DIR/fastq-to-pos_call.py"

for FQ in $(ls *fastq)
do
  echo $FQ
  $POS_CALL $FQ
done
