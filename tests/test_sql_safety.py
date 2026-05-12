"""
test_sql_safety.py — Unit tests for utils.py (SQL safety + JSON extraction).

Run with:
    pytest tests/ -v
"""

import pytest
import sys
import os

# Make sure the project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.utils import is_safe_sql, extract_json, validate_agent_response


# ─────────────────────────────────────────
# is_safe_sql
# ─────────────────────────────────────────
class TestIsSafeSql:

    def test_select_is_safe(self):
        safe, kw = is_safe_sql("SELECT * FROM covid_data")
        assert safe is True
        assert kw == ""

    def test_select_with_where(self):
        safe, _ = is_safe_sql("SELECT country, deaths FROM covid_data WHERE date > '2020-01-01'")
        assert safe is True

    def test_drop_blocked(self):
        safe, kw = is_safe_sql("DROP TABLE covid_data")
        assert safe is False
        assert kw == "drop"

    def test_delete_blocked(self):
        safe, kw = is_safe_sql("DELETE FROM covid_data WHERE id = 1")
        assert safe is False
        assert kw == "delete"

    def test_update_blocked(self):
        safe, kw = is_safe_sql("UPDATE covid_data SET deaths = 0")
        assert safe is False
        assert kw == "update"

    def test_insert_blocked(self):
        safe, kw = is_safe_sql("INSERT INTO covid_data VALUES (1, 'Egypt', 100)")
        assert safe is False
        assert kw == "insert"

    def test_truncate_blocked(self):
        safe, kw = is_safe_sql("TRUNCATE TABLE covid_data")
        assert safe is False
        assert kw == "truncate"

    def test_alter_blocked(self):
        safe, kw = is_safe_sql("ALTER TABLE covid_data ADD COLUMN test INT")
        assert safe is False
        assert kw == "alter"

    def test_case_insensitive(self):
        safe, kw = is_safe_sql("DrOp TaBlE covid_data")
        assert safe is False
        assert kw == "drop"

    def test_keyword_in_column_name_not_blocked(self):
        """'insertion_date' should NOT be blocked — only whole-word match."""
        safe, _ = is_safe_sql("SELECT insertion_date FROM bookings")
        assert safe is True

    def test_subquery_safe(self):
        sql = "SELECT country FROM (SELECT country, SUM(confirmed) FROM covid_data GROUP BY country) t"
        safe, _ = is_safe_sql(sql)
        assert safe is True


# ─────────────────────────────────────────
# extract_json
# ─────────────────────────────────────────
class TestExtractJson:

    VALID_PAYLOAD = {
        "sql": "SELECT * FROM covid_data LIMIT 10",
        "chart": "bar",
        "title": "Top Countries",
        "insight": "مصر في المرتبة الأولى",
    }

    def test_clean_json(self):
        import json
        result = extract_json(json.dumps(self.VALID_PAYLOAD))
        assert result == self.VALID_PAYLOAD

    def test_json_with_prose_before(self):
        import json
        text = f"Here is the result:\n{json.dumps(self.VALID_PAYLOAD)}"
        result = extract_json(text)
        assert result["chart"] == "bar"

    def test_json_with_markdown_fence(self):
        import json
        text = f"```json\n{json.dumps(self.VALID_PAYLOAD)}\n```"
        result = extract_json(text)
        assert result["sql"].startswith("SELECT")

    def test_invalid_raises_value_error(self):
        with pytest.raises(ValueError):
            extract_json("This is just plain text with no JSON.")

    def test_partial_json_raises(self):
        with pytest.raises(ValueError):
            extract_json('{"sql": "SELECT 1"')  # unterminated


# ─────────────────────────────────────────
# validate_agent_response
# ─────────────────────────────────────────
class TestValidateAgentResponse:

    def test_all_keys_present(self):
        result = {"sql": "x", "chart": "bar", "title": "t", "insight": "i"}
        missing = validate_agent_response(result)
        assert missing == []

    def test_missing_insight(self):
        result = {"sql": "x", "chart": "bar", "title": "t"}
        missing = validate_agent_response(result)
        assert "insight" in missing

    def test_missing_multiple(self):
        result = {"sql": "x"}
        missing = validate_agent_response(result)
        assert set(missing) == {"chart", "title", "insight"}

    def test_extra_keys_ok(self):
        result = {"sql": "x", "chart": "bar", "title": "t", "insight": "i", "extra": "y"}
        assert validate_agent_response(result) == []
