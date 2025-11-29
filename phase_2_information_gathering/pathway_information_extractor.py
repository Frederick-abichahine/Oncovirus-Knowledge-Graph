#!/usr/bin/env python3

########################
# Importing Dependencies
########################

import os
import pandas as pd
import requests
import time

########################################
# Setting Environment & Global Variables
########################################

os.chdir(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = "../data/host_protein_data.tsv"
OUTPUT_FILE = "../data/pathway_data.tsv"
df = pd.read_csv(INPUT_FILE, sep="\t")
id_column = df.columns[1]
uniprot_ids = df[id_column].dropna().astype(str).tolist()
records = []

######################################################
# Extracting KEGG Pathway Information from UniProt IDs
######################################################

def get_kegg_gene_from_uniprot(uniprot_id):
    # Converting UniProt ID to KEGG gene ID
    url = f"https://rest.kegg.jp/conv/genes/uniprot:{uniprot_id}"
    r = requests.get(url)
    if r.status_code != 200 or not r.text.strip():
        print(f"No KEGG mapping for {uniprot_id}")
        return None
    lines = r.text.strip().split("\n")
    genes = [line.split("\t")[1] for line in lines if "\t" in line]
    print(f"Found KEGG gene(s): {genes}")
    return genes

def get_pathways_from_kegg_gene(kegg_gene):
    # Getting pathway IDs linked to a KEGG gene
    url = f"https://rest.kegg.jp/link/pathway/{kegg_gene}"
    r = requests.get(url)
    if r.status_code != 200 or not r.text.strip():
        return []
    return [line.split("\t")[1] for line in r.text.strip().split("\n") if "\t" in line]

def get_pathway_details(pathway_id):
    # Fetching pathway details from KEGG
    url = f"https://rest.kegg.jp/get/{pathway_id}"
    r = requests.get(url)
    if r.status_code != 200 or not r.text.strip():
        return None

    data = {
        "pathwayKeggID": pathway_id,
        "pathwayName": None,
        "pathwayCategory": None,
        "pathwayDescription": None,
        "pathwaySource": f"https://www.kegg.jp/pathway/{pathway_id.split(':')[1]}"
    }

    for line in r.text.split("\n"):
        if line.startswith("NAME"):
            data["pathwayName"] = line.replace("NAME", "").strip()
        elif line.startswith("CLASS"):
            data["pathwayCategory"] = line.replace("CLASS", "").strip()
        elif line.startswith("DESCRIPTION"):
            data["pathwayDescription"] = line.replace("DESCRIPTION", "").strip()
    return data

def get_kegg_info_for_uniprot(uniprot_id):
    # Getting all KEGG pathway info for a UniProt ID
    kegg_genes = get_kegg_gene_from_uniprot(uniprot_id)
    if not kegg_genes:
        return []

    all_pathways = []
    for gene in kegg_genes:
        pathway_ids = get_pathways_from_kegg_gene(gene)
        if not pathway_ids:
            print(f"No pathways for {gene}")
        for pid in pathway_ids:
            details = get_pathway_details(pid)
            if details:
                all_pathways.append(details)
            time.sleep(0.2)
        time.sleep(0.2)
    return all_pathways

#######################################################
# Fetching KEGG pathway information for each UniProt ID
#######################################################

for i, uid in enumerate(uniprot_ids, 1):
    clean_uid = uid.strip().split(".")[0]
    print(f"\n[{i}/{len(uniprot_ids)}] Fetching KEGG info for {clean_uid}...")
    pathways = get_kegg_info_for_uniprot(clean_uid)
    if pathways:
        for p in pathways:
            records.append({
                "hostUniprotID": clean_uid,
                "pathwayKeggID": p["pathwayKeggID"],
                "pathwayName": p["pathwayName"],
                "pathwayCategory": p["pathwayCategory"],
                "pathwayDescription": p["pathwayDescription"],
                "pathwaySource": p["pathwaySource"]
            })
    else:
        records.append({
            "hostUniprotID": clean_uid,
            "pathwayKeggID": None,
            "pathwayName": None,
            "pathwayCategory": None,
            "pathwayDescription": None,
            "pathwaySource": None
        })  
    time.sleep(0.5)  # To avoid overloading KEGG
    
##########################
# Cleaning and Saving Data
##########################

out_df = pd.DataFrame(records)
out_df = out_df.dropna()
out_df.to_csv(OUTPUT_FILE, sep="\t", index=False)
print(f"Saved KEGG pathway information to {OUTPUT_FILE}")