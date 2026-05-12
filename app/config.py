"""
config.py — Single source of truth for all configuration.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DBConfig:
    user:     str
    password: str
    host:     str
    port:     str
    name:     str

    @property
    def uri(self) -> str:
        return (
            f"mysql+mysqlconnector://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )

def _make_db(name: str) -> DBConfig:
    return DBConfig(
        user     = os.getenv("DB_USER",     "root"),
        password = os.getenv("DB_PASSWORD", ""), 
        host     = os.getenv("DB_HOST",     "127.0.0.1"),
        port     = os.getenv("DB_PORT",     "3306"),
        name     = name,
    )


DATABASES: dict[str, DBConfig] = {
    "covid_db":     _make_db("covid_db"),
    "playstore_db": _make_db("playstore_db"), 
}

@dataclass
class LLMConfig:
    api_key:    str
    model_name: str = "llama-3.1-8b-instant"
    temperature: float = 0.0

LLM = LLMConfig(
    api_key = os.getenv("GROQ_API_KEY", ""),
)

@dataclass
class AppConfig:
    title:            str  = "📊 AI Data Engineering Platform"
    page_icon:        str  = "📊"
    layout:           str  = "wide"
    default_db:       str  = "covid_db"
    max_history_rows: int  = 10

APP = AppConfig()

FORBIDDEN_SQL_KEYWORDS: list[str] = [
    "drop", "delete", "update", "insert",
    "alter", "truncate", "create", "grant", "revoke",
]

def validate() -> list[str]:
    errors = []
    if not LLM.api_key:
        errors.append("GROQ_API_KEY is missing in .env")
    return errors