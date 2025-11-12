#!/usr/bin/env python3

########################
# Importing Dependencies
########################

import csv
import os
import re

########################################
# Setting Environment & Global Variables
########################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = "../data/full_intact_data.tsv"
OUTPUT_FILE = "../data/ppi_data.tsv"
HUMAN_TAXID = "9606"
counter_na = 0
counter_dup = 0

###########################
# Defining Helper Functions
###########################

def extract_gene_and_protein(alias_field):
    """
    Extract gene and protein names from the Alias(es) field.
    Looks for 'uniprotkb:GENE_NAME(gene name)' and 'display_long' protein names.
    """
    parts = alias_field.split("|")
    gene_name = ""
    protein_name = ""

    # Extracting gene name
    for part in parts:
        match = re.search(r"uniprotkb:([A-Za-z0-9\-]+)\(gene name\)", part)
        if match:
            gene_name = match.group(1)
            break

    # Extracting protein name
    for part in parts:
        if "display_long" in part:
            match = re.search(r":(.+?)\(display_long\)", part)
            if match:
                protein_name = match.group(1).strip()
                break

    return gene_name, protein_name


def is_valid_record(values):
    """Return True if none of the values are empty or NA."""
    for v in values:
        if not v or v.strip() == "" or v.strip().upper() == "NA":
            global counter_na
            counter_na += 1
            return False
    return True

#######################
# Main Processing Logic
#######################

with open(INPUT_FILE, "r", encoding="utf-8") as infile, open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(infile, delimiter="\t")
    writer = csv.writer(outfile, delimiter="\t")

    # Creating file header
    writer.writerow([
        "VirusCode",
        "ViralProteinID",
        "HostProteinID",
        "VirusGeneName",
        "HostGeneName",
        "VirusProteinName",
        "HostProteinName"
    ])

    seen = set()

    for row in reader:
        taxid_a = row["Taxid interactor A"]
        taxid_b = row["Taxid interactor B"]

        id_a = row["# ID(s) interactor A"].split(":")[1] if ":" in row["# ID(s) interactor A"] else row["# ID(s) interactor A"]
        id_b = row["ID(s) interactor B"].split(":")[1] if ":" in row["ID(s) interactor B"] else row["ID(s) interactor B"]

        alias_a = row["Alias(es) interactor A"]
        alias_b = row["Alias(es) interactor B"]

        # Identifying virus vs host
        if HUMAN_TAXID in taxid_a and HUMAN_TAXID not in taxid_b:
            virus_id, host_id = id_b, id_a
            virus_alias, host_alias = alias_b, alias_a
            virus_taxid = taxid_b
        elif HUMAN_TAXID in taxid_b and HUMAN_TAXID not in taxid_a:
            virus_id, host_id = id_a, id_b
            virus_alias, host_alias = alias_a, alias_b
            virus_taxid = taxid_a
        else:
            # In order to skip invalid rows
            continue

        # Extracting gene/protein names
        virus_gene, virus_protein = extract_gene_and_protein(virus_alias)
        host_gene, host_protein = extract_gene_and_protein(host_alias)

        # Getting virus code
        virus_code_match = re.search(r"\((.*?)\)", virus_taxid)
        virus_code = virus_code_match.group(1).upper() if virus_code_match else "UNKNOWN"

        # Preparing record
        record = [
            virus_code,
            virus_id,
            host_id,
            virus_gene,
            host_gene,
            virus_protein,
            host_protein
        ]

        # Skipping records with missing data
        if not is_valid_record(record):
            continue

        # Skipping duplicate records (based on VirusCode, VirusProteinID and HostProteinID)
        key = (virus_code, virus_id, host_id)
        if key in seen:
            counter_dup += 1
            continue
        seen.add(key)

        writer.writerow(record)

# Displaying some information
print(f"Cleaned and deduplicated virus-host interactions written to '{OUTPUT_FILE}'")
print(f"Skipped {counter_na} records due to missing or NA values.")
print(f"Skipped {counter_dup} duplicate records.")