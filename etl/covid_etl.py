"""
covid_etl.py — ETL pipeline for the COVID dataset.

Flow:
    Extract  → CSV / API source
    Transform → clean, normalize, cast types
    Load     → MySQL covid_db

Usage:
    python main.py --etl covid
"""

import logging
import pandas as pd
from sqlalchemy import text

from app.db import get_engine
from etl.transform import (
    normalize_column_names,
    drop_empty_rows,
    cast_numeric,
    cast_dates,
    fill_nulls,
    deduplicate,
    summary,
)

logger = logging.getLogger(__name__)

DB_NAME     = "covid_db"
TABLE_NAME  = "covid_data"

# ─── TODO: add more columns as needed ───

SOURCE       = "data/owid-covid-latest.csv"

DATE_COLS    = ["last_updated"]
NUMERIC_COLS = [
    "total_cases", "new_cases", "total_deaths", "new_deaths",
    "total_cases_per_million", "total_deaths_per_million",
    "reproduction_rate", "total_vaccinations",
    "people_vaccinated", "people_fully_vaccinated", "population",
]


# ─────────────────────────────────────────
# Steps
# ─────────────────────────────────────────
def extract() -> pd.DataFrame:
    logger.info("Extracting COVID data from: %s", SOURCE)
    # ── Swap this block if your source is an API or a database ──
    df = pd.read_csv(SOURCE)
    logger.info("Extracted %d rows.", len(df))
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming COVID data...")
    df = normalize_column_names(df)
    df = drop_empty_rows(df)
    df = cast_numeric(df, NUMERIC_COLS)
    df = cast_dates(df, DATE_COLS)
    df = fill_nulls(df)
    df = deduplicate(df, subset=["location"])

    # Derived column: case_fatality_rate
    # Derived column: case_fatality_rate
    if {"total_deaths", "total_cases"}.issubset(df.columns):

        df["case_fatality_rate"] = (
            df["total_deaths"].div(df["total_cases"].replace(0, pd.NA)) * 100
        ).fillna(0).round(2)
    return df

def load(df: pd.DataFrame) -> None:
    logger.info("Loading %d rows into %s.%s ...", len(df), DB_NAME, TABLE_NAME)
    
    engine = get_engine(DB_NAME)

    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists='replace',      # replace = Drop + Create + Insert
        index=False,
        chunksize=1000,
        method='multi'
    )
    
    logger.info(f"✅ Load completed successfully ({len(df):,} rows).")


# ─────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────
def run() -> None:
    df_raw       = extract()
    df_clean     = transform(df_raw)
    load(df_clean)
