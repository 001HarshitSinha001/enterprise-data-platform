import argparse
import threading
import time
from datetime import datetime, timedelta

from ingestion.ingestion_engine import IngestionEngine
from ingestion.registry_loader import RegistryLoader


class SimpleScheduler:

    def __init__(self, poll_interval_seconds: int = 30):
        self.loader = RegistryLoader()
        self.engine = IngestionEngine()
        self.poll_interval_seconds = poll_interval_seconds
        self.last_run = {}

    def get_interval_seconds(self, schedule: str) -> int:
        schedule = schedule.strip()

        if schedule == "@continuous":
            return 60
        if schedule == "@hourly":
            return 3600
        if schedule == "@daily":
            return 86400

        parts = schedule.split()
        if len(parts) == 5 and parts[0].startswith("*/"):
            try:
                minutes = int(parts[0][2:])
                return minutes * 60
            except ValueError:
                pass

        if len(parts) == 5 and parts[0] == "0" and parts[1] == "*":
            return 3600

        return 86400

    def should_run(self, source: dict) -> bool:
        schedule = source.get("schedule", "@daily")
        interval = self.get_interval_seconds(schedule)
        source_name = source["source_name"]
        last = self.last_run.get(source_name)

        if last is None:
            return True

        return (datetime.utcnow() - last).total_seconds() >= interval

    def run_source_task(self, source: dict) -> None:
        try:
            print(f"Starting scheduled source: {source['source_name']}")
            self.engine.run_source(source)
        except Exception as exc:
            print(f"Error running source {source['source_name']}: {exc}")
        finally:
            self.last_run[source["source_name"]] = datetime.utcnow()

    def run_once(self, sources: list[dict]) -> None:
        for source in sources:
            if self.should_run(source):
                self.run_source_task(source)

    def run(self, once: bool = False) -> None:
        sources = [
            source
            for source in self.loader.load_sources()
            if source.get("enabled", False)
        ]

        print("Starting SimpleScheduler...")

        if once:
            self.run_once(sources)
            return

        while True:
            self.run_once(sources)
            time.sleep(self.poll_interval_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the lightweight ETL scheduler for enabled sources."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run enabled sources once and exit.",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=30,
        help="Scheduler poll interval in seconds.",
    )
    parser.add_argument(
        "--source",
        action="append",
        help="Run only the named source(s). Can be repeated.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    scheduler = SimpleScheduler(poll_interval_seconds=args.poll_interval)
    if args.source:
        enabled_sources = [
            source
            for source in scheduler.loader.load_sources()
            if source.get("enabled", False) and source["source_name"] in args.source
        ]
        missing = [name for name in args.source if name not in {s["source_name"] for s in enabled_sources}]
        if missing:
            print(f"Warning: source(s) not found or not enabled: {', '.join(missing)}")
        if not enabled_sources:
            print("No enabled sources matched the provided names. Exiting.")
            return
        for source in enabled_sources:
            if scheduler.should_run(source):
                scheduler.run_source_task(source)
            else:
                print(f"Skipping source {source['source_name']} because its schedule has not elapsed.")
        return

    scheduler.run(once=args.once)


if __name__ == "__main__":
    main()
