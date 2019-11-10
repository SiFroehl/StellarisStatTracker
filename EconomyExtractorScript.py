import os
import json
import GameDictConverter


def process_all_empire_data(game_dict):
    ret = dict()  # Maps Empire ID to "Economy Dict" (income, expenses and balance)
    for empire_id, empire in game_dict["country"].items():
        ret[empire_id] = process_empire_data(game_dict, empire_id)
    return ret


def process_empire_data(game_dict, empire_id):
    if type(empire_id) != str:
        empire_id = str(empire_id)
    month = game_dict["country"][empire_id]["budget"]["current_month"]
    income = tally_econ_data(month["income"])
    expenses = tally_econ_data(month["expenses"])
    balance = tally_econ_data(month["balance"])
    # Returns "Economy Dict"
    return {"income": income, "expenses": expenses, "balance": balance}


def tally_econ_data(sub_dict):
    ret = dict()  # Maps resource type to sum of that type
    for source_name, source in sub_dict.items():
        for key in source:
            if key in ret.keys():
                ret[key] += float(source[key])
            else:
                ret[key] = float(source[key])
    return ret


def track_empire_data_over_time(time_dict, empire_id):
    # Time Dict contains time -> game_dict mappings
    # ret will contain time -> single empire economy data mappings
    ret = dict()
    for time, game_dict in time_dict:
        ret[time] = process_empire_data(game_dict, empire_id)
    return ret


def track_all_empire_data_over_time(time_dict):
    # Time Dict contains time -> game_dict mappings
    # ret will contain empire_id -> dict{time -> single empire economy data} mappings
    ret = dict()
    for time, game_dict in time_dict.items():
        for empire_id in game_dict["country"].keys():
            if empire_id not in ret.keys():
                ret[empire_id] = dict()
            ret[empire_id][time] = process_empire_data(game_dict, empire_id)
    return ret


root = ("C:/Users/Simon/Simon/Python/Git Projects/StellarisStatTracker/workspace" +
        "_mppamperexpansiondirectiveorganisation_-1362655182/dicts/")
time_dict = GameDictConverter.create_save_over_time_dict(root)
print(time_dict)
data = track_all_empire_data_over_time(time_dict)


