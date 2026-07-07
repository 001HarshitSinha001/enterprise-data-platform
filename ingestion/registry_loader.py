import json
from pathlib import Path


class RegistryLoader:
    """
    Loads all source system metadata from source_registry.json.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        self.registry_path = (
            project_root / "metadata" / "source_registry.json"
        )

    def load_sources(self):
        """
        Reads the source registry and returns all configured sources.
        """

        with open(self.registry_path, "r", encoding="utf-8") as file:
            sources = json.load(file)

        return sources