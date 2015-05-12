#!/usr/bin/env python
import os
import sys
import gzip

filename_fa = sys.argv[1]
query_h = sys.argv[2].strip()

f = open(filename_fa,'r')
if( filename_fa.endswith('.gz') ):
    f = gzip.open(filename_fa,'rb')

is_query = 0
seq_list = []
for line in f:
    if( line.startswith('>') ):
        tmp_h = line.strip().lstrip('>')
        if( tmp_h == query_h ):
            print ">%s"%(tmp_h)
            is_query = 1
        else:
            is_query = 0
    elif( is_query > 0 ):
        print line.strip()
f.close()
