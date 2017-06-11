from collections import namedtuple
from os import listdir
from os.path import isfile, join
from watchdog.observers import Observer

import config
from parser_xml import parse_standing_from_file
from models.standings import TotalStandings
from fs_event_handler import FSEventHandler

StandingPath = namedtuple("StandingPath", "fname standing")

def parse_file(file_name):
    return parse_standing_from_file(config.XML_DIR + file_name)

def get_files(mypath):
    """Get list of files in samples directory"""
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

class DataRepository:

    def __init__(self):
        self.__set_data()
        self.__init_watchers()

    def __set_data(self):
        self.standings, self.total_standing = self.read_data_from_files()

    def read_data_from_files(self):

        files = filter(lambda fname: fname.endswith(".xml"), get_files(config.XML_DIR))
        standings = list(map(lambda fname: StandingPath(fname, parse_file(fname)), files))
        total_standing = TotalStandings(list(map(lambda s: s.standing, standings)))
        return standings, total_standing

    def get_contests_files(self):
        """returns list of { name: 'Contest 1', path: 'contest1.xml' }"""
        files = map(lambda t: {"path": t.fname, "name": t.standing.contest.name}, self.standings)
        return sorted(files, key=lambda t: t["name"])

    def get_total_standings(self):
        return self.total_standing

    def get_all_standings(self):
        return list(map(lambda t: t.standing, self.standings))

    def get_contest_standing(self, file_name):
        return next(t.standing for t in self.standings if t.fname == file_name)

    def __init_watchers(self):
        event_handler = FSEventHandler(self.__set_data)
        self.observer = Observer()
        self.observer.schedule(event_handler, config.XML_DIR)
        self.observer.start()