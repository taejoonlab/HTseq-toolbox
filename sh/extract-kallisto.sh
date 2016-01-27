#!/bin/bash
SAMPLE=$1

for ORIG in $(ls *$SAMPLE*/abundance.*)
do
    NEW=${ORIG/\/abundance/.abundance}
    echo "$ORIG --> $NEW"
    mv $ORIG $NEW
done
