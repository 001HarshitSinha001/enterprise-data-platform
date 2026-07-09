from ingestion.connectors.base_connector import BaseConnector


class PostgresConnector(BaseConnector):

    def read(self):
        print(f"Reading from Postgres: {self.config['name']}")