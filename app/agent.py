"""
agent.py — SQL Agent creation and invocation.
"""
import logging
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent


from config import LLM as LLMCfg
from db import get_langchain_db
from utils import extract_json, is_safe_sql, validate_agent_response

logger = logging.getLogger(__name__)

AGENT_INSTRUCTIONS = """
If the user asks for COVID data, use the 'owid_covid_latest' table. If the user asks for Play Store data, use the 'playstore_apps' table.
You are a SQL GENERATOR. 
Your ONLY job is to produce a JSON containing a SQL query.
Never answer the user question directly in text
STRICT RULE: Output ONLY a valid JSON object. 
NO introductory text, NO explanations before or after the JSON.
If you talk or add text outside the JSON, the system will crash.

Your output must be EXACTLY this structure:
{
  "sql": "SELECT ...",
  "chart": "line | bar | pie | none",
  "title": "Chart Title",
  "insight": "Arabic insight here"
}

Specific instructions for the data:
- Use 'app_name' and 'rating' columns for Play Store queries.
- Limit results to top 10 unless asked otherwise.
- The 'insight' field must be in Arabic and provide a professional analysis.
"""

@st.cache_resource(show_spinner=False)
def _build_agent(db_name: str):
    llm = ChatGroq(
        api_key    = LLMCfg.api_key,
        model_name = "llama-3.1-8b-instant",
        temperature= 0,
    )
    db = get_langchain_db(db_name)
    
    return create_sql_agent(
        llm,
        db=db,
        agent_type="tool-calling", 
        verbose=False,
        max_iterations=15, # ارفعها لـ 15
        handle_parsing_errors=True,
        extra_instructions=AGENT_INSTRUCTIONS,
    )

class AgentResponse:
    def __init__(self, sql: str, chart: str, title: str, insight: str):
        self.sql     = sql.strip()
        self.chart   = chart.strip().lower()
        self.title   = title.strip()
        self.insight = insight.strip()

class AgentError(Exception):
    pass

def run_agent(question: str, db_name: str) -> AgentResponse:
    agent = _build_agent(db_name)
    try:
        raw = agent.invoke({"input": question})
        result = extract_json(raw["output"])
    except Exception as e:
        raise AgentError(f"Agent failed: {e}")

    missing = validate_agent_response(result)
    if missing:
        raise AgentError(f"Missing keys: {missing}")

    safe, keyword = is_safe_sql(result["sql"])
    if not safe:
        raise AgentError(f"Unsafe SQL: {keyword}")

    return AgentResponse(
        sql     = result["sql"],
        chart   = result["chart"],
        title   = result["title"],
        insight = result["insight"],
    )