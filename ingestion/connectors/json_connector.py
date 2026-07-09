from ingestion.connectors.base_connector import BaseConnector


class JSONConnector(BaseConnector):

    def read(self):
        print(f"Reading JSON file: {self.config['name']}")