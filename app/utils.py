"""
utils.py — Shared helpers: JSON extraction, SQL safety, formatting.
"""

import json
import re
import logging
from config import FORBIDDEN_SQL_KEYWORDS

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# JSON extractor
# ─────────────────────────────────────────
def extract_json(text: str) -> dict:
    """
    Safely extract a JSON object from an LLM response.
    Handles cases where the model adds prose around the JSON block.

    Raises:
        ValueError: if no valid JSON can be found.
    """
    # 1. Try direct parse (ideal case)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Strip markdown code fences  ```json ... ```
    fenced = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(fenced)
    except json.JSONDecodeError:
        pass

    # 3. Find first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not extract valid JSON from LLM response.\n"
        f"Raw output (first 500 chars):\n{text[:500]}"
    )


# ─────────────────────────────────────────
# SQL safety
# ─────────────────────────────────────────
def is_safe_sql(sql: str) -> tuple[bool, str]:
    """
    Check SQL for destructive keywords.

    Returns:
        (True, "") if safe
        (False, keyword) if dangerous keyword found
    """
    sql_lower = sql.lower()
    for keyword in FORBIDDEN_SQL_KEYWORDS:
        # Match whole words only — avoids false positives like 'insertion_date'
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, sql_lower):
            logger.warning("Blocked SQL keyword detected: %s", keyword)
            return False, keyword
    return True, ""


# ─────────────────────────────────────────
# Validation
# ─────────────────────────────────────────
REQUIRED_AGENT_KEYS = {"sql", "chart", "title", "insight"}

def validate_agent_response(result: dict) -> list[str]:
    """Return list of missing keys in agent response dict."""
    missing = REQUIRED_AGENT_KEYS - result.keys()
    return sorted(missing)


# ─────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────
def truncate_text(text: str, max_len: int = 300) -> str:
    """Truncate long strings for display."""
    return text if len(text) <= max_len else text[:max_len] + "..."


def format_number(n: float | int) -> str:
    """Format large numbers with commas."""
    return f"{n:,.0f}" if isinstance(n, (int, float)) else str(n)
