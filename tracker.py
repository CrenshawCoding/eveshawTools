import csv
from datetime import datetime, timedelta
from os.path import exists

import appraiser

LOOT_PATH = "./db/runs.csv"


def save_run(appraisal: appraiser.Appraisal):
    runs_fieldnames = ["ID", "Date", "Value"]
    current_id = 0
    new_file = False
    if not exists(LOOT_PATH):
        f = open(LOOT_PATH, "w+")
        new_file = True
        f.close()
    with open(LOOT_PATH, 'r+', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        writer = csv.DictWriter(csvfile, fieldnames=runs_fieldnames)
        if new_file:
            writer.writeheader()
        for row in reader:
            current_id = int(row["ID"])
        current_id += 1
        # with open(LOOT_PATH, "a", newline='') as csvfile:
        writer.writerow({"ID": current_id, "Date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                         "Value": appraisal.total_value})
