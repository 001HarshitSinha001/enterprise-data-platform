import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.registry_loader import RegistryLoader

loader = RegistryLoader()
sources = loader.load_sources()

print(f"Loaded {len(sources)} sources")

for source in sources:
    print(source["source_name"])