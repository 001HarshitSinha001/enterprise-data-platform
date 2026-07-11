import psycopg2

from ingestion.connectors.base_connector import BaseConnector


class PostgresConnector(BaseConnector):

    def read(self, query="SELECT * FROM orders LIMIT 10"):

        connection = psycopg2.connect(**self.config)

        cursor = connection.cursor()

        cursor.execute(query)

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data