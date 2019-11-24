# StellarisStatTracker
Hopefully usable python scripts to track the progression of a Stellaris game

BasicScoreTracking provides functionality to extract information from aggregated data collected from multiple save games and the ability to plot them.

The CopyScript will take autosaves from the save directory and save the unzipped gamestate in the saves folder in the workspace. These files are human readable but can contain millions of lines. It is intendet to be fairly lightweight and to be run in the background while playing to regularly collect the autosaves and keep them for later injestion while creating a much smaller file to be processed later, as much of the save game information is usually of no intrest.

EconomyExtractor provieds a way to extract the income, balance and expenes information from refined game states (As they are have to be refined out of the game save as they are devided up by the income (etc.) source (base income, jobs, etc...))

ExsampleScript is a small example of how to use the other Files, it contains a usual usecase, extracting and plotting economy and military data for some of the empires (this would usually be the human played empires)

GameDictConverter converts game saves into Python Dicts and is able to output these as .json files
