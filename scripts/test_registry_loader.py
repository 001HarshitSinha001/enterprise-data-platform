from ingestion.registry_loader import RegistryLoader


loader = RegistryLoader()

sources = loader.load_sources()

print(sources)