<div align="center">

# AI Data Engineering Platform

**Transform natural language into SQL insights — in Arabic and English**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.1-1C3C3C?style=flat&logo=chainlink&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=flat)](https://groq.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)](LICENSE)

</div>

---

## What This Does

You type a question in Arabic or English. The platform converts it to SQL, runs it safely against a real database, and returns an interactive chart with a professional Arabic business summary — in seconds.

```
"أعلى 10 تطبيقات في التقييم؟"
        ↓
  LangChain SQL Agent
        ↓
  SELECT title, score FROM app_reviews ORDER BY score DESC LIMIT 10
        ↓
  SQL Safety Check → Execute → DataFrame
        ↓
  Plotly Bar Chart  +  Arabic Insight
```

---

## Datasets

| Dataset | Records | Coverage | Key Fields |
|---|---|---|---|
| **Google Play Store** | 62,694 apps | 2010 – 2018, 48 genres | score, installs, reviews, genre, price |
| **COVID-19 (OWID)** | 247 countries | Global snapshot | total_cases, total_deaths, vaccinations |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Streamlit UI                      │
│  ┌─────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ Sidebar │  │  Chat UI │  │  Charts + Insights  │  │
│  └─────────┘  └──────────┘  └────────────────────┘  │
└───────────────────────┬─────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │   LangChain Agent   │
              │  (agent.py)         │
              │  Groq LLaMA 3.1 8B  │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │  SQL Safety Layer   │
              │  (utils.py)         │
              │  Blocks DDL/DML     │
              └─────────┬──────────┘
                        │
         ┌──────────────▼──────────────┐
         │         MySQL 8.0            │
         │  ┌────────────┐ ┌─────────┐ │
         │  │ covid_db   │ │playstore│ │
         │  │ 247 rows   │ │ 62K rows│ │
         │  └────────────┘ └─────────┘ │
         └─────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │  Pandas + Plotly    │
              │  (visualizer.py)    │
              │  Bar / Line / Pie   │
              └────────────────────┘
```

---

## Project Structure

```
ai-data-engineering-platform/
│
├── app/                        # Core application package
│   ├── config.py               # Central config — single source of truth
│   ├── db.py                   # Connection manager + query runner
│   ├── agent.py                # LangChain SQL Agent logic
│   ├── visualizer.py           # Plotly chart builders
│   ├── utils.py                # JSON parser, SQL safety, validators
│   └── app.py                  # Streamlit UI (thin layer — rendering only)
│
├── etl/                        # ETL pipelines
│   ├── transform.py            # Shared: normalize, cast, deduplicate
│   ├── covid_etl.py            # OWID COVID → covid_db
│   └── playstore_etl.py        # Play Store CSV → playstore_db
│
├── sql/                        # Database schemas
│   ├── schema_covid.sql
│   └── schema_playstore.sql
│
├── tests/
│   └── test_sql_safety.py      # 19 pytest cases
│
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml          # App + MySQL in one command
├── main.py                     # CLI entry point
└── README.md
```

---

## Setup

### Prerequisites
- Python 3.11+
- MySQL 8.0 running locally (or use Docker below)
- Groq API key — free at [console.groq.com](https://console.groq.com)

### Local Installation

**1. Clone**
```bash
git clone https://github.com/YOUR_USERNAME/ai-data-engineering-platform.git
cd ai-data-engineering-platform
```

**2. Virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Environment variables**
```bash
cp .env.example .env
```
Open `.env` and fill in:
```
GROQ_API_KEY=your_key_here
DB_PASSWORD=your_mysql_password
```

**4. Database schemas**
```bash
mysql -u root -p < sql/schema_covid.sql
mysql -u root -p < sql/schema_playstore.sql
```

**5. Load data**
```bash
mkdir data
cp path/to/owid-covid-latest.csv     data/
cp path/to/google-play-store.csv     data/

python main.py --etl covid
python main.py --etl playstore
```

**6. Run**
```bash
streamlit run app/app.py
```
Open **http://localhost:8501**

---

### Docker — one command

```bash
docker-compose up --build
```

Spins up MySQL, runs both SQL schemas on first boot, and starts the app. Open **http://localhost:8501**.

---

## Usage

### Web Interface

Switch datasets from the sidebar, then type any question:

| Question | Dataset |
|---|---|
| أعلى 10 تطبيقات في التقييم؟ | Play Store |
| توزيع التطبيقات حسب الفئة | Play Store |
| مقارنة التطبيقات المجانية والمدفوعة | Play Store |
| ما أعلى 10 دول في الإصابات؟ | COVID-19 |
| مقارنة نسب الوفيات بين القارات | COVID-19 |
| What genres have the highest average score? | Play Store |

### CLI

```bash
# Query
python main.py --db playstore_db --question "top 5 genres by installs"
python main.py --db covid_db     --question "أعلى دول في الوفيات"

# ETL
python main.py --etl covid
python main.py --etl playstore
```

---

## Security

The SQL Safety Layer in `utils.py` uses **whole-word regex matching** to block destructive operations before any query reaches the database.

**Blocked keywords:** `DROP` `DELETE` `UPDATE` `INSERT` `ALTER` `TRUNCATE` `CREATE` `GRANT` `REVOKE`

```python
# Whole-word match — won't block legitimate column names
# "insertion_date"  → ✅ allowed
# "DROP TABLE"      → ❌ blocked
pattern = rf"\b{keyword}\b"
```

---

## Testing

```bash
pytest tests/ -v
```

19 test cases covering SQL safety (including edge cases like `insertion_date`), JSON extraction from noisy LLM output, and agent response validation.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit 1.32 |
| LLM Orchestration | LangChain 0.1 |
| Inference | Groq — LLaMA 3.1 8B Instant |
| Visualization | Plotly |
| Data Layer | Pandas + SQLAlchemy |
| Database | MySQL 8.0 |
| Containerization | Docker + Compose |
| Testing | pytest |

---

## License

MIT
