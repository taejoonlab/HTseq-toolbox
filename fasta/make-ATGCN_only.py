#!/usr/bin/env python
import os
import sys

filename_fa = sys.argv[1]

seq_list = dict()
f_fa = open(filename_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append( line.strip() )
f_fa.close()

f_out = open('%s.ATGC_only'%filename_fa,'w')
for tmp_h in sorted(seq_list.keys()):
    tmp_residual = set( (''.join(seq_list[tmp_h])).upper() ) - set(['A','T','G','C','N'])
    if( len(tmp_residual) > 0 ):
        continue
    f_out.write('>%s\n%s\n'%(tmp_h, "\n".join(seq_list[tmp_h])))
f_out.close()
