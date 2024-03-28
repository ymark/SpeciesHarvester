# Collect information from WoRMS regarding:
# (a) taxonomic information,
# (b) common names in english
# (c) external identifiers
# using the WoRMS REST API

import requests, json

worms_record_api="https://www.marinespecies.org/rest/AphiaRecordByAphiaID/"
worms_cname_api="https://www.marinespecies.org/rest/AphiaVernacularsByAphiaID/"
worms_ext_ids_api="https://www.marinespecies.org/rest/AphiaExternalIDByAphiaID/"
species_ids="datasets/species_accepted_aphia_ids.txt"
worms_species={}

def identify_marine_species_and_taxonomy():
  with open(species_ids,'r') as ids_file:
    for line in ids_file:
      aphia_id=line.strip()
      req_url=worms_record_api+aphia_id
      print("Hitting URL: "+req_url)
      response=requests.get(req_url)
      if response.status_code==200:
        output=response.json()
        if "isMarine" in output and output["isMarine"]==1:
          worms_species[aphia_id]={}
          worms_species[aphia_id]["genus"]=output["genus"]
          worms_species[aphia_id]["family"]=output["family"]
          worms_species[aphia_id]["order"]=output["order"]
          worms_species[aphia_id]["class"]=output["class"]
          worms_species[aphia_id]["phylum"]=output["phylum"]
          worms_species[aphia_id]["kingdom"]=output["kingdom"]
  with open("worms_species_common_names.json","w") as json_output:
    json.dump(worms_species,json_output)

def identify_common_names_eng():
  for aphia_id in worms_species.keys():
    req_url=worms_cname_api+aphia_id
    print("Hitting URL: "+req_url)
    response=requests.get(req_url)
    if response.status_code==200:
      output=response.json()
      for item in output:
        if item["language"]=="English":
          worms_species[aphia_id]["common_names_eng"]=[]
          worms_species[aphia_id]["common_names_eng"].append(item["vernacular"])
  with open("worms_species_common_names.json","w") as json_output:
    json.dump(worms_species,json_output)

def identify_external_ids():
  for aphia_id in worms_species.keys():
    for ext_id_source in ["algaebase","bold","dyntaxa","fishbase","iucn","lsid","ncbi","tsn","gisd"]:
      req_url=worms_ext_ids_api+aphia_id+"?type="+ext_id_source
      print("Hitting URL: "+req_url)
      response=requests.get(req_url)
      if response.status_code==200:
        output=response.json()
        worms_species[aphia_id]["external_ids"]=[]
        for item in output:
          external_id_pair={}
          external_id_pair["source"]=ext_id_source
          external_id_pair["id"]=item
          worms_species[aphia_id]["external_ids"].append(external_id_pair)
  with open("worms_species_common_names.json","w") as json_output:
    json.dump(worms_species,json_output)

# find marine species and retrieve their taxonomy
identify_marine_species_and_taxonomy()
identify_common_names_eng()
identify_external_ids()