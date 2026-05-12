"""
playstore_etl.py — ETL for Google Play Store.
"""

import logging
import pandas as pd
from sqlalchemy import text
from app.db import get_engine
from etl.transform import (
    normalize_column_names, drop_empty_rows, cast_numeric,
    cast_dates, fill_nulls, deduplicate, summary,
)

logger = logging.getLogger(__name__)

DB_NAME    = "playstore_db" 
TABLE_NAME = "app_reviews"
SOURCE     = "data/google-play-store.csv"

DATE_COLS    = ["released"]
NUMERIC_COLS = ["reviews", "ratings", "min_installs", "score", "price", 
                "ratings_per_day", "rating_one_star", "rating_two_star", 
                "rating_three_star", "rating_four_star", "rating_five_star"]
BOOL_COLS    = ["offers_iap", "ad_supported"]

def extract() -> pd.DataFrame:
    logger.info("Extracting Play Store data from: %s", SOURCE)
    return pd.read_csv(SOURCE)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming Play Store data...")

    df = normalize_column_names(df)
    df = drop_empty_rows(df)
    df = cast_numeric(df, NUMERIC_COLS)
    df = cast_dates(df, DATE_COLS)

    # تحويل bool columns لـ 0/1
    for col in BOOL_COLS:
        if col in df.columns:
            df[col] = df[col].map(
                {True: 1, False: 0, "True": 1, "False": 0}
            ).fillna(0).astype(int)

    df = fill_nulls(df)
    df = deduplicate(df, subset=["app_id"])

  
    total_ratings = (
        df["rating_one_star"] + df["rating_two_star"] +
        df["rating_three_star"] + df["rating_four_star"] +
        df["rating_five_star"]
    )
    
    
    df["five_star_ratio"] = (df["rating_five_star"].div(total_ratings.replace(0, pd.NA)) * 100).fillna(0).round(2)

    # Derived:
    df["is_free"] = (df["price"] == 0).astype(int)

    summary(df, "Play Store (post-transform)")
    return df

def load(df: pd.DataFrame) -> None:
    logger.info("Loading %d rows into %s.%s", len(df), DB_NAME, TABLE_NAME)
    
    engine = get_engine(DB_NAME)

    with engine.begin() as conn:
        df.to_sql(
            name=TABLE_NAME,
            con=conn,
            if_exists='replace',      
            index=False,
            chunksize=1000,
            method='multi'
        )
        
       
        
        logger.info(f"✅ Successfully loaded {len(df):,} rows into {TABLE_NAME}")

def run():
    df_raw = extract()
    df_clean = transform(df_raw)
    load(df_clean)