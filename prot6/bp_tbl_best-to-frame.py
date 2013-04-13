#!/usr/bin/python
import os
import sys

data_name = sys.argv[1]

frames = dict()
count_best = 0
for filename in os.listdir('.'):
    if( not filename.startswith(data_name) ):
        continue
    if( not filename.endswith('bp+_tbl_best') ):
        continue

    sys.stderr.write('Read %s\n'%filename)
    count_best += 1

    f = open(filename,'r')
    for line in f:
        if( line.startswith('#') ):
            continue
        tokens = line.strip().split("\t")
        q_id = tokens[0]
        q_tokens = q_id.split('|')
        q_frame = q_tokens[-1]
        q_orig_id = '|'.join(q_tokens[:-1])
        align_len = int(tokens[4])

        if( not frames.has_key(q_orig_id) ):
            frames[q_orig_id] = dict()
        if( not frames[q_orig_id].has_key(q_frame) ):
            frames[q_orig_id][q_frame] = {'count':0, 'align_len':align_len}
        frames[q_orig_id][q_frame]['count'] += 1
        if( align_len > frames[q_orig_id][q_frame]['align_len'] ):
            frames[q_orig_id][q_frame]['align_len'] = align_len
    f.close()

count_unique = 0
count_dubious = 0
f_unique = open('%s.unique_frame'%data_name,'w')
f_dubious = open('%s.dubious_frame'%data_name,'w')
for tmp_q in sorted(frames.keys()):
    if( len(frames[tmp_q].keys()) == 1 ):
        f_unique.write("%s|%s\n"%(tmp_q,frames[tmp_q].keys()[0]))
        count_unique += 1
    else:
        freq_map = dict()
        align_len_map = dict()
        for tmp_frame in frames[tmp_q].keys():
            tmp = frames[tmp_q][tmp_frame]
            tmp_tag = '%s=%d|%d'%(tmp_frame,tmp['count'],tmp['align_len']) 
            freq_map[ tmp_tag ] = tmp['count']
            align_len_map[ tmp_tag ] = tmp['align_len']
         
        tmp_tag_list = sorted(freq_map.keys(), key=freq_map.get, reverse=True)
        tag_1 = tmp_tag_list[0]
        tag_2 = tmp_tag_list[1]
        if( freq_map[tag_1] == freq_map[tag_2] ):
            tmp_tag_list = sorted(align_len_map.keys(), key=align_len_map.get, reverse=True)
            tag_1 = tmp_tag_list[0]
            tag_2 = tmp_tag_list[1]

        if( align_len_map[tag_1] * 0.5 > align_len_map[tag_2] ):
            f_unique.write("%s|%s\n"%(tmp_q,frames[tmp_q].keys()[0]))
            count_unique += 1
        else:
            f_dubious.write("%s\t%s\n"%(tmp_q,','.join([x for x in tmp_tag_list] )))
            count_dubious += 1
f_unique.close()
f_dubious.close()

print "unique=%d, dubious=%d"%(count_unique,count_dubious)
