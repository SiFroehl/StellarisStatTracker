import os
import json
import logging

USUALLY_SKIPPED_KEYS = ['species', 'half_species', 'last_created_species', 'nebula', 'pop', 'last_created_pop',
                        'galactic_object', 'starbases', 'planets', 'alliance', 'truce', 'trade_deal',
                        'last_created_country', 'last_refugee_country', 'last_created_system', 'leaders',
                        'saved_leaders', 'ships', 'fleet', 'fleet_template', 'last_created_fleet',
                        'last_created_ship', 'last_created_leader', 'last_created_army',
                        'last_created_design', 'army', 'deposit', 'ground_combat', 'fired_events',
                        'war', 'debris', 'missile', 'strike_craft', 'ambient_object',
                        'last_created_ambient_object', 'message', 'last_diplo_action_id',
                        'last_notification_id', 'last_event_id', 'random_name_database', 'name_list',
                        'galaxy', 'galaxy_radius', 'flags', 'saved_event_target', 'ship_design',
                        'pop_factions', 'last_created_pop_faction', 'last_killed_country_name',
                        'megastructures', 'bypasses', 'natural_wormholes', 'trade_routes', 'sectors',
                        'buildings', 'archaeological_sites', 'global_ship_design', 'clusters',
                        'rim_galactic_objects', 'used_color', 'used_symbols', 'used_species_names',
                        'used_species_portrait', 'random_seed', 'random_count',
                        'trade_routes_manager', 'slave_market_manager']


def create_dict_from_file(file_name, skipped_top_level_keys=[]):
    logging.info("create_dict_from_file")
    file = open(file_name, "r")
    root = dict()
    nest = [root]
    for line in file:
        try:
            if "{" in line:
                key = line.split("=")[0].strip()
                nd = dict()
                nest[-1][key] = nd
                nest.append(nd)
            if "}" in line:
                nest.pop(-1)
            if "=" in line and "{" not in line:
                key = line.split("=")[0].strip()
                val = line.split("=")[1].strip()
                nest[-1][key] = val
        except:
            print(nest)
            print(line)
    file.close()
    for skipped_key in skipped_top_level_keys:
        if skipped_key in root.keys():
            root[skipped_key] = "Skipped"
    return root


def create_json_from_file(file, out_file, skipped_top_level_keys=[]):
    logging.info("create_json_from_file")
    root = create_dict_from_file(file, skipped_top_level_keys)
    dir_name = "/".join(out_file.split("/")[:-1]) + "/"
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    f_out = open(out_file, "w")
    json.dump(root, f_out, indent=2)
    f_out.close()


def convert_all_saves(src, out, skipped_top_level_keys = USUALLY_SKIPPED_KEYS):
    logging.info("convert_all_saves")
    files = os.listdir(src)
    if not os.path.exists(out):
        os.mkdir(out)
    for file in files:
        out_file = file.replace(src, out).replace(".sav", ".json")
        create_json_from_file(src + file, out + out_file, skipped_top_level_keys)


def create_save_over_time_dict(save_name):
    json_folder = "workspace_" + save_name + "/dicts/"
    logging.info("create_save_over_time_dict")
    ret = dict()
    files = [f for f in os.listdir(json_folder) if f.endswith(".json")]
    for i, file in enumerate(files):
        logging.info("Processing files: %i/%i (%.1f)" % (i, len(files), float(i)/len(files)*100))
        date = file.split("_")[1].replace(".json", "").split(".")
        time = float(date[0]) + (float(date[1])-1) / 12 + (float(date[2])-1) / 360
        fin = open(json_folder + file)
        ret[time] = json.load(fin)
        fin.close()
    logging.info("Processed all files!")
    return ret


def compound_data_over_time(game_save_name, file_out="compound_dict.json"):
    logging.info("compound_data_over_time")
    data = create_save_over_time_dict("workspace_"+game_save_name+"/dicts/")
    f_out = open("workspace_"+game_save_name+"/"+file_out, "w")
    logging.info("Dumping into file, may take quite some time...")
    json.dump(data, f_out, indent=2)
    logging.info("Done writing to file!")
    f_out.close()




