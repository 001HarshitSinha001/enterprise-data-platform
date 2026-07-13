import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ingestion.connectors.base_connector import BaseConnector


class APIConnector(BaseConnector):

    def read(self):
        connection = self.config.get("connection", {})
        base_url = connection.get("base_url")
        endpoint = connection.get("endpoint", "")

        if not base_url:
            self.logger.error("Missing API base_url for source %s", self.source_name)
            return []

        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        request = Request(url, headers=connection.get("headers", {}))

        try:
            with urlopen(request, timeout=connection.get("timeout", 30)) as response:
                payload = response.read().decode("utf-8")
                return json.loads(payload)
        except (HTTPError, URLError, ValueError, ConnectionError) as exc:
            self.logger.warning(
                "API read failed for %s: %s. Attempting fallback local load.",
                self.source_name,
                exc,
            )
            return self._load_local_fallback()

    def _load_local_fallback(self):
        project_root = Path(__file__).resolve().parents[2]
        fallback_dir = project_root / "source_systems" / self.source_name

        if not fallback_dir.exists():
            return []

        for candidate in fallback_dir.glob("*.json"):
            try:
                with open(candidate, "r", encoding="utf-8") as file:
                    return json.load(file)
            except ValueError:
                continue

        return []