#!/usr/bin/python
import os
import sys
import re

filename_conf = sys.argv[1]
output_name = filename_conf.split('.')[0]

def read_count(filename):
    rv = dict()
    f = open(filename,'r')
    for line in f:
        if( line.startswith('#') ):
            continue
        tokens = line.strip().split("\t")
        t_id = tokens[0]
        if( t_id == 'gene_id' ):
            continue
        tmp_rpkm = float(tokens[6])
        rv[t_id] = {'rpkm': tmp_rpkm}
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
    exp[tmp_group][tmp_sample] = read_rpkm(tmp_filename)
    sample_list.append(tmp_sample)
    gene_list += exp[tmp_group][tmp_sample].keys()
f.close()

group_list = sorted(group_list)
sample_list = sorted(sample_list)

f_indiv_rpkm = open('%s.indiv_rpkm.txt'%output_name,'w')
f_mean_rpkm  = open('%s.mean_rpkm.txt'%output_name,'w')
f_low_rpkm = open('%s.low_rpkm.txt'%output_name,'w')

f_indiv_rpkm.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_low_rpkm.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_mean_rpkm.write('SeqID\t%s\n'%('\t'.join(group_list)))
for tmp_id in sorted(list(set(gene_list))):
    rpkm_indiv = dict()
    rpkm_mean = dict()
    count_nonzero = 0
    for tmp_group in group_list:
        rpkm_sum = 0
        for tmp_sample in exp[tmp_group].keys():
            if( exp[tmp_group][tmp_sample].has_key(tmp_id) ):
                tmp_rpkm = exp[tmp_group][tmp_sample][tmp_id]['rpkm']
                rpkm_indiv[tmp_sample] = tmp_rpkm
                rpkm_sum += tmp_rpkm
                if( tmp_rpkm > 1 ):
                    count_nonzero += 1
            else:
                rpkm_indiv[tmp_sample] = 0.0
        rpkm_mean[tmp_group] = rpkm_sum*1.0/len(exp[tmp_group])
    
    if( count_nonzero < 2 or sum(rpkm_indiv.values()) < 2.0 ):
        f_low_rpkm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%rpkm_indiv[x] for x in sample_list])))
        continue
    f_indiv_rpkm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%rpkm_indiv[x] for x in sample_list])))
    f_mean_rpkm.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%rpkm_mean[x] for x in group_list])))

f_low_rpkm.close()
f_indiv_rpkm.close()
f_mean_rpkm.close()
