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
INPUT_FILE = "../data/host_protein_data.tsv" # Also do for viral proteins
OUTPUT_FILE = "../data/protein_annotation_data.tsv"
df = pd.read_csv(INPUT_FILE, sep="\t")
id_column = df.columns[1]
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
        "ProteinID": data.get("primaryAccession"),
        "Function": None,
        "Localization": None,
    }

    # Extracting function and localization information
    for comment in data.get("comments", []):
        if comment.get("commentType") == "FUNCTION" and not info["Function"]:
            texts = comment.get("texts", [])
            if texts:
                info["Function"] = texts[0].get("value")

        if comment.get("commentType") == "SUBCELLULAR LOCATION" and not info["Localization"]:
            locs = comment.get("subcellularLocations", [])
            if locs:
                info["Localization"] = locs[0].get("location", {}).get("value")

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
results = [r for r in results if r["Function"] and r["Localization"]]
print(f"Total records after cleaning: {len(results)}")

# Adding ID column
for idx, record in enumerate(results, 1):
    record["ID"] = idx
out_df = pd.DataFrame(results)
out_df = out_df[["ID"] + [col for col in out_df.columns if col != "ID"]]

# Saving results
out_df.to_csv(OUTPUT_FILE, sep="\t", index=False)
print(f"Saved UniProt information to {OUTPUT_FILE}")