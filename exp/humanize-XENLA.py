#!/usr/bin/env python3
import os
import sys

filename_cpm = sys.argv[1]

hs_list = dict()
f_cpm = open(filename_cpm,'r')
for line in f_cpm:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    hs_id = tokens[0].split('|')[1].replace('HS=','')

    if hs_id == 'NA':
        continue

    if not hs_id in hs_list:
        hs_list[hs_id] = {'read_count':int(tokens[1]), 'pair_count':int(tokens[2])}
    else:
        hs_list[hs_id]['read_count'] += int(tokens[1])
        hs_list[hs_id]['pair_count'] += int(tokens[2])
f_cpm.close()

for tmp_hs_id in sorted(hs_list.keys()):
    print("%s\t%d\t%d"%(tmp_hs_id, hs_list[tmp_hs_id]['read_count'], hs_list[tmp_hs_id]['pair_count']))
