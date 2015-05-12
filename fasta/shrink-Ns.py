#!/usr/bin/env python
import os
import sys
import re
import gzip

max_N = 20000
#max_N = 100

filename_fa = sys.argv[1]

f_fa = open(filename_fa,'r')
if( filename_fa.endswith('.gz') ):
    f_fa = gzip.open(filename_fa,'rb')

sys.stderr.write('Read %s ... '%filename_fa)
seq_h = ''
seq_list = dict()
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append( line.strip() )
f_fa.close()
sys.stderr.write('Done\n')

for tmp_h in seq_list.keys():
    count_N = 0
    print ">%s"%tmp_h
    for tmp_n in ''.join(seq_list[tmp_h]):
        if( tmp_n == 'N' ):
            count_N += 1
        else:
            if( count_N < max_N ):
                sys.stdout.write(''.join(['N' for i in range(0,count_N)]))
            else:
                sys.stdout.write(''.join(['N' for i in range(0,max_N)]))
            sys.stdout.write(tmp_n)
            count_N = 0

    sys.stdout.write("\n")
