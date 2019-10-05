import threading
import os
import zipfile
import json
import time


class ObservationThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.save_game_path = ""
        self.processed_files = dict()
        # self.selected_save_game = input("Folder Name of save game to observe: ")
        self.selected_save_game = "mppamperexpansiondirectiveorganisation_-1362655182"
        self.workspace = "workspace_" + self.selected_save_game + "/"

    def run(self):
        self.load_config_data()
        self.setup_workspace()
        self.load_processed_data()
        self.observe()

    def observe(self):
        print("Starting observation!\n")
        while True:
            files = os.listdir(self.save_game_path + self.selected_save_game + "/")
            rewrite_processed_data = False
            for file in files:
                last_modified = os.path.getmtime(self.save_game_path + self.selected_save_game + "/" + file)
                if file in self.processed_files and last_modified == self.processed_files[file]:
                    # file has been processed before
                    continue
                # file has not been processed
                rewrite_processed_data = True
                self.process(file)
            if rewrite_processed_data:
                self.save_processed_data()
            time.sleep(10)

    def setup_workspace(self):
        if not os.path.exists(self.workspace):
            try:
                os.mkdir(self.workspace)
            except OSError:
                print("Error while creating working directory!")
        if not os.path.exists(self.workspace + "saves/"):
            try:
                os.mkdir(self.workspace + "saves/")
            except OSError:
                print("Error while creating working directory!")

    def process(self, file):
        self.processed_files[file] = os.path.getmtime(self.save_game_path + self.selected_save_game + "/" + file)
        # copy file
        zip_file = zipfile.ZipFile(self.save_game_path + self.selected_save_game + "/" + file)
        zip_file.extract("gamestate")
        os.rename("gamestate", self.workspace + "saves/" + file)

    def load_config_data(self):
        f_in = open("config.txt", "r")
        for line in f_in:
            if line.startswith("save_game_path"):
                self.save_game_path = line.split('"')[1]
                print("save_game_path =", self.save_game_path)

    def load_processed_data(self):
        try:
            f_in = open(self.workspace + "processed_files.json", "r")
            self.processed_files = json.load(f_in)
            f_in.close()
        except FileNotFoundError:
            # No real problem, probably running for the first time
            pass

    def save_processed_data(self):
        f_out = open(self.workspace + "processed_files.json", "w")
        json.dump(self.processed_files, f_out)
        f_out.close()


observation_thread = ObservationThread("ObservationThread")
observation_thread.start()

