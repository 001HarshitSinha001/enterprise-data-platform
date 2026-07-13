import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from ingestion.registry_loader import RegistryLoader
from ingestion.connector_factory import ConnectorFactory
from ingestion.reporter import ETLReporter
from ingestion.transformer import DataTransformer
from shared.validation import DataValidator


class IngestionEngine:

    def __init__(self):
        self.loader = RegistryLoader()
        self.transformer = DataTransformer()
        self.reporter = ETLReporter()
        self.validator = DataValidator()
        project_root = Path(__file__).resolve().parents[1]
        self.raw_root = project_root / "data" / "raw"
        self.staging_root = project_root / "data" / "staging"
        self.curated_root = project_root / "data" / "curated"

    def run(self):
        sources = self.loader.load_sources()
        run_report = {
            "run_timestamp": datetime.utcnow().isoformat(),
            "sources": [],
        }

        for source in sources:
            if not source.get("enabled", False):
                continue

            result = self._run_source(source)
            run_report["sources"].append(result)

        report_path = self.reporter.save_run_report(run_report)
        summary_path = self.reporter.save_consolidated_report(run_report)

        print(f"\nETL report saved: {report_path}")
        print(f"ETL summary CSV saved: {summary_path}")

    def run_source(self, source: dict):
        result = self._run_source(source)
        run_report = {
            "run_timestamp": datetime.utcnow().isoformat(),
            "sources": [result],
        }
        report_path = self.reporter.save_run_report(run_report)
        summary_path = self.reporter.save_consolidated_report(run_report)

        print(f"\nETL report saved: {report_path}")
        print(f"ETL summary CSV saved: {summary_path}")

    def _run_source(self, source: dict) -> dict:
        print(f"\nProcessing: {source['source_name']}")
        connector = ConnectorFactory.get_connector(source)
        data = connector.read()

        record_count = self._record_count(data)
        print(f"Records Read: {record_count}")

        raw_path = self._write_raw(source, data)
        print(f"Raw data written: {raw_path}")

        staging_df = self.transformer.stage(source, data)
        staging_path = self._write_dataframe(source, staging_df, self.staging_root, "staging")
        print(f"Staging data written: {staging_path} ({len(staging_df)} rows)")

        curated_df = self.transformer.curate(source, staging_df)
        curated_path = self._write_dataframe(source, curated_df, self.curated_root, "curated")
        print(f"Curated data written: {curated_path} ({len(curated_df)} rows)")

        validation_result = self.validator.validate_dataframe(
            curated_df,
            required_columns=source.get("required_columns", []),
        )

        summary = self.reporter.summarize_curated(source["source_name"], curated_df)
        return {
            "source_name": source["source_name"],
            "record_count": record_count,
            "staging_rows": len(staging_df),
            "curated_rows": len(curated_df),
            "validation": validation_result,
            "summary": summary,
        }

    def _record_count(self, data: Any) -> int:
        if data is None:
            return 0

        if isinstance(data, pd.DataFrame):
            return len(data)

        if isinstance(data, dict):
            return 1

        if isinstance(data, list):
            return len(data)

        return 1

    def _write_raw(self, source: dict, data: Any) -> Path:
        destination = Path(source.get("destination", {}).get("path", source["source_name"]))
        raw_dir = self.raw_root / destination
        raw_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        raw_file = raw_dir / f"{source['source_name']}_{timestamp}_raw.json"

        if isinstance(data, pd.DataFrame):
            payload = data.to_dict(orient="records")
        else:
            payload = data if data is not None else []

        with open(raw_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, default=str, indent=2)

        return raw_file

    def _write_dataframe(self, source: dict, df: pd.DataFrame, root: Path, layer: str) -> Path:
        destination = Path(source.get("destination", {}).get("path", source["source_name"]))
        output_dir = root / destination
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{layer}.csv"
        df.to_csv(output_file, index=False)

        return output_file
