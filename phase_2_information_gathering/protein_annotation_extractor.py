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
OUTPUT_FILE = "../data/protein_annotation_data.tsv"
df = pd.read_csv(INPUT_FILE, sep="\t")
id_column = df.columns[0]
uniprot_ids = df[id_column].dropna().astype(str).tolist()
results = []

###############################
# Uniprot Information Extractor
###############################

def get_uniprot_info(uniprot_id):
    # Fetching protein information from UniProt REST API
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching {uniprot_id}: {response.status_code}")
        return None

    data = response.json()

    info = {
        "hostUniprotID": data.get("primaryAccession"),
        "function": None,
        "localization": None,
    }

    # Extracting function and localization information
    for comment in data.get("comments", []):
        if comment.get("commentType") == "FUNCTION" and not info["function"]:
            texts = comment.get("texts", [])
            if texts:
                info["function"] = texts[0].get("value")

        if comment.get("commentType") == "SUBCELLULAR LOCATION" and not info["localization"]:
            locs = comment.get("subcellularLocations", [])
            if locs:
                info["localization"] = locs[0].get("location", {}).get("value")

    return info

# Fetching information for each UniProt ID
for i, uid in enumerate(uniprot_ids, 1):
    print(f"[{i}/{len(uniprot_ids)}] Fetching {uid}...")
    info = get_uniprot_info(uid)
    if info:
        results.append(info)
    time.sleep(0.5)  # To avoid overloading UniProt

##########################
# Cleaning and Saving Data
##########################

# Cleaning the results by removing records with missing Function or Localization
print(f"Total records before cleaning: {len(results)}")
results = [r for r in results if r["function"] and r["localization"]]
print(f"Total records after cleaning: {len(results)}")
out_df = pd.DataFrame(results)

# Adding a numerical ID column to the start
out_df.insert(0, "proteinAnnotationID", range(1, len(out_df) + 1))

# Saving results
out_df.to_csv(OUTPUT_FILE, sep="\t", index=False)
print(f"Saved UniProt information to {OUTPUT_FILE}")