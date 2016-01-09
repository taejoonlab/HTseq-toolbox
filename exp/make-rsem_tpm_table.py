#!/usr/bin/python
import os
import sys
import re

filename_conf = sys.argv[1]
output_name = filename_conf.split('.')[0]

def read_results(filename):
    rv = dict()
    f = open(filename,'r')
    for line in f:
        tokens = line.strip().split("\t")
        t_id = tokens[0]
        if( t_id == 'gene_id' ):
            continue
        tmp_tpm = float(tokens[5])
        rv[t_id] = {'tpm': tmp_tpm}
    f.close()
    return rv

exp = dict()
group_list = []
sample_list = []
gene_list = []

#Filename	GroupName	SampleName
#Chang201302_XENLA_Animal_paired.XENLA_JGIv18pV2_cdna_final.bwa_mem.rsem.genes.results	Animal	Animal_1
f = open(filename_conf,'r')
headers = f.readline().strip().split("\t")
for line in f:
    tokens = line.strip().split()
    tmp_filename = tokens[ headers.index('Filename') ]
    tmp_group = tokens[ headers.index('GroupName') ]
    tmp_sample = tokens[ headers.index('SampleName') ]
    if( not exp.has_key(tmp_group) ):
        exp[tmp_group] = dict()
        group_list.append(tmp_group)
    exp[tmp_group][tmp_sample] = read_results(tmp_filename)
    sample_list.append(tmp_sample)
    gene_list += exp[tmp_group][tmp_sample].keys()
f.close()

group_list = sorted(group_list)
sample_list = sorted(sample_list)

f_indiv_tpm = open('%s.indiv_tpm.txt'%output_name,'w')
f_mean_tpm  = open('%s.mean_tpm.txt'%output_name,'w')
f_low_tpm = open('%s.low_tpm.txt'%output_name,'w')

f_indiv_tpm.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_low_tpm.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_mean_tpm.write('SeqID\t%s\n'%('\t'.join(group_list)))
for tmp_id in sorted(list(set(gene_list))):
    tpm_indiv = dict()
    tpm_mean = dict()
    count_nonzero = 0
    for tmp_group in group_list:
        tpm_sum = 0
        for tmp_sample in exp[tmp_group].keys():
            if( exp[tmp_group][tmp_sample].has_key(tmp_id) ):
                tmp_tpm = exp[tmp_group][tmp_sample][tmp_id]['tpm']
                tpm_indiv[tmp_sample] = tmp_tpm
                tpm_sum += tmp_tpm
                if( tmp_tpm > 0 ):
                    count_nonzero += 1
            else:
                tpm_indiv[tmp_sample] = 0.0
        tpm_mean[tmp_group] = tpm_sum*1.0/len(exp[tmp_group])
    
    if( count_nonzero < 2 ):
        f_low_tpm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%tpm_indiv[x] for x in sample_list])))
        continue
    f_indiv_tpm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%tpm_indiv[x] for x in sample_list])))
    f_mean_tpm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%tpm_mean[x] for x in group_list])))
f_indiv_tpm.close()
f_mean_tpm.close()

