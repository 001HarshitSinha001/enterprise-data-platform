import pandas as pd
from pathlib import Path

from ingestion.connectors.base_connector import BaseConnector


class ExcelConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        file_path = Path(connection.get("file_path", ""))

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[2] / file_path

        try:
            return pd.read_excel(
                file_path,
                sheet_name=connection.get("sheet_name", 0),
                engine="openpyxl",
            )
        except Exception as exc:
            self.logger.error("Failed to read Excel file for %s: %s", self.source_name, exc)
            return pd.DataFrame()