import xml.etree.ElementTree as ET
from pathlib import Path

from ingestion.connectors.base_connector import BaseConnector


class XMLConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        file_path = Path(connection.get("file_path", ""))

        if not file_path.is_absolute():
            file_path = Path(__file__).resolve().parents[2] / file_path

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            rows = []

            for element in root:
                row = {child.tag: child.text for child in element}
                rows.append(row)

            return rows
        except Exception as exc:
            self.logger.error("Failed to read XML for %s: %s", self.source_name, exc)
            return []