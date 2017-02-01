#!/usr/bin/env python
import os
import sys
import gzip

filename_fq1 = sys.argv[1]
filename_fq2 = sys.argv[2]
filename_out = sys.argv[3]

f_fq1 = open(filename_fq1,'r')
if( filename_fq1.endswith('.gz') ):
    f_fq1 = gzip.open(filename_fq1,'rb')

f_fq2 = open(filename_fq2,'r')
if( filename_fq2.endswith('.gz') ):
    f_fq2 = gzip.open(filename_fq2,'rb')

f_out = open('%s.paired.fastq'%filename_out,'w')
for line in f_fq1:
    h_nseq1 = line.strip()
    nseq1 = f_fq1.next().strip()
    h_qseq1 = f_fq1.next().strip()
    qseq1 = f_fq1.next().strip()

    h_nseq2 = f_fq2.next().strip()
    nseq2 = f_fq2.next().strip()
    h_qseq2 = f_fq2.next().strip()
    qseq2 = f_fq2.next().strip()

    f_out.write('%s\n%s\n+\n%s\n'%(h_nseq1,nseq1,qseq1))
    f_out.write('%s\n%s\n+\n%s\n'%(h_nseq2,nseq2,qseq2))

f_fq1.close()
f_fq2.close()
f_out.close()
