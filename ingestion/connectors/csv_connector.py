from ingestion.connectors.base_connector import BaseConnector


class CSVConnector(BaseConnector):

    def read(self):
        print(f"Reading CSV: {self.config['name']}")