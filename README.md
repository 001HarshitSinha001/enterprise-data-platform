# Enterprise Data Platform

This project implements a metadata-driven ETL pipeline for ingesting data from multiple source systems, transforming it, and producing curated datasets for analytics.

## Project Structure

- `ingestion/`: ingestion engine, connector factory, and transformer logic.
- `metadata/source_registry.json`: source metadata configuration.
- `source_systems/`: sample source systems and mock data.
- `data/raw/`: ingested raw snapshots.
- `data/staging/`: normalized staging data.
- `data/curated/`: analytics-ready curated datasets.

## Running the ETL Pipeline

1. Activate the Python virtual environment.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python run_pipeline.py
   ```

## Data Validation and Reporting

- The pipeline writes an ETL run report to `data/reports/`.
- Each report includes source row counts, validation results, numeric summaries, and top categorical values.
- Required columns can be configured per source in `metadata/source_registry.json` using `required_columns`.

## Notes

- Connectors support CSV, Excel, JSON, XML, API, PostgreSQL, Kafka, and MongoDB.
- Local fallback data is used for API, Kafka, MongoDB, and Finance if live access is unavailable.
- Transformed outputs are stored as CSV files in `data/staging/` and `data/curated/`.
