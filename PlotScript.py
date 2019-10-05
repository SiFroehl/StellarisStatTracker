import numpy as np
import matplotlib.pyplot as plt
import os

def plot_economy(direc):
    files = os.listdir(direc)
    for file in files:
        try:
            if not file.startswith("table"):
                continue
            f_in = open(direc + file, "r")
            data = np.loadtxt(f_in, skiprows=1, unpack=True)
            plt.clf()
            for i in range(1, len(data)):
                plt.plot(data[0], data[i])
            plt.xlabel("Time")
            plt.ylabel(file.split("_")[2].split(".")[0])
            plt.title(file.split("_")[2].split(".")[0] + "-" + file.split("_")[1])
            fname = direc + file.replace("table", "plot").replace(".csv", ".png")
            plt.savefig(fname)
        except:

            print("passed "+file)
            pass


plot_economy("workspace_mppamperexpansiondirectiveorganisation_-1362655182/economy_data/")
