#!/usr/bin/python
import os
import sys
import gzip
seqlen = dict()
seq_h = ''
filename_fa = sys.argv[1]
f = open(filename_fa,'r')
if( filename_fa.endswith('.gz') ):
    f = gzip.open(filename_fa,'rb')

for line in f:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seqlen[seq_h] = 0
    else:
        seqlen[seq_h] += len(line.strip())
f.close()

len_list = sorted(seqlen.values(), reverse=True)
concat_total = sum(len_list)
concat_lt1k = sum([x for x in len_list if x > 1000])
N50 = 0
N50_lt1k = 0
cum_len = 0

for tmp_len in len_list:
    cum_len += tmp_len
    if( N50 == 0 and cum_len < concat_total*0.5 ):
        N50 = tmp_len
    if( N50_lt1k == 0 and cum_len < concat_lt1k*0.5 ):
        N50_lt1k = tmp_len

print "# seqs: ",len(len_list)
print "Concat. length: %d (%.1f Mb)"%(concat_total, concat_total*1.0/1000000)
print "Concat. length of len(seq) > 1kb: %d (%.3f pct)"%(concat_lt1k, concat_lt1k*100.0/concat_total)
print "Mean: ",sum(len_list)/len(len_list)
print "Median: ",sorted(len_list)[ int(len(len_list)*0.5) ]
print ">1000bp: ",len([x for x in len_list if x > 1000])
print ">10kbp: ",len([x for x in len_list if x > 10000])
print ">50kbp: ",len([x for x in len_list if x > 50000])

print "N50 total:",N50
print "N50 with len(seq) > 1kb:", N50_lt1k
