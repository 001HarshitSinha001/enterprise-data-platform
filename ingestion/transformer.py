import re
from datetime import datetime
from pathlib import Path

import pandas as pd


def _normalize_column_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"[^a-z0-9_]+", "", name)
    return name


class DataTransformer:

    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent
        self.staging_root = project_root / "data" / "staging"
        self.curated_root = project_root / "data" / "curated"

    def stage(self, source, data):
        df = self._to_dataframe(data)

        if df.empty:
            return df

        df = self._clean_column_names(df)
        df = self._normalize_fields(df)
        df["source_name"] = source["source_name"]
        df["ingested_at"] = datetime.utcnow().isoformat()

        return df

    def curate(self, source, staging_df):
        if staging_df.empty:
            return staging_df

        source_name = source["source_name"]
        strategy = {
            "customer_api": self._curate_customers,
            "products_csv": self._curate_products,
            "inventory_excel": self._curate_inventory,
            "marketing_json": self._curate_marketing,
            "logistics_xml": self._curate_logistics,
            "orders_db": self._curate_orders,
        }

        return strategy.get(source_name, self._default_curate)(staging_df.copy())

    def _to_dataframe(self, data):
        if isinstance(data, pd.DataFrame):
            return data.copy()

        if data is None:
            return pd.DataFrame()

        if isinstance(data, dict):
            return pd.DataFrame([data])

        try:
            return pd.DataFrame(data)
        except ValueError:
            return pd.DataFrame([data])

    def _clean_column_names(self, df):
        df = df.copy()
        df.columns = [_normalize_column_name(col) for col in df.columns]
        return df

    def _normalize_fields(self, df):
        df = df.copy()

        for column in df.columns:
            if df[column].dtype == object:
                df[column] = df[column].astype(str).str.strip()

            if "date" in column:
                df[column] = pd.to_datetime(df[column], errors="coerce")

            if column in {"price", "amount", "budget", "quantity", "reorder_level"}:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        return df

    def _curate_customers(self, df):
        df = df.copy()
        if "first_name" in df.columns and "last_name" in df.columns:
            df["full_name"] = (
                df["first_name"].fillna("") + " " + df["last_name"].fillna("")
            ).str.strip()

        df["membership"] = df.get("membership", pd.Series(dtype="object")).astype(str)
        return df.drop_duplicates().reset_index(drop=True)

    def _curate_products(self, df):
        df = df.copy()
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["stock_status"] = df["stock_status"].str.title()
        df["is_in_stock"] = df["stock_status"] == "In Stock"
        df["product_name"] = df["product_name"].str.title()
        return df.drop_duplicates().reset_index(drop=True)

    def _curate_inventory(self, df):
        df = df.copy()
        df["needs_reorder"] = df["quantity"].fillna(0) <= df["reorder_level"].fillna(0)
        df["warehouse"] = df["warehouse"].str.title()
        return df.drop_duplicates().reset_index(drop=True)

    def _curate_marketing(self, df):
        df = df.copy()
        df["campaign_duration_days"] = (
            df["end_date"] - df["start_date"]
        ).dt.days
        df["campaign_status"] = df["status"].str.title()
        df["is_active_campaign"] = df["campaign_status"] == "Active"
        return df.drop_duplicates().reset_index(drop=True)

    def _curate_logistics(self, df):
        df = df.copy()
        status_mapping = {
            "shipped": "Delivered",
            "in transit": "In Transit",
            "delayed": "Delayed",
            "delivered": "Delivered",
        }
        df["status_category"] = (
            df["status"].str.lower().map(status_mapping).fillna(df["status"])
        )
        df["destination"] = df["destination"].str.title()
        return df.drop_duplicates().reset_index(drop=True)

    def _curate_orders(self, df):
        df = df.copy()
        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
            df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
            df["order_weekday"] = df["order_date"].dt.day_name()

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["is_high_value"] = df["amount"] > 1000
        return df.drop_duplicates().reset_index(drop=True)

    def _default_curate(self, df):
        return df.drop_duplicates().reset_index(drop=True)
