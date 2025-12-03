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
viral_interactions = []
host_proteins = {}

###############################
# Extracting Data from PPI File
###############################

with open(INPUT_FILE, "r") as infile:
    reader = csv.reader(infile, delimiter="\t")
    next(reader)
    for row in reader:
        id = row[0]
        virus_code = row[1]
        viral_protein_id = row[2]
        host_protein_id = row[3]
        virus_gene_name = row[4]
        host_gene_name = row[5]
        virus_protein_name = row[6]
        host_protein_name = row[7]
        interaction_id = f"{viral_protein_id}/{host_protein_id}"

        viral_interactions.append({
            "interactionID": interaction_id,
            "virusCode": virus_code,
            "viralUniprotID": viral_protein_id,
            "hostUniprotID": host_protein_id,
            "viralGeneName": virus_gene_name,
            "viralProteinName": virus_protein_name
        })

        if host_protein_id not in host_proteins:
            host_proteins[host_protein_id] = {
                "hostGeneName": host_gene_name,
                "hostProteinName": host_protein_name
            }
            
#################################################
# Writing Extracted Data to Separate Output Files
#################################################

with open(OUTPUT_FILE_1, "w", newline="") as outfile1:
    writer = csv.writer(outfile1, delimiter="\t")
    writer.writerow([
        "interactionID",
        "virusCode",
        "viralUniprotID",
        "hostUniprotID",
        "viralGeneName",
        "viralProteinName"
    ])
    for record in viral_interactions:
        writer.writerow([
            record["interactionID"],
            record["virusCode"],
            record["viralUniprotID"],
            record["hostUniprotID"],
            record["viralGeneName"],
            record["viralProteinName"]
        ])

with open(OUTPUT_FILE_2, "w", newline="") as outfile2:
    writer = csv.writer(outfile2, delimiter="\t")
    writer.writerow(["hostUniprotID", "hostGeneName", "hostProteinName"])
    for hp_id, details in host_proteins.items():
        writer.writerow([hp_id, details["hostGeneName"], details["hostProteinName"]])