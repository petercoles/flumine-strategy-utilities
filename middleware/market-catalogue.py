import os
import json
import smart_open
from betfairlightweight.resources import MarketCatalogue
from flumine.markets.middleware import Middleware

class MarketCatalogueMiddleware(Middleware):
    '''
    Will read and parse the market_catalogue file and add to the market object when simulating
    '''
    def __init__(self, catalogue_path, file_extension):
        self.catalogue_path = catalogue_path
        self.file_extension = file_extension

    def add_market(self, market) -> None:
        catalogue_file_path = f"{self.catalogue_path}/{market.market_id}.{self.file_extension}"
        if os.path.exists(catalogue_file_path):
            with smart_open.open(catalogue_file_path, "r") as r:
                data = r.read()
                catalogue_json_data = json.loads(data)
                market.market_catalogue = MarketCatalogue(**catalogue_json_data)
