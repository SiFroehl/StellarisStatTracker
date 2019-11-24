import os
import logging


# logging.basicConfig(level=logging.INFO)
# logging.info("Initializing DirectoryManager")


SAVE_GAME_PATH = ""
f_in = open("config.txt", "r")
for line in f_in:
    if line.startswith("save_game_path"):
        SAVE_GAME_PATH = line.split('"')[1]
        logging.info("SAVE_GAME_PATH =" + str(SAVE_GAME_PATH))
f_in.close()


successfully_selected_game = False
SELECTED_GAME = ""
while not successfully_selected_game:
    SELECTED_GAME = input("Please select the game you want to observe!")
    if os.path.exists(SAVE_GAME_PATH + SELECTED_GAME + "/"):
        logging.info("Successfully selected save game to observe!")
        successfully_selected_game = True
    else:
        print("The selected game could not be found in the given save game folder!")
        print("Available Saves:")
        for file in os.listdir(SAVE_GAME_PATH):
            print(file)


WORKSPACE_DIRECTORY = "workspace_" + SELECTED_GAME + "/"
JSON_DIRECTORY = WORKSPACE_DIRECTORY + "dicts/"
SAVES_DIRECTORY = WORKSPACE_DIRECTORY + "saves/"
PLOTS_DIRECTORY = WORKSPACE_DIRECTORY + "plots/"

directories = [WORKSPACE_DIRECTORY, JSON_DIRECTORY, SAVES_DIRECTORY, PLOTS_DIRECTORY]

for directory in directories:
    if not os.path.exists(directory):
        try:
            os.mkdir(directory)
        except OSError:
            logging.warn("Error while creating directory %s!" % directory)
