from ingestion.connectors.base_connector import BaseConnector


class MongoDBConnector(BaseConnector):

    def read(self):
        print(f"Reading from MongoDB: {self.config['name']}")