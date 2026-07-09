from ingestion.connectors.base_connector import BaseConnector


class KafkaConnector(BaseConnector):

    def read(self):
        print(f"Reading from Kafka: {self.config['name']}")