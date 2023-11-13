#!/usr/bin/env python3
# calculate codon usage for longest CDSes from a FASTA file 
# ejr: 2023-11-13

import fileinput
import signal
import re

###############################################################################
### Main
###############################################################################
def main():
    fh = fileinput.input()
    fasta = read_fasta(fh)

    cds = fasta2longestcds(fasta)
    codon_usage = count_codons(cds)
    print_codon_usage(codon_usage)

    exit(0)

###############################################################################
### Get six frame translation for each sequence in FASTA file
###############################################################################
def fasta2longestcds(fasta):
    cds = {}

    for header in fasta:
        seq = fasta[header]
        seq = seq.upper()
        seq = seq.replace('U', 'T')
        # create list of possible CDSes in all 6 frames
        cdses = list()
        for i in range(3):
            frame = seq[i:]
            # split every 3 base pairs
            codons = [frame[j:j+3] for j in range(0, len(frame), 3)]
            codon_str = "_".join(codons)
            # 232 (4 * 58) is at least a 60aa orf ?: captures whole string instead of parens
            matches = re.findall(r'ATG_.{232,}_(?:TAA|TAG|TGA)', codon_str)
            cdses.extend(matches)

            # reverse strand
            frame = reverse_complement(seq)[i:]

            # split every 3 base pairs
            codons = [frame[j:j+3] for j in range(0, len(frame), 3)]
            codon_str = "_".join(codons)
            # 232 is at least a 60aa orf ?: captures whole string instead of parens
            matches = re.findall(r'(ATG_.{232,}_(?:TAA|TAG|TGA))', codon_str)
            cdses.extend(matches)

        # keep longest cds (format: ATG_XXX_XXX_TAG)
        if len(cdses) > 0:
            cds[header] = max(cdses, key=len)       

    return cds

###############################################################################
# Reverse Complement Sequence
###############################################################################
def reverse_complement(seq):
    bases = str.maketrans('AGCTagct','TCGAtcga')
    return seq.translate(bases)[::-1]

###############################################################################
### Calculate codon usage for longest CDSes
###############################################################################
def count_codons(cds):
    codon_usage = {}
    total = 0
    # count number of occurances of each codon
    for header in cds:
        codon_str = cds[header]
        codons = codon_str.split("_")
        for codon in codons:
            if codon not in codon_usage:
                codon_usage[codon] = 0
            codon_usage[codon] += 1
            total += 1

    # calculate codon usage
    for codon in codon_usage:
        codon_usage[codon] = round(codon_usage[codon] / total, 4)

    return codon_usage

###############################################################################
### Print codon usage table to STDOUT
###############################################################################
def print_codon_usage(codon_usage):

    # print header
    print("Codon\tUsage")

    # sort codon usage alphabetically
    codon_usage = dict(sorted(codon_usage.items()))

    # print codon usage
    for codon in codon_usage:
        # format condon usage as percentage
        codon_usage[codon] = str(round(codon_usage[codon] * 100, 2)) + "%"
        print(codon, codon_usage[codon], sep="\t")

    return True

###############################################################################
### Read FASTA filehandle into dictionary
###############################################################################
def read_fasta(fh):
    header = ""
    fasta = {}

    for line in fh:
        line = line.rstrip()
        # starts with handles blank lines better than line[0]
        if (line.startswith(">")):
            header = line[1:]
            fasta[header] = []
        else:
            fasta[header].append(line)
    # append is more efficient that string concatenation
    for header in fasta:
        fasta[header] = ''.join(fasta[header])

    return fasta

###############################################################################
### RUN MAIN 
###############################################################################
if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()    