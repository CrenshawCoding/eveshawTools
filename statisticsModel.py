import csv
import math
from os.path import exists

import tracker


class StatisticsModel:

    def __init__(self):
        self.number_of_runs = 0
        self.average_loot_per_run = 0
        self.update_statistics()

    def update_statistics(self):
        if not exists(tracker.LOOT_PATH):
            raise FileNotFoundError(tracker.LOOT_PATH)
        with open(tracker.LOOT_PATH, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            total = 0
            counter = 0
            for row in reader:
                total += float(row["Value"])
                counter += 1
        self.number_of_runs = counter
        if counter > 0:
            self.average_loot_per_run = math.floor(total / counter)
    