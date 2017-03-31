filename_sp_list = 'MODtree.species_list.txt'
filename_HS_names = 'ens70.HUMAN.prot2name.gz'
filename_names = 'ens70.prot2name.gz'

import gzip

def get_tax2sp():
    tax2sp = dict()
    f_list =  open(filename_sp_list,'r')
    for line in f_list:
        tokens = line.strip().split("\t")
        sp_code = tokens[0]
        tax_id = tokens[2]
        tax2sp[tax_id] = sp_code
    f_list.close()
    return tax2sp

def get_HS_prot2names():
    HS_names = dict()
    f_names = gzip.open(filename_HS_names,'rt')
    for line in f_names:
        tokens = line.replace('"','').split()
        if len(tokens) != 4:
            continue
        HS_names[tokens[3]] = tokens[1]
    f_names.close()
    return HS_names

def get_prot2names():
    prot_names = dict()
    f_names = gzip.open(filename_names,'rt')
    for line in f_names:
        tokens = line.replace('"','').split()
        if len(tokens) != 4:
            continue
        prot_names[tokens[3]] = tokens[1]
    f_names.close()
    return prot_names
