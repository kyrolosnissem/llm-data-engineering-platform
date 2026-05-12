"""
transform.py — Shared transformation utilities for ETL pipelines.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase, strip, replace spaces with underscores."""
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )
    return df


def drop_empty_rows(df: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """Drop rows where more than `threshold` fraction of columns are null."""
    min_non_null = int(len(df.columns) * (1 - threshold))
    before = len(df)
    df = df.dropna(thresh=min_non_null)
    dropped = before - len(df)
    if dropped:
        logger.info("Dropped %d near-empty rows.", dropped)
    return df


def cast_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce columns to numeric, setting errors to NaN."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def cast_dates(df: pd.DataFrame, columns: list[str],
               fmt: str | None = None) -> pd.DataFrame:
    """Parse date columns."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=fmt, errors="coerce")
    return df


def fill_nulls(df: pd.DataFrame, numeric_val: float = 0,
               string_val: str = "Unknown") -> pd.DataFrame:
    """Fill numeric nulls with 0, string nulls with 'Unknown'."""
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(numeric_val)
        else:
            df[col] = df[col].fillna(string_val)
    return df


def deduplicate(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows."""
    before = len(df)
    df = df.drop_duplicates(subset=subset)
    removed = before - len(df)
    if removed:
        logger.info("Removed %d duplicate rows.", removed)
    return df


def summary(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """Log a quick shape/null summary."""
    logger.info(
        "%s → shape=%s | nulls=%d | dtypes: %s",
        name, df.shape,
        df.isnull().sum().sum(),
        df.dtypes.value_counts().to_dict(),
    )
