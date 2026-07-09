from ingestion.connectors.base_connector import BaseConnector


class APIConnector(BaseConnector):

    def read(self):
        print(f"Reading data from API: {self.config['name']}")