from ingestion.connectors.postgres_connector import PostgresConnector
from shared.config import DB_CONFIG

connector = PostgresConnector(DB_CONFIG)

data = connector.read()

for row in data:
    print(row)