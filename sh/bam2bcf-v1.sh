#!/bin/bash
SAMTOOLS="/work/project/src/samtools/samtools-1.3.1/samtools"
BCFTOOLS="/work/project/src/samtools/bcftools-1.3.1/bcftools"

DB="/work/project/xenopus.annot/XENLA_JGIv18/XENLA_JGIv18pV2_cdna_final.fa"

RUN_FIXMATE=0
RUN_SORT_BAM=0

for BAM in $(ls *.bwa_mem.bam)
do
  BCF=${BAM/.bam/}".bcf"

  if [ $RUN_FIXMATE ]; then
    echo "Run fixmate: "$FIXMATE
    FIXMATE=${BAM/.bam/}".fixmate.bam"
    if [ ! -e $FIXMATE ]; then
      echo ""
      $SAMTOOLS fixmate -O bam $BAM $FIXMATE
    else
      echo $FIXMATE" exists. Skip."
    fi
  fi

  if [ $RUN_SORT_BAM ]; then
    SORTED=${BAM/.bam/}".sorted"
    if [ ! -e $SORTED".bam" ]; then
      echo ""
      $SAMTOOLS sort -O bam -@ 16 -T $SORTED $BAM > $SORTED".bam"
    else
      echo $SORTED".bam exists. Skip."
    fi
  fi

  if [ ! -e $BCF ]; then
    $SAMTOOLS mpileup -go $BCF -f $DB $SORTED".bam"
  else
    echo $BCF" exists. Skip."
  fi
  #VCF_GZ=${BAM/.bam/}".vcf.gz"
  # $BCFTOOLS call -vmO z -o $VCF_GZ $BCF
done
