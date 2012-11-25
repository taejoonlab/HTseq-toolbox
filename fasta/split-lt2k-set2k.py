#!/usr/bin/python
import os
import sys
import gzip

filename_fa = sys.argv[1]

h = ''
seq_list = dict()
seqlen = dict()
f_fa = open(filename_fa,'r')
if( filename_fa.endswith('.gz') ):
    f_fa = gzip.open(filename_fa,'rb')
for line in f_fa:
    if( line.startswith('>') ):
        h = line.strip().lstrip('>')
        seq_list[h] = []
        seqlen[h] = 0
    else:
        seq_list[h].append( line.strip() )
        seqlen[h] += len( line.strip() )
f_fa.close()

filename_base = filename_fa.replace('.fasta','').replace('.fa','').replace('_fa','').replace('.gz','')

f_lt2k = open('%s_lt2k_fa'%filename_base,'w')
f_set2k = open('%s_set2k_fa'%filename_base,'w')

is_lt2k = 0
for tmp_h in sorted( seqlen.keys(), key=seqlen.get, reverse=True):
    tmp_seq = ''.join(seq_list[tmp_h])
    if( len(tmp_seq) > 2000 ):
        f_lt2k.write('>%s\n%s\n'%(tmp_h,tmp_seq))
    else:
        f_set2k.write('>%s\n%s\n'%(tmp_h,tmp_seq))

f_lt2k.close()
f_set2k.close()
