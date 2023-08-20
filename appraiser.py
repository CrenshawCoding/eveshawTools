import enum
import json

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
    """This class is used to get marketstats from eve tycoon."""

    # TODO: move enums out of the class

    QUERY_BASE = "https://evetycoon.com/api/v1/market/stats/"

    # loot that has a fixed value (e.g. NPC buy orders) and should not be queried from eve tycoon:
    STATIC_LOOT = {48121: 100000}

    def __init__(self, region: Regions = Regions.THE_FORGE, order_type: OrderType = OrderType.BUY):
        self.query_base = Appraiser.QUERY_BASE + repr(region.value) + '/'
        self.order_type = order_type

    # Returns a dictionary with item ids mapped to their value
    def appraise_items(self, loot) -> dict:
        query_items = ""
        item_values = {}
        for item_ID in loot:
            if item_ID not in Appraiser.STATIC_LOOT:  # Filter static loot out
                json_response = self.appraise_item(item_ID)
                item_values[item_ID] = json_response['maxBuy'] if self.order_type == OrderType.BUY else json_response['minSell']
        return item_values
    
    def appraise_item(self, item_id):
        query = self.query_base + str(item_id)
        response = requests.get(query)
        if response.status_code != 200:
            print("Bad response!\n" + repr(response))
            raise customExceptions.ResponseError
        return json.loads(response.content)

    def generate_appraisal(self, loot_quantity: dict) -> Appraisal:
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
        appraisal = Appraisal(item_drops)
        print('Appraisal value: ' + str(appraisal.total_value))
        if appraisal.total_value > 0:
            return appraisal
        else:
            raise customExceptions.InputInvalid
