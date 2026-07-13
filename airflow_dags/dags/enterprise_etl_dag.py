from datetime import timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

PROJECT_ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.registry_loader import RegistryLoader
from ingestion.ingestion_engine import IngestionEngine


def run_source(source_name: str):
    engine = IngestionEngine()
    loader = RegistryLoader()
    sources = loader.load_sources()
    source = next((item for item in sources if item["source_name"] == source_name), None)

    if source is None:
        raise ValueError(f"Source not found: {source_name}")

    engine.run_source(source)


with DAG(
    dag_id="enterprise_data_platform_etl",
    default_args={
        "owner": "EDP Team",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Run the enterprise data platform ETL pipeline in Airflow.",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=["enterprise", "etl", "data_platform"],
) as dag:

    loader = RegistryLoader()
    sources = loader.load_sources()

    tasks = []
    for source in sources:
        if not source.get("enabled", False):
            continue

        task = PythonOperator(
            task_id=f"run_{source['source_name']}",
            python_callable=run_source,
            op_kwargs={"source_name": source["source_name"]},
        )

        tasks.append(task)

    if tasks:
        tasks[0]  # ensure DAG is not empty
