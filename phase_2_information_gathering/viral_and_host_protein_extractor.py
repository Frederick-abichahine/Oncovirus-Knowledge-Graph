#!/usr/bin/env python3

########################
# Importing Dependencies
########################

import csv
import os

########################################
# Setting Environment & Global Variables
########################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = "../data/ppi_data.tsv"
OUTPUT_FILE_1 = "../data/viral_protein_data.tsv"
OUTPUT_FILE_2 = "../data/host_protein_data.tsv"
viral_proteins = {}
host_proteins = {}

###############################
# Extracting Data from PPI File
###############################

with open(INPUT_FILE, "r") as infile:
    reader = csv.reader(infile, delimiter="\t")
    next(reader)
    for row in reader:
        virus_code = row[0]
        viral_protein_id = row[1]
        host_protein_id = row[2]
        virus_gene_name = row[3]
        host_gene_name = row[4]
        virus_protein_name = row[5]
        host_protein_name = row[6]

        if viral_protein_id not in viral_proteins:
            viral_proteins[viral_protein_id] = {
                "VirusCode": virus_code,
                "GeneName": virus_gene_name,
                "ProteinName": virus_protein_name
            }

        if host_protein_id not in host_proteins:
            host_proteins[host_protein_id] = {
                "GeneName": host_gene_name,
                "ProteinName": host_protein_name
            }
            
#################################################
# Writing Extracted Data to Separate Output Files
#################################################

with open(OUTPUT_FILE_1, "w", newline="") as outfile1:
    writer = csv.writer(outfile1, delimiter="\t")
    writer.writerow(["VirusCode", "ViralProteinID", "VirusGeneName", "VirusProteinName"])
    for vp_id, details in viral_proteins.items():
        writer.writerow([details["VirusCode"], vp_id, details["GeneName"], details["ProteinName"]])

with open(OUTPUT_FILE_2, "w", newline="") as outfile2:
    writer = csv.writer(outfile2, delimiter="\t")
    writer.writerow(["HostProteinID", "HostGeneName", "HostProteinName"])
    for hp_id, details in host_proteins.items():
        writer.writerow([hp_id, details["GeneName"], details["ProteinName"]])