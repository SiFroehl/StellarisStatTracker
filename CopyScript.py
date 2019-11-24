import threading
import os
import zipfile
import json
import time
import GameDictConverter
import DirectoryManager
import logging


class ObservationThread (threading.Thread):
    def __init__(self, name, auto_process_files=True):
        threading.Thread.__init__(self)
        self.main_loop_flag = True
        self.num_processed = 0
        self.name = name
        self.auto_process = auto_process_files
        self.processed_files = dict()

    def run(self):
        self.observe()

    def setup(self):
        self.load_processed_data()

    def observe(self):
        print("Starting observation!\n")
        while self.main_loop_flag:
            files = os.listdir(DirectoryManager.SAVE_GAME_PATH + DirectoryManager.SELECTED_GAME + "/")
            rewrite_processed_data = False
            for file in files:
                last_modified = os.path.getmtime(
                    DirectoryManager.SAVE_GAME_PATH + DirectoryManager.SELECTED_GAME + "/" + file)
                if file in self.processed_files and last_modified == self.processed_files[file]:
                    # file has been processed before
                    continue
                # file has not been processed
                rewrite_processed_data = True
                self.process(file)
            if rewrite_processed_data:
                self.save_processed_data()
            time.sleep(10)

    def process(self, file):
        self.num_processed += 1
        self.processed_files[file] = os.path.getmtime(
            DirectoryManager.SAVE_GAME_PATH + DirectoryManager.SELECTED_GAME + "/" + file)
        # copy file
        zip_file = zipfile.ZipFile(DirectoryManager.SAVE_GAME_PATH + DirectoryManager.SELECTED_GAME + "/" + file)
        zip_file.extract("gamestate")
        if os.path.isfile(DirectoryManager.SAVES_DIRECTORY + file):
            os.remove(DirectoryManager.SAVES_DIRECTORY + file)
        os.rename("gamestate", DirectoryManager.SAVES_DIRECTORY + file)

        if self.auto_process:
            GameDictConverter.create_json_from_file(
                DirectoryManager.SAVES_DIRECTORY + file,
                DirectoryManager.JSON_DIRECTORY + file.replace(".sav", ".json"),
                GameDictConverter.USUALLY_SKIPPED_KEYS)

    def load_processed_data(self):
        try:
            f_in = open(DirectoryManager.WORKSPACE_DIRECTORY + "processed_files.json", "r")
            self.processed_files = json.load(f_in)
            f_in.close()
        except FileNotFoundError:
            # No real problem, probably running for the first time
            logging.warn("Unable to find list of allready processed files!"
                         " This is unexpected if this is not the first run")

    def save_processed_data(self):
        f_out = open(DirectoryManager.WORKSPACE_DIRECTORY + "processed_files.json", "w")
        json.dump(self.processed_files, f_out)
        f_out.close()


auto_process_inp = input("Auto process save files?[y/n]")
auto_process = False
if auto_process_inp.lower() == "y" or auto_process_inp.lower() == "yes":
    auto_process = True

observation_thread = ObservationThread("ObservationThread", auto_process)
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
