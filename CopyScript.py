import threading
import os
import zipfile
import json
import time




class ObservationThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.main_loop_flag = True
        self.num_processed = 0
        self.name = name
        self.save_game_path = ""
        self.processed_files = dict()
        self.selected_save_game = input("Folder Name of save game to observe: ")
        # self.selected_save_game = "mppamperexpansiondirectiveorganisation_-1362655182"
        self.workspace = "workspace_" + self.selected_save_game + "/"

    def run(self):
        self.observe()

    def setup(self):
        self.load_config_data()
        self.setup_workspace()
        self.load_processed_data()

    def observe(self):
        while not os.path.exists(self.save_game_path + self.selected_save_game + "/"):
            print("'%s' is not a valid directory!"%self.save_game_path + self.selected_save_game + "/")
            self.selected_save_game = input("Folder Name of save game to observe: ")
        print("Starting observation!\n")
        while self.main_loop_flag:
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
        self.num_processed += 1
        self.processed_files[file] = os.path.getmtime(self.save_game_path + self.selected_save_game + "/" + file)
        # copy file
        zip_file = zipfile.ZipFile(self.save_game_path + self.selected_save_game + "/" + file)
        zip_file.extract("gamestate")
        if os.path.isfile(self.workspace + "saves/" + file):
            os.remove(self.workspace + "saves/" + file)
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
observation_thread.setup()
observation_thread.start()
while observation_thread.main_loop_flag:
    s = input("")
    s_1 = input("End observation?[y/n]")
    if s_1.lower() == "y" or s_1.lower() == "yes":
        observation_thread.main_loop_flag = False
    else:
        continue
print("Processed %i files (%i total)" %
      (observation_thread.num_processed, len(observation_thread.processed_files)))
print("Console will close on it's own")
