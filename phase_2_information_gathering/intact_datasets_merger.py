#!/usr/bin/env python3

########################
# Importing Dependencies
########################

import os

########################################
# Setting Environment & Global Variables
########################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILES = [
    "../data/EBV_intact_data.tsv",
    "../data/HBV_intact_data.tsv",
    "../data/HCV_intact_data.tsv",
    "../data/HPV_intact_data.tsv",
    "../data/HTLV1_intact_data.tsv",
    "../data/HHV8_intact_data.tsv"  
]
OUTPUT_FILE = "../data/full_intact_data.tsv"

##############
# Merging Data
##############

with open(OUTPUT_FILE, "w") as outfile:
    for i, file in enumerate(INPUT_FILES):
        with open(file, "r") as infile:
            if i != 0:
                next(infile)
            for line in infile:
                outfile.write(line)