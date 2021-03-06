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
        tmp_count = float(tokens[7])
        rv[t_id] = {'count': tmp_count}
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
    exp[tmp_group][tmp_sample] = read_count(tmp_filename)
    sample_list.append(tmp_sample)
    gene_list += exp[tmp_group][tmp_sample].keys()
f.close()

group_list = sorted(group_list)
sample_list = sorted(sample_list)

f_indiv_count = open('%s.indiv_p_rpkm.txt'%output_name,'w')
f_mean_count  = open('%s.mean_p_rpkm.txt'%output_name,'w')
f_low_count = open('%s.low_p_rpkm.txt'%output_name,'w')

f_indiv_count.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_low_count.write('SeqID\t%s\n'%('\t'.join(sample_list)))
f_mean_count.write('SeqID\t%s\n'%('\t'.join(group_list)))
for tmp_id in sorted(list(set(gene_list))):
    count_indiv = dict()
    count_mean = dict()
    count_nonzero = 0
    for tmp_group in group_list:
        count_sum = 0
        for tmp_sample in exp[tmp_group].keys():
            if( exp[tmp_group][tmp_sample].has_key(tmp_id) ):
                tmp_count = exp[tmp_group][tmp_sample][tmp_id]['count']
                count_indiv[tmp_sample] = tmp_count
                count_sum += tmp_count
                if( tmp_count > 1 ):
                    count_nonzero += 1
            else:
                count_indiv[tmp_sample] = 0.0
        count_mean[tmp_group] = count_sum*1.0/len(exp[tmp_group])
    
    if( count_nonzero < 2 or sum(count_indiv.values()) < 2.0 ):
        f_low_count.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%count_indiv[x] for x in sample_list])))
        continue
    f_indiv_count.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%count_indiv[x] for x in sample_list])))
    f_mean_count.write('%s\t%s\n'%(tmp_id,'\t'.join(['%.3f'%count_mean[x] for x in group_list])))

f_low_count.close()
f_indiv_count.close()
f_mean_count.close()
