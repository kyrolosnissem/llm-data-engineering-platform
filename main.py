"""
main.py — CLI entry point.
"""

import argparse
import sys
import logging

logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt = "%H:%M:%S",
)
logger = logging.getLogger("main")

def run_query_cli(db_name: str, question: str) -> None:
    from app.config import validate
    from app.agent import run_agent, AgentError
    from app.db import run_query

    errors = validate()
    if errors:
        for e in errors:
            logger.error(e)
        sys.exit(1)

    try:
        response = run_agent(question, db_name)
        df = run_query(response.sql, db_name)
        print(f"\n📊 {response.title}")
        print(f"\n🧠 {response.insight}")
        print(f"\n🔍 SQL:\n{response.sql}")
        print(f"\n📋 Results ({len(df)} rows):\n{df.to_string(index=False)}")
    except AgentError as e:
        logger.error("Agent error: %s", e)
        sys.exit(1)

def run_etl(source: str) -> None:
    if source == "covid":
        from etl.covid_etl import run as etl_run
    elif source == "playstore":
        from etl.playstore_etl import run as etl_run
    else:
        logger.error("Unknown ETL source: %s", source)
        sys.exit(1)

    print(f"\n🔄 Running ETL for [{source}]...")
    etl_run()
    print("✅ ETL complete.")

def main():
    parser = argparse.ArgumentParser(description="AI Data Engineering Platform — CLI")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--question", "-q", type=str, help="Natural language question")
    group.add_argument("--etl", "-e", type=str, choices=["covid", "playstore"], help="Run ETL pipeline")

    parser.add_argument("--db", "-d", type=str, default="covid_db", 
                        choices=["covid_db", "playstore_db"], help="Database to query")

    args = parser.parse_args()

    if args.etl:
        run_etl(args.etl)
    else:
        run_query_cli(args.db, args.question)

if __name__ == "__main__":
    main()