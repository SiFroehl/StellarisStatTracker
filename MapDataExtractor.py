from matplotlib import pyplot as plt
import DirectoryManager

def plot_map(single_game_dict):
    systems = single_game_dict["galactic_object"]
    map = dict()
    plt.clf()
    plt.rcParams['axes.facecolor'] = 'dimgray'
    star_classes = []
    for system_id, system in systems.items():
        x1, y1 = (float(system["coordinate"]["x"]), float(system["coordinate"]["y"]))
        reduced_type = "default"
        if "binary" in system["star_class"]:
            reduced_type = "binary"
        if "trinary" in system["star_class"]:
            reduced_type = "trinary"
        if "black_hole" in system["star_class"]:
            reduced_type = "black_hole"
        if "neutron_star" in system["star_class"]:
            reduced_type = "neutron_star"
        if "pulsar" in system["star_class"]:
            reduced_type = "pulsar"
        map[system_id] = (x1, y1, reduced_type)
        if "hyperlane" in system.keys():
            for connection_key, connection in system["hyperlane"].items():
                if connection["to"] in map.keys():
                    x2, y2, _ = map[connection["to"]]
                    plt.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=.5)
    # x_points = [tup[0] for sid, tup in map.items()]
    # y_points = [tup[1] for sid, tup in map.items()]
    # print(x_points)
    # print(y_points)
    # plt.plot(x_points, y_points, marker='.', linestyle=" ", color="r")
    markers = {"default": ".", "binary": "$..$", "trinary": "$.'.$", "black_hole": "o", "neutron_star": "$\emptyset$",
               "pulsar": "$\emptyset$"}
    marker_size = {"default": 2, "binary": 5, "trinary": 5, "black_hole": 2, "neutron_star": 3,
               "pulsar": 3}
    colors = {"default": "gold", "binary": "gold", "trinary": "gold", "black_hole": "k", "neutron_star": "azure",
              "pulsar": "lightcyan"}

    for id, tup in map.items():
        plt.plot(tup[0], tup[1], marker=markers[tup[2]], color=colors[tup[2]], markersize=marker_size[tup[2]])
    plt.savefig(DirectoryManager.PLOTS_DIRECTORY + "map.png", dpi=500)
    print(star_classes)
