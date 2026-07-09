from ingestion.connectors.base_connector import BaseConnector


class ExcelConnector(BaseConnector):

    def read(self):
        print(f"Reading Excel file: {self.config['name']}")