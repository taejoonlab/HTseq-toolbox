#!/usr/bin/env python
import os
import sys
import re
import gzip

filename_sam = sys.argv[1]

f_sam = open(filename_sam,'r')
if( filename_sam.endswith('.gz') ):
    f_sam = gzip.open(filename_sam,'rb')

seq_len = dict()
read_freq = dict()
pair_freq = dict()
for line in f_sam:
    if( line.startswith('@SQ') ):
        tokens = line.strip().split()
        seq_id = re.sub(r'^SN:','',tokens[1])
        seq_len[seq_id] = int(re.sub(r'^LN:','',tokens[2]))
        continue
    elif( len(line.split()[0]) < 5 ):
        continue

    tokens = line.strip().split("\t")
    read_id = tokens[0]
    pair_id = read_id.split('/')[0]
    tmp_flag = int(tokens[1])
    h1_t = tokens[2]
    h1_pos = int(tokens[3])
    h2_t = tokens[6]
    h2_pos = int(tokens[7])

    if( h1_t == '*' ):
        continue
    if( tmp_flag & 4 ):
        continue
    if( h1_pos == h2_pos ):
        continue

    if( not read_freq.has_key(h1_t) ):
        read_freq[h1_t] = 0
    read_freq[h1_t] += 1
    if( h1_t == h2_t or h2_t == '=' ):
        if( not pair_freq.has_key(h1_t) ):
            pair_freq[h1_t] = 0
        pair_freq[h1_t] += 1
f_sam.close()

norm = dict()
sum_T = 0
sum_read_freq = sum(read_freq.values())
sum_pair_freq = sum(pair_freq.values())

f_out = open('%s.rpkm+cpm'%filename_sam,'w')
f_out.write('# ReadSum=%d, PairSum=%d\n'%(sum_read_freq, sum_pair_freq))
f_out.write("#SeqID\tReadCount\tPairCount\tReadCPM\tPairCPM\tSeqLen\tReadRPKM\tPairRPKM\n")
for tmp_id in sorted(read_freq.keys()):
    tmp_read_count = read_freq[tmp_id]
    tmp_read_CPM = 1000000.0/sum_read_freq

    tmp_pair_count = 0
    tmp_pair_CPM = 0.0
    if( pair_freq.has_key(tmp_id) ):
        tmp_pair_count = pair_freq[tmp_id]
        tmp_pair_CPM = 1000000.0/sum_pair_freq
    
    f_out.write("%s\t%d\t%d\t%.3f\t%.3f\t"%(tmp_id, tmp_read_count, tmp_pair_count, tmp_read_count*tmp_read_CPM, tmp_pair_count*tmp_pair_CPM))
    tmp_len = 0
    if( seq_len.has_key(tmp_id) ):
        tmp_len = seq_len[tmp_id]
        tmp_read_RPKM = tmp_read_CPM * 1000.0/tmp_len
        tmp_pair_RPKM = tmp_pair_CPM * 1000.0/tmp_len
        f_out.write('%d\t%.3f\t%.3f\n'%(tmp_len,tmp_read_count*tmp_read_RPKM, tmp_pair_count*tmp_pair_RPKM))
    else:
        f_out.write('%d\t%.3f\t%.3f\n'%(0,0,0))
f_out.close()
