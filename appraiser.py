import enum
import xml.etree.ElementTree as elementTree

import requests

import customExceptions
import databaseController


class ItemDrop:
    def __init__(self, item_name: str, item_quantity: int, item_value: float):
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.item_value = item_value
        self.total_value = item_quantity * item_value


class Appraisal:
    def __init__(self, loot: list):
        self.item_drops = list
        self.total_value = 0
        for item_drop in loot:
            self.total_value += item_drop.total_value


class Regions(enum.Enum):
    THE_FORGE = 10000002
    DOMAIN = 10000043


class OrderType(enum.Enum):
    BUY = "buy"
    SELL = "sell"


class Appraiser:
    """This class is used to get marketstats from evemarketer."""

    # TODO: move enums out of the class

    QUERY_BASE = "https://api.evemarketer.com/ec/marketstat?regionlimit="

    # loot that has a fixed value (e.g. NPC buy orders) and should not be queried from evemarketer:
    STATIC_LOOT = {48121: 100000}

    def __init__(self, region: Regions = Regions.THE_FORGE, order_type: OrderType = OrderType.BUY):
        self.query_base = Appraiser.QUERY_BASE + repr(region.value)
        self.order_type = order_type

    # Returns a dictionary with item ids mapped to their value
    def appraise_items(self, loot):
        query_items = ""
        for item_ID in loot:
            if item_ID not in Appraiser.STATIC_LOOT:  # Filter static loot out
                query_items += "&typeid=" + item_ID
        query = self.query_base + query_items
        response = requests.get(query)
        if response.status_code != 200:
            print("Bad response!\n" + repr(response))
            raise customExceptions.ResponseError
        root = elementTree.fromstring(response.content)
        item_values = {}
        for child in root[0]:
            item_id = child.attrib["id"]
            if self.order_type == OrderType.BUY:
                item_values[item_id] = float(child.find('buy').find('max').text)
            elif self.order_type == OrderType.SELL:
                item_values[item_id] = float(child.find('sell').find('min').text)
        return item_values

    def generate_appraisal(self, loot_quantity: dict):
        database_controller = databaseController.DatabaseController()
        item_drops = []
        loot_value = self.appraise_items(loot_quantity)
        for item_id in loot_quantity:
            try:
                name = database_controller.get_item_name(item_id)
                quantity = loot_quantity[item_id]
                value = Appraiser.STATIC_LOOT[item_id] if item_id in Appraiser.STATIC_LOOT else loot_value[item_id]
                item_drops.append(ItemDrop(item_name=name, item_quantity=quantity, item_value=value))
            except ValueError:
                print("Was not able to find item id " + repr(item_id) + " continuing.")
                continue
        return Appraisal(item_drops)
