# 📊 AI Data Engineering Platform

A production-grade AI-powered data analysis platform built with **Streamlit**, **LangChain**, **Groq LLaMA 3.1**, and **MySQL** — featuring a full ETL pipeline, SQL safety layer, unit tests, and Docker support.

---

## 🏗️ Architecture

```
ai-data-engineering-platform/
│
├── app/
│   ├── app.py          # Streamlit UI (thin layer — rendering only)
│   ├── config.py       # Central config — single source of truth
│   ├── db.py           # DB connection manager + query runner
│   ├── agent.py        # SQL Agent logic (LangChain + Groq)
│   ├── visualizer.py   # Plotly chart builders
│   └── utils.py        # JSON parser, SQL safety, validators
│
├── etl/
│   ├── covid_etl.py    # COVID ETL pipeline (Extract → Transform → Load)
│   ├── tourism_etl.py  # Tourism ETL pipeline
│   └── transform.py    # Shared transformation utilities
│
├── sql/
│   ├── schema_covid.sql    # MySQL schema for covid_db
│   └── schema_tourism.sql  # MySQL schema for tourism
│
├── tests/
│   └── test_sql_safety.py  # Unit tests (pytest)
│
├── .env.example        # Config template
├── requirements.txt
├── Dockerfile
├── docker-compose.yml  # App + MySQL together
├── main.py             # CLI entry point
└── README.md
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 Natural Language Queries | Ask in Arabic or English |
| 📊 Auto Charts | Line / Bar / Donut charts via Plotly |
| 🧠 Arabic Insights | Professional analysis + recommendations |
| 🔒 SQL Safety Guard | Whole-word keyword blocking |
| 🗄️ Multi-DB Support | Switch between covid_db and tourism |
| 🔄 ETL Pipelines | Clean, transform, load raw CSVs to MySQL |
| 🧪 Unit Tests | pytest coverage for safety + parsing logic |
| 🐳 Docker | One-command deployment with docker-compose |
| 💻 CLI Mode | Run queries or ETL from the terminal |

---

## ⚙️ Setup

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-data-engineering-platform.git
cd ai-data-engineering-platform
```

### 2. Virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure `.env`

```bash
cp .env.example .env
# Edit .env and fill in GROQ_API_KEY and DB_PASSWORD
```

### 4. Set up MySQL schemas

```bash
mysql -u root -p < sql/schema_covid.sql
mysql -u root -p < sql/schema_tourism.sql
```

---

## 🚀 Running

### Option A — Local

```bash
streamlit run app/app.py
```

Open **http://localhost:8501**

### Option B — Docker (App + MySQL)

```bash
docker-compose up --build
```

### Option C — CLI

```bash
# Run a query
python main.py --db covid_db --question "أعلى 10 دول في الإصابات"
python main.py --db tourism  --question "أكثر مدينة تحقق دخلاً"

# Run ETL
python main.py --etl covid
python main.py --etl tourism
```

---

## 🔄 ETL Pipeline

1. Put your raw CSV files in `data/`:
   - `data/covid_raw.csv`
   - `data/tourism_raw.csv`

2. Run the ETL:
   ```bash
   python main.py --etl covid
   python main.py --etl tourism
   ```

The pipeline normalizes column names, drops near-empty rows, casts types, fills nulls, deduplicates, and adds derived columns automatically.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Tests cover: SQL safety (whole-word blocking), JSON extraction from noisy LLM output, and agent response validation.

---

## 🔒 Security

- API keys and passwords stored only in `.env` — never committed
- SQL safety guard blocks: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `CREATE`, `GRANT`, `REVOKE`
- Whole-word matching prevents false positives (e.g. `insertion_date` is allowed)
- Docker runs as non-root user

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI |
| [LangChain](https://langchain.com) | LLM orchestration |
| [Groq LLaMA 3.1 8B](https://groq.com) | Fast LLM inference |
| [Plotly](https://plotly.com) | Interactive charts |
| [SQLAlchemy](https://sqlalchemy.org) | DB connection pooling |
| [MySQL 8](https://mysql.com) | Data storage |
| [pytest](https://pytest.org) | Unit testing |
| [Docker](https://docker.com) | Containerization |

---

## 📝 License

MIT
