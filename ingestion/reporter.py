import json
from datetime import datetime
from pathlib import Path

import pandas as pd


class ETLReporter:

    def __init__(self):
        project_root = Path(__file__).resolve().parents[1]
        self.report_root = project_root / "data" / "reports"
        self.report_root.mkdir(parents=True, exist_ok=True)

    def save_run_report(self, report: dict) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_path = self.report_root / f"etl_report_{timestamp}.json"

        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(report, file, default=str, indent=2)

        return report_path

    def save_consolidated_report(self, report: dict) -> Path:
        rows = []
        for source_report in report.get("sources", []):
            rows.append(
                {
                    "source_name": source_report.get("source_name"),
                    "record_count": source_report.get("record_count"),
                    "staging_rows": source_report.get("staging_rows"),
                    "curated_rows": source_report.get("curated_rows"),
                    "valid": source_report.get("validation", {}).get("valid"),
                    "missing_columns": json.dumps(source_report.get("validation", {}).get("missing_columns", [])),
                    "null_columns": json.dumps(source_report.get("validation", {}).get("null_columns", {})),
                    "duplicate_issues": json.dumps(source_report.get("validation", {}).get("duplicate_issues", [])),
                }
            )

        output_path = self.report_root / "etl_summary.csv"
        pd.DataFrame(rows).to_csv(output_path, index=False)
        return output_path

    def summarize_curated(self, source_name: str, df: pd.DataFrame) -> dict:
        summary = {
            "source_name": source_name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "numeric_summary": self._numeric_summary(df),
            "top_values": self._top_values(df),
        }
        return summary

    def _numeric_summary(self, df: pd.DataFrame) -> dict:
        numeric = df.select_dtypes(include="number")
        summary = {
            column: {
                "mean": numeric[column].mean(),
                "min": numeric[column].min(),
                "max": numeric[column].max(),
                "null_count": int(numeric[column].isna().sum()),
            }
            for column in numeric.columns
        }
        return summary

    def _top_values(self, df: pd.DataFrame) -> dict:
        top_values = {}
        for column in df.select_dtypes(include="object").columns:
            values = df[column].dropna().astype(str)
            top_values[column] = values.value_counts().head(5).to_dict()
        return top_values
