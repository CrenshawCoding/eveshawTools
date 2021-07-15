from html.parser import HTMLParser

import requests


class MineralParser(HTMLParser):
    Minerals = ["Tritanium", "Pyerite", "Mexallon", "Isogen", "Nocxium", "Zydrine"]

    def handle_data(self, data):
        if str(data) in MineralParser.Minerals:
            print(self.getpos())


class WebScraper:
    everef_base_url = "https://everef.net/type/"

    def get_reprocessed_items(self, item_id):
        response_content = requests.get(WebScraper.everef_base_url + str(item_id)).content
