import json
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

from ingestion.connectors.base_connector import BaseConnector
from shared.config import DB_CONFIG


class PostgresConnector(BaseConnector):

    def read(self):
        connection_config = DB_CONFIG.copy()
        source_connection = self.config.get("connection", {})

        connection_config.update(
            {
                k: source_connection.get(k, v)
                for k, v in {
                    "host": connection_config.get("host"),
                    "port": connection_config.get("port"),
                    "database": connection_config.get("database"),
                    "user": connection_config.get("user"),
                    "password": connection_config.get("password"),
                }.items()
                if source_connection.get(k) is not None
            }
        )

        table = source_connection.get("table")
        if not table:
            self.logger.error("Missing table name for Postgres source %s", self.source_name)
            return pd.DataFrame()

        try:
            with psycopg2.connect(**connection_config) as connection:
                query = f"SELECT * FROM {table} LIMIT 1000"
                return pd.read_sql_query(query, connection)
        except OperationalError as exc:
            self.logger.warning(
                "Postgres read failed for %s: %s. Falling back to local JSON if available.",
                self.source_name,
                exc,
            )
            return self._load_local_fallback()
        except Exception as exc:
            self.logger.error("Failed to read Postgres for %s: %s", self.source_name, exc)
            return pd.DataFrame()

    def _load_local_fallback(self):
        for candidate in (Path(__file__).resolve().parents[2] / "source_systems" / self.source_name).glob("*.json"):
            try:
                with open(candidate, "r", encoding="utf-8") as file:
                    return pd.DataFrame(json.load(file))
            except Exception:
                continue

        return pd.DataFrame()