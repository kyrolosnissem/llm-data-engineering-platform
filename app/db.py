"""
db.py — Database connection manager.
"""
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from langchain_community.utilities import SQLDatabase


from config import DATABASES, DBConfig

@st.cache_resource(show_spinner=False)
def get_engine(db_name: str):
    cfg: DBConfig = _get_cfg(db_name)
    return create_engine(cfg.uri, pool_pre_ping=True, pool_recycle=3600)

@st.cache_resource(show_spinner=False)
def get_langchain_db(db_name: str) -> SQLDatabase:
    cfg: DBConfig = _get_cfg(db_name)
    return SQLDatabase.from_uri(cfg.uri)

def is_connected(db_name: str) -> bool:
    try:
        engine = get_engine(db_name)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False

def run_query(sql: str, db_name: str) -> pd.DataFrame:
    engine = get_engine(db_name)
    return pd.read_sql(sql, engine)

def get_table_names(db_name: str) -> list[str]:
    db = get_langchain_db(db_name)
    return db.get_usable_table_names()

def _get_cfg(db_name: str) -> DBConfig:
    if db_name not in DATABASES:
        raise ValueError(f"Unknown database: '{db_name}'. Available: {list(DATABASES)}")
    return DATABASES[db_name]