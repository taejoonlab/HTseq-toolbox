#!/bin/bash
DIRNAME_ENS="/work/project/pub/ens/70"
zgrep 'P0' $DIRNAME_ENS/*.gtf.gz | grep 'protein_coding' | awk -F"\t" '{print $9}' | awk -F";" '{print $4"\t"$7}' | sort -u > ens70.prot2name
zgrep 'ENSP0' $DIRNAME_ENS/*.gtf.gz | grep 'protein_coding' | awk -F"\t" '{print $9}' | awk -F";" '{print $4"\t"$7}' | sort -u > ens70.HUMAN.prot2name
