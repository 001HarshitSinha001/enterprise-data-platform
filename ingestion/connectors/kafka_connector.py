import json
from pathlib import Path

from ingestion.connectors.base_connector import BaseConnector


class KafkaConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        file_path = connection.get("file_path")

        if file_path:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path(__file__).resolve().parents[2] / path

            if path.exists():
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        return json.load(file)
                except Exception as exc:
                    self.logger.warning("Kafka fallback file read failed for %s: %s", self.source_name, exc)

        self.logger.warning(
            "Kafka connector for %s cannot read live events in this environment. Returning empty message list.",
            self.source_name,
        )
        return []