import pandas as pd
from pathlib import Path

from ingestion.connectors.base_connector import BaseConnector


class CSVConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        file_path = Path(connection.get("file_path", ""))

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[2] / file_path

        try:
            return pd.read_csv(
                file_path,
                sep=connection.get("delimiter", ","),
                encoding=connection.get("encoding", "utf-8"),
            )
        except Exception as exc:
            self.logger.error("Failed to read CSV for %s: %s", self.source_name, exc)
            return pd.DataFrame()