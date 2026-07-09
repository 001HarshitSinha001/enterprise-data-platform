from ingestion.connector_factory import ConnectorFactory


config = {
    "name": "customer_CSV",
    "type": "csv"
}

connector = ConnectorFactory.get_connector(config)

print(type(connector).__name__)

connector.read()