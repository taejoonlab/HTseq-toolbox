#!/bin/bash
for SRA in $(ls *sra)
do
  fastq-dump --split-files $SRA
done
