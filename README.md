# StellarisStatTracker
Hopefully usable python scripts to track the progression of a Stellaris game

The CopyScript will take autosaves from the save directory and save the unzipped gamestate in the saves folder in the workspace. These files are human readable but can contain millions of lines. It is intendet to be fairly lightweight and to be run in the background while playing to regularly collect the autosaves and keep them for later injestion using the ProcessorScript

The ProcessorScript will take the files output from CopyScript and extract the useful information (for now just economy) into smaller, more manageable files

The PlotScript will take the files output from ProcessorScript and create plots using the accumulated information (the data tables)
