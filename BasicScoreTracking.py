import logging
import matplotlib.pyplot as plt
import os
import EconomyExtractor


AVAILABLE_SUPERFICIAL_KEYS = ["military_power", "economy_power", "victory_rank", "victory_score", "tech_power",
                              "immigration", "emigration", "fleet_size", "empire_size", "empire_cohesion",
                              "new_colonies", "sapient"]

AVAILABLE_STOCKPILE_KEYS = ["energy", "minerals", "food", "influence", "unity", "alloys", "consumer_goods",
                            "volatile_motes", "exotic_gases", "rare_crystals", "sr_living_metal", "sr_zro",
                            "sr_dark_matter", "minor_artifacts"]


def track_superficial_stats(compound_dict, keys, empires):
    ret = dict()  # key -> dict(empire -> dict(time -> value))
    alt_keys = [str(k) for k in empires]
    for key in keys:
        ret[key] = dict()
    for time, single_time_dict in compound_dict.items():
        logging.info("(Superficial)Processing " + str(time))
        for country_id, country in single_time_dict["country"].items():
            if country_id in empires or country_id in alt_keys:
                try:
                    for country_key, ck_value in country.items():
                        if country_key in keys:
                            if country["name"] not in ret[country_key].keys():
                                ret[country_key][country["name"]] = dict()
                            try:
                                ret[country_key][country["name"]][time] = float(ck_value)
                            except:
                                ret[country_key][country["name"]][time] = ck_value
                except:
                    logging.info("Unknown error while processing empire " + str(country["name"]))
    return ret


def track_stockpile_stats(compound_dict, keys, empires):
    ret = dict()  # key -> dict(empire -> dict(time -> value))
    alt_keys = [str(k) for k in empires]
    for key in keys:
        ret[key] = dict()
    for time, single_time_dict in compound_dict.items():
        logging.info("(Stockpile)Processing " + str(time))
        for country_id, country in single_time_dict["country"].items():
            if country_id in empires or country_id in alt_keys:
                try:
                    for resource_key, resource_value in \
                            country["modules"]["standard_economy_module"]["resources"].items():
                        if resource_key in keys:
                            if country["name"] not in ret[resource_key].keys():
                                ret[resource_key][country["name"]] = dict()
                            try:
                                ret[resource_key][country["name"]][time] = float(resource_value)
                            except:
                                ret[resource_key][country["name"]][time] = resource_value
                except:
                    logging.info("Unknown error while processing empire " + str(country["name"]))

    return ret


def track_production_stats(compound_dict, keys, empires):
    ret = dict()  # key -> dict(empire -> dict(time -> value))
    alt_keys = [str(k) for k in empires]
    for key in keys:
        ret["income_" + key] = dict()
        ret["expenses_" + key] = dict()
        ret["balance_" + key] = dict()
    for time, single_time_dict in compound_dict.items():
        logging.info("(Production)Processing " + str(time))
        for country_id, country in single_time_dict["country"].items():
            if country_id in empires or country_id in alt_keys:
                try:
                    production_data = EconomyExtractor.process_empire_data(country)
                    for type_key, type_dict in production_data.items():
                        for value_key, value in type_dict.items():
                            if value_key in keys:
                                resource_key = type_key + "_" + value_key
                                if country["name"] not in ret[resource_key].keys():
                                    ret[resource_key][country["name"]] = dict()
                                try:
                                    ret[resource_key][country["name"]][time] = float(value)
                                except:
                                    ret[resource_key][country["name"]][time] = value
                except:
                    logging.info("Unknown error while processing empire " + str(country["name"]))


    return ret


def plot_superficial_stats(stat_dict):
    if not os.path.exists("plots/"):
        try:
            os.mkdir("plots/")
        except OSError:
            logging.warn("Error while attempting to create plot directory!")
    for key, sub_dict in stat_dict.items():
        logging.info("Plotting " + key)
        plt.clf()
        plt.title(key + " over time")
        plt.xlabel("Time")
        plt.ylabel(key)
        for empire_id, empire in sub_dict.items():
            time_data = []
            value_data = []
            for time, value in empire.items():
                time_data.append(time)
                value_data.append(value)
            plt.plot(time_data, value_data, label="Empire "+empire_id)
        plt.legend()
        plt.savefig("plots/"+key+".png")
