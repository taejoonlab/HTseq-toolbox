#!/usr/bin/env python
import os
import sys
import re

filename_fa = sys.argv[1]

seq_h = ''
seq_list = dict()
f_fa = open(filename_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()

filename_base = os.path.basename(filename_fa)
filename_base = re.sub(r'.fa[sta]*','',filename_base)

f_out = open('%s.trim53N.fa'%filename_base,'w')
f_log = open('%s.trim53N.log'%filename_base,'w')
for tmp_h in sorted(seq_list.keys(),reverse=True):
    tmp_seq = ''.join(seq_list[tmp_h])

    if( tmp_seq.startswith('N') or tmp_seq.endswith('N') ):
        if( len(set(tmp_seq)) == 1 ):
            f_log.write('TrimmedOut: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), 0))
            sys.stderr.write('TrimmedOut: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), 0))
        else:
            tmp_start = 0
            tpm_end = len(tmp_seq)
            if( tmp_seq.startswith('N') ):
                for tmp_i in range(0,len(tmp_seq)):
                    if( tmp_seq[tmp_i] != 'N' ):
                        tmp_start = tmp_i
                        break
            elif( tmp_seq.endswith('N') ):
                for tmp_i in range(len(tmp_seq)-1,0,-1):
                    if( tmp_seq[tmp_i] != 'N' ):
                        tmp_end = tmp_i
                        break
            
            trimmed_seq = tmp_seq[tmp_start:tmp_end]
            if( len(trimmed_seq) > 1000 ):
                f_log.write('Trimmed: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), len(trimmed_seq)))
                sys.stderr.write('Trimmed: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), len(trimmed_seq)))
                f_out.write('>%s\n%s\n'%(tmp_h, trimmed_seq))
            else:
                f_log.write('TrimmedOut: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), len(trimmed_seq)))
                sys.stderr.write('TrimmedOut: %s (%d -> %d)\n'%(tmp_h, len(tmp_seq), len(trimmed_seq)))
    else:
        f_log.write('NoChange: %s\n'%(tmp_h))
        sys.stderr.write('NoChange: %s\n'%(tmp_h))
        f_out.write('>%s\n%s\n'%(tmp_h, tmp_seq))

f_out.close()
f_log.close()
