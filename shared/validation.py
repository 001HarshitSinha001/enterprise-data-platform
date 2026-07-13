import pandas as pd
from typing import List, Dict, Any


class DataValidator:

    @staticmethod
    def validate_dataframe(
        df: pd.DataFrame,
        required_columns: List[str] = None,
        unique_keys: List[List[str]] = None,
    ) -> Dict[str, Any]:
        if required_columns is None:
            required_columns = []
        if unique_keys is None:
            unique_keys = []

        missing = [col for col in required_columns if col not in df.columns]
        null_columns = {
            col: int(df[col].isna().sum())
            for col in required_columns
            if col in df.columns and df[col].isna().any()
        }

        duplicate_issues = []
        for key_group in unique_keys:
            if all(key in df.columns for key in key_group):
                duplicates = int(df.duplicated(subset=key_group).sum())
                if duplicates:
                    duplicate_issues.append(
                        {"keys": key_group, "duplicate_count": duplicates}
                    )

        valid = not missing and not null_columns and not duplicate_issues

        return {
            "valid": valid,
            "missing_columns": missing,
            "null_columns": null_columns,
            "duplicate_issues": duplicate_issues,
            "row_count": len(df),
        }
