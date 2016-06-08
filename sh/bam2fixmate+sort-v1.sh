#!/bin/bash
SAMTOOLS="/work/project/src/samtools/samtools-1.3.1/samtools"

for BAM in $(ls *.bwa_mem.bam)
do
  FIXMATE=${BAM/.bam/}".fixmate.bam"
  if [ ! -e $FIXMATE ]; then
    $SAMTOOLS fixmate -O bam $BAM $FIXMATE
  else
    echo $FIXMATE" exists. Skip."
  fi

  SORTED=${BAM/.bam/}".sorted"
  if [ ! -e $SORTED".bam" ]; then
    $SAMTOOLS sort -O bam -@ 16 -T $SORTED $BAM > $SORTED".bam"
  else
    echo $SORTED".bam exists. Skip."
  fi
done
