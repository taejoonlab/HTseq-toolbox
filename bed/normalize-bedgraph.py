#!/usr/bin/env python3
import sys

filename_bed = sys.argv[1]

sum_cov = 0
f_bed = open(filename_bed, 'r')
for line in f_bed:
    tokens = line.strip().split("\t")
    start_pos = int(tokens[1])
    end_pos = int(tokens[2])
    data_value = float(tokens[3])
    if data_value > 0:
        sum_cov += data_value * (end_pos - start_pos)
f_bed.close()

norm_factor = 1000000000 / sum_cov
f_out = open('%s.norm' % filename_bed, 'w')
f_bed = open(filename_bed, 'r')
for line in f_bed:
    tokens = line.strip().split("\t")
    start_pos = int(tokens[1])
    end_pos = int(tokens[2])
    data_value = float(tokens[3])
    f_out.write("%s\t%d\t%d\t%.3f\n" %
                (tokens[0], start_pos, end_pos, data_value*norm_factor))
f_bed.close()
f_out.close()
