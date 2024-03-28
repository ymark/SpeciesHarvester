import requests, json

def harvest_resources(current_set):
    next_iter_set=set()
    for id in current_set:
        response_with_results = True
        offset_counter = 0;
        while (response_with_results):
            req_url = worms_api_rel + str(id) + worms_api_suf + str(offset_counter)
            response = requests.get(req_url);

            if response.status_code == 200:
                output = response.json()
                for item in output:
                    if "rank" in item and "status" in item:
                        if item["status"] == "accepted":
                            if item["rank"] == "Species":
                                print(item["AphiaID"])
                                species_ids.add(item["AphiaID"])
                                with open('species_ids.txt', 'a') as species_file:
                                    species_file.write(item["AphiaID"] + "\n")
                            else:
                                next_iter_set.add(item["AphiaID"])
                offset_counter += 50
            else:
                response_with_results = False
    return next_iter_set

worms_api_rel = "https://www.marinespecies.org/rest/AphiaChildrenByAphiaID/"
worms_api_suf = "?marine_only=false&offset="

current_iteration_set = set()
next_iterarion_set = set()
species_ids = set()

current_iteration_set.add(2)  # the seed ID (e.g. 2 is animalia kingdom)

next_iterarion_set=harvest_resources(current_iteration_set)
while len(next_iterarion_set)!=0:
    next_iterarion_set = harvest_resources(next_iterarion_set)

print("Size species: ", len(species_ids))
with open("species_ids.json", "w") as json_file:
    json.dump(list(species_ids), json_file)

