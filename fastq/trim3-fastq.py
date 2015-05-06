#!/usr/bin/python
import os
import sys
import re
import gzip

filename_fq = sys.argv[1]
read_len = int(sys.argv[2])

filename_base =  re.sub(r'.[a-z]*fastq[.gz]*','',filename_fq)
f_out = open("%s.trim3_%d.fastq"%(filename_base, read_len),'w')

f_fq = open(filename_fq,'r')
if( filename_fq.endswith('.gz') ):
    f_fq = gzip.open(filename_fq,'rb')

for line in f_fq:
    if( line.startswith('@') ):
        h = line.strip()
        nseq = f_fq.next().strip()
        qh = f_fq.next()
        qseq = f_fq.next().strip()
        f_out.write("%s\n%s\n+\n%s\n"%(h,nseq[:read_len],qseq[:read_len]))
f_fq.close()
f_out.close()
