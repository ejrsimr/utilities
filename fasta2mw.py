#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ejr: 2023-11-08
# read in a FASTA file and output the molecular weight
# of each amino acid sequence

import sys

aa2mw = {
"A":	89.1,
"R":	174.2,
"N":	132.1,
"D":	133.1,
"C":	121.2,
"E":	147.1,
"Q":	146.2,
"G":	75.1,
"H":	155.2,
"I":	131.2,
"L":	131.2,
"K":	146.2,
"M":	149.2,
"F":	165.2,
"P":	115.1,
"S":	105.1,
"T":	119.1,
"W":	204.2,
"Y":	181.2,
"V":	117.1,
"X":	0,
"*":    0
}

def main():
    fasta_file = sys.argv[1]
    fasta_dict = fasta2dict(fasta_file)
    weights = fasta2mw(fasta_dict)

    print("seq_id\tmolecular_weight_kDa")
    for k,v in weights.items():
        kd = round(v / 1000, 2)
        print("\t".join([k, str(kd)]))

def fasta2mw(fasta_dict):
    # calculate the molecular weight of each sequence
    # in a FASTA file
    weights = {}

    for header in fasta_dict:
        sequence = fasta_dict[header]
        weights[header] = 0
        for aa in sequence:
            weights[header] += aa2mw[aa]

    return(weights)

def fasta2dict(fasta_file):
    # read a FASTA file into a dictionary
    fasta_dict = {}

    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('>'):
                # use first word as header
                header = line.split()[0][1:]
                fasta_dict[header] = ''
            else:
                fasta_dict[header] += line

    return(fasta_dict)

if __name__ == "__main__":
    main()