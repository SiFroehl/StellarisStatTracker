import os
import json


def process_empire_data(file_name):
    file = open(file_name, "r")
    root = dict()
    nest = [root]
    depth = 0
    for line in file:
        if line.startswith("country={"):
            depth += 1
            continue
        if depth > 0:
            if "{" in line:
                key = line.split("=")[0].strip()
                nest[-1][key] = dict()
                nest.append(nest[-1][key])
                depth += 1
            if "}" in line:
                depth -= 1
                if depth > 0:
                    nest.pop(len(nest) - 1)
            if "=" in line and "{" not in line:
                key = line.split("=")[0].strip()
                val = line.split("=")[1].strip()
                nest[-1][key] = val

    file.close()
    print(root.keys())
    print(root["0"].keys())

    try:
        os.mkdir(file_name.split("/")[0] + "/empire_data/")
    except OSError:
        # Already made dir
        pass

    f_out = open(file_name.replace("saves", "empire_data").replace("autosave", "empire_data"), "w")
    json.dump(root, f_out, indent=4)
    f_out.close()


def process_all_empire_data(direc):
    files = os.listdir(direc)
    for file in files:
        process_empire_data(direc + file)


def process_all_economy_data(direc):
    files = os.listdir(direc)
    for file in files:
        process_economy_data(direc + file)


def process_economy_data(file_name):
    f_in = open(file_name, "r")
    data = json.load(f_in)
    econ_data = dict()
    for key in data.keys():
        econ_data[key] = {"income": dict(), "expenses": dict(), "balance": dict()}

        if type(data[key]) == dict and "budget" in data[key].keys():
            for key2, value2 in data[key]["budget"]["current_month"]["income"].items():
                for key3, value3 in value2.items():
                    if key3 in econ_data[key]["income"].keys():
                        econ_data[key]["income"][key3] += float(value3)
                    else:
                        econ_data[key]["income"][key3] = float(value3)
            for key2, value2 in data[key]["budget"]["current_month"]["expenses"].items():
                for key3, value3 in value2.items():
                    if key3 in econ_data[key]["expenses"].keys():
                        econ_data[key]["expenses"][key3] += float(value3)
                    else:
                        econ_data[key]["expenses"][key3] = float(value3)
            for key2, value2 in data[key]["budget"]["current_month"]["balance"].items():
                for key3, value3 in value2.items():
                    if key3 in econ_data[key]["balance"].keys():
                        econ_data[key]["balance"][key3] += float(value3)
                    else:
                        econ_data[key]["balance"][key3] = float(value3)


    try:
        os.mkdir(file_name.split("/")[0] + "/economy_data/")
    except OSError:
        # Already made dir
        pass

    f_out = open(file_name.replace("empire_data", "economy_data"), "w")
    json.dump(econ_data, f_out, indent=4)
    f_out.close()


def accumulate_economy_data(direc):
    files = os.listdir(direc)
    tables_income = dict()
    tables_expenses = dict()
    tables_balance = dict()
    for file in files:
        if not file.startswith("economy_data"):
            continue
        acc_helper(direc, file, "income", tables_income)
        acc_helper(direc, file, "expenses", tables_expenses)
        acc_helper(direc, file, "balance", tables_balance)
    acc_table_helper(direc, tables_income, "income")
    acc_table_helper(direc, tables_balance, "balance")
    acc_table_helper(direc, tables_expenses, "expenses")


def acc_table_helper(direc, table, keyword):
    for key, value in table.items():
        list_table = []
        row_id_dict = {"time": 0}
        row_idx = 1
        for time, empire_dict in value.items():
            curr = []
            list_table.append(curr)
            curr.insert(row_id_dict["time"], time)
            for empire, emp_value in empire_dict.items():
                if empire not in row_id_dict:
                    row_id_dict[empire] = row_idx
                    row_idx += 1
                curr.insert(row_id_dict[empire], emp_value)
        f_out = open(direc + "table_" + keyword + "_" + key + ".csv", "w")
        for key2 in row_id_dict.keys():
            f_out.write(key2 + " ")
        f_out.write("\n")
        for sublist in list_table:
            for item in sublist:
                f_out.write(str(item) + " ")
            f_out.write("\n")
        f_out.close()


def acc_helper(direc, file, keyword, table_dict):
    f_in = open(direc + file, "r")
    temp = file.split("_")[2].split(".")
    time = float(temp[0]) + (float(temp[1]) - 1) / 12.0  # ignore the day
    root = json.load(f_in)
    for empire_id, empire_data in root.items():
        for key, value in empire_data[keyword].items():
            if key not in table_dict:
                # dict that connects time to a dict that connects empire ids to the respective value
                table_dict[key] = dict()
            if time not in table_dict[key].keys():
                # dict that connects empire ids to the respective value
                table_dict[key][time] = dict()
            table_dict[key][time][empire_id] = value


process_all_empire_data("workspace_mppamperexpansiondirectiveorganisation_-1362655182/saves/")
process_all_economy_data("workspace_mppamperexpansiondirectiveorganisation_-1362655182/empire_data/")
accumulate_economy_data("workspace_mppamperexpansiondirectiveorganisation_-1362655182/economy_data/")
