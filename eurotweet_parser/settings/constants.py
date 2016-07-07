#! coding:utf-8
'''
Parses settings file
'''

import os
import ConfigParser
import __root__

CONFIG_DIR = "settings/conf/"
SETTINGS_FILENAME = "settings_.conf"

date_intervals={
    "week1": ['2016-06-10', '2016-06-14'],
    "week2": ['2016-06-15', '2016-06-18'],
    "week3": ['2016-06-19', '2016-06-22'],
    "week4": ['2016-06-23', '2016-06-27'],
    "week5": ['2016-06-28', '2016-07-04'],
    "pol-pt": ['2016-06-30', '2016-07-01'],
    "wa-bel": ['2016-06-30', '2016-07-01'],
    "ger-it": ['2016-07-02', '2016-07-03'],
    "fra-ice": ['2016-07-03', '2016-07-04'],
}

tag_selections = {
    "pol-pt": ["#POLPOR", "#POL", "POR"],
    "wa-bel": ["#WALBE", "#WAL", "#BE"],
    "ger-it": ["#GERIT", "#GER", "#IT"],
    "fra-ice": ["#FRAICE", "#FRA", "#ICE"]
}


class SettingsGenerator:
    def get_settings(self):
        config = ConfigParser.RawConfigParser()
        # Checks if the settings settings file already exists
        path = os.path.join(__root__.path(), CONFIG_DIR + SETTINGS_FILENAME)
        if os.path.isfile(path):
            config.read(CONFIG_DIR + SETTINGS_FILENAME)
            return config
        raise Exception("Conf file not found in path: %s"% path)