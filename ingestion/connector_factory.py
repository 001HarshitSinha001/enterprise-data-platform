from ingestion.connectors.api_connector import APIConnector
from ingestion.connectors.csv_connector import CSVConnector
from ingestion.connectors.excel_connector import ExcelConnector
from ingestion.connectors.json_connector import JSONConnector
from ingestion.connectors.xml_connector import XMLConnector
from ingestion.connectors.postgres_connector import PostgresConnector
from ingestion.connectors.kafka_connector import KafkaConnector
from ingestion.connectors.mongodb_connector import MongoDBConnector

class ConnectorFactory:

    @staticmethod
    def get_connector(source):

        connector_type = source["source_type"].lower()

        connectors = {
            "api": APIConnector,
            "csv": CSVConnector,
            "excel": ExcelConnector,
            "json": JSONConnector,
            "xml": XMLConnector,
            "postgres": PostgresConnector,
            "kafka": KafkaConnector,
            "mongodb": MongoDBConnector
        }

        connector = connectors.get(connector_type)

        if connector is None:
            raise ValueError(
                f"Unsupported connector type: {connector_type}"
            )

        return connector(source)