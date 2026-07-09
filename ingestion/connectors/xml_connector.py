
from ingestion.connectors.base_connector import BaseConnector


class XMLConnector(BaseConnector):

   
    def read(self):
        print(f"Reading XML: {self.config['name']}")