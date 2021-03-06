import GameDictConverter
import logging
import BasicScoreTracking
import DirectoryManager
import MapDataExtractor

# GameDictConverter.convert_all_saves()
sot_dict = GameDictConverter.create_save_over_time_dict(DirectoryManager.SELECTED_GAME)
MapDataExtractor.plot_map(sot_dict[[key for key in sot_dict.keys()][0]])
empires = range(0, 3)
stats = BasicScoreTracking.track_superficial_stats(sot_dict, BasicScoreTracking.AVAILABLE_SUPERFICIAL_KEYS, empires)
stockpile_stats = \
    BasicScoreTracking.track_stockpile_stats(sot_dict, BasicScoreTracking.AVAILABLE_STOCKPILE_KEYS, empires)
production_stats = BasicScoreTracking.track_production_stats(sot_dict, BasicScoreTracking.AVAILABLE_STOCKPILE_KEYS +
                                                             ["physics_research", "society_research",
                                                              "engineering_research"], empires)
# BasicScoreTracking.plot_superficial_stats(stats)
# BasicScoreTracking.plot_superficial_stats(stockpile_stats)
# BasicScoreTracking.plot_superficial_stats(production_stats)
