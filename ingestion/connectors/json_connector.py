import json
from pathlib import Path

from ingestion.connectors.base_connector import BaseConnector


class JSONConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        file_path = Path(connection.get("file_path", ""))

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[2] / file_path

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as exc:
            self.logger.error("Failed to read JSON for %s: %s", self.source_name, exc)
            return []