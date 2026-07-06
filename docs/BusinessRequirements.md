# Business Requirements

## Project Name
Enterprise Data Platform (EDP)

## Company Overview
RetailHub is an e-commerce company that collects data from multiple operational systems. The business requires a centralized data platform to ingest, process, validate, and serve data for analytics and reporting.

## Business Problem
Different departments generate data in different formats and technologies. Manually integrating these sources is time-consuming and difficult to maintain.

## Objective
Build a metadata-driven enterprise data platform capable of:

- Ingesting data from multiple source systems.
- Supporting different file formats and databases.
- Automating data ingestion workflows.
- Validating data quality.
- Transforming raw data into analytics-ready datasets.
- Serving curated datasets to business users.

## Source Systems

| Source | Type | Frequency |
|---------|------|-----------|
| Customer | REST API | Hourly |
| HR | REST API | Daily |
| Orders | PostgreSQL | Every 15 minutes |
| Finance | PostgreSQL | Daily |
| Products | CSV | Daily |
| Inventory | Excel | Daily |
| Marketing | JSON | Daily |
| Logistics | XML | Daily |
| Payments | Kafka | Real-time |
| Support | MongoDB | Hourly |

## Expected Outcome

- Centralized Data Lake
- Curated Data Warehouse
- Automated ETL Pipelines
- Metadata-driven Ingestion
- Scalable Architecture