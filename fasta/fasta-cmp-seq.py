#!/usr/bin/env python
import os
import sys
import gzip

def read_s2h(filename):
    seq_list = dict()
    seq_h = ''
    f = open(filename,'r')
    if( filename.endswith('.gz') ):
        f = gzip.open(filename,'rb')
    for line in f:
        if( line.startswith('>') ):
            seq_h = line.strip().lstrip('>')
            seq_list[seq_h] = []
        else:
            seq_list[seq_h].append(line.strip())
    f.close()

    rv = dict()
    for tmp_h in seq_list.keys():
        tmp_seq = ''.join(seq_list[tmp_h])
        if( not rv.has_key(tmp_seq) ):
            rv[tmp_seq] = []
        rv[tmp_seq].append(tmp_h)
    return rv

filename_1 = sys.argv[1]
filename_2 = sys.argv[2]

s2h_1 = read_s2h(filename_1)
s2h_2 = read_s2h(filename_2)

f_cmp = open('%s.%s.cmp_list'%(filename_1,filename_2),'w')
f_only1 = open('%s.%s.cmp_only1.fa'%(filename_1,filename_2),'w')
f_only2 = open('%s.%s.cmp_only1.fa'%(filename_1,filename_2),'w')
f_cmp.write('#File_1 : %s\n'%filename_1)
f_cmp.write('#File_2 : %s\n'%filename_2)
f_cmp.write('#ID@File_1\tID@File_2\n')

for tmp_s in s2h_1.keys():
    if( s2h_2.has_key(tmp_s) ):
        f_cmp.write('%s\t%s\n'%(';'.join(sorted(list(set(s2h_1[tmp_s])))), ';'.join(sorted(list(set(s2h_2[tmp_s]))))))
    else:
        f_only1.write('>%s\n%s\n'%(';'.join(sorted(list(set(s2h_1[tmp_s])))),tmp_s))

f_cmp.close()
f_only1.close()

for tmp_s in s2h_2.keys():
    if( not s2h_1.has_key(tmp_s) ):
        f_only2.write('>%s\n%s\n'%(';'.join(sorted(list(set(s2h_2[tmp_s])))),tmp_s))
f_only2.close()
