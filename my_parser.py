import databaseController


# Returns a dictionary of the looted item id and its quantity
# loot_input_raw - raw input read from user input
def parse_loot(loot_input_raw):
    loot = {}
    for line in loot_input_raw.split('\n'):
        if len(line.split('\t')) < 2 or len(line.split('\t')[0]) < 1 or len(
                line.split('\t')[1]) < 1:  # invalid line, continue
            continue
        item_name = line.split('\t')[0]
        item_quantity = int(line.split('\t')[1])
        database_controller = databaseController.DatabaseController()
        try:
            item_id = database_controller.get_item_id(item_name)
        except ValueError:
            print(item_name + " does not exist in database. Skipping")
            continue

        if item_id in loot:
            loot[database_controller.get_item_id(item_name)] += item_quantity
        else:
            loot[database_controller.get_item_id(item_name)] = item_quantity
    return loot
