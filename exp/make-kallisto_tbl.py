#!/usr/bin/env python
import os
import sys

def read_tsv(filename_tsv):
    rv = dict()
    f = open(filename_tsv,'r')
    tokens = f.readline().strip()
    for line in f:
        tokens = line.strip().split("\t")
        tmp_id = tokens[0]
        tmp_tpm = float(tokens[4])
        rv[ tmp_id ] = tmp_tpm
    f.close()
    return rv

filename_conf = sys.argv[1]
#Liver06	Yang2012_DANREtx_liver_SRR392106.DANRE_ens85_cdna_longest.abundance.tsv

sample_list = []
gene_list = []
tpm_list = dict()
f_conf = open(filename_conf,'r')
for line in f_conf:
    tmp_name, tmp_filename = line.strip().split("\t")
    tpm_list[tmp_name] = read_tsv(tmp_filename)
    gene_list += tpm_list[tmp_name].keys()
    sample_list.append(tmp_name)
f_conf.close()

gene_list = sorted(list(set(gene_list)))
f_out = open('%s.kallisto.txt'%(filename_conf.replace('.conf','')), 'w')
f_out.write('SeqID\t%s\n'%('\t'.join(sample_list)))
for tmp_gene in gene_list:
    out_str = []
    for tmp_sample in sample_list:
        if( tpm_list.has_key(tmp_sample) and tpm_list[tmp_sample].has_key(tmp_gene) ):
            out_str.append('%.3f'%tpm_list[tmp_sample][tmp_gene])
        else:
            out_str.append('%.3f'%(0))
    f_out.write('%s\t%s\n'%(tmp_gene, '\t'.join(out_str)))
f_out.close()
