# 📊 AI Data Engineering Platform

A production-grade AI-powered Data Engineering system that transforms natural language into SQL insights, interactive dashboards, and Arabic business intelligence.

Built with Streamlit, LangChain, Groq (LLaMA 3.1), MySQL, and Plotly, this platform demonstrates end-to-end Data Engineering + AI integration including ETL pipelines, secure SQL execution, and intelligent visualization.

---

## 🚀 Live Capabilities

- 🧠 Natural Language → SQL Query Engine (English + Arabic)
- 📊 Auto-generated Interactive Charts (Bar / Line / Pie)
- 🇸🇦 Arabic AI-generated Insights & Business Summaries
- 🔒 Secure SQL Execution Layer (Prevents DDL/DML attacks)
- 🗄️ Multi-Dataset Switching (COVID-19 / Play Store)
- ⚡ Low-latency LLM inference via Groq (LLaMA 3.1)
- 🔄 Production-style ETL pipelines for structured ingestion

---

## 🏗️ Architecture

User Query (Arabic / English)
→ Streamlit UI (app.py)
→ LangChain SQL Agent (agent.py)
→ SQL Safety Layer (utils.py)
→ MySQL Database (covid_db / playstore_db)
→ Pandas DataFrame
→ Plotly Visualizer
→ Arabic Insight Generator (LLM)
→ Final Dashboard Output

---

## 📁 Project Structure

ai-data-engineering-platform/

├── app/
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── agent.py
│   ├── visualizer.py
│   └── utils.py
│
├── etl/
│   ├── covid_etl.py
│   ├── playstore_etl.py
│   └── transform.py
│
├── sql/
│   ├── schema_covid.sql
│   └── schema_playstore.sql
│
├── tests/
│   └── test_sql_safety.py
│
├── .env
├── requirements.txt
├── Dockerfile
└── README.md

---

## ✨ Features

### 🤖 AI-Powered SQL Engine
Ask questions in English or Arabic and get instant SQL results.

### 📊 Smart Visualization Engine
Automatically generates the best chart type using Plotly.

### 🇸🇦 Arabic Insights
Human-like explanations and business summaries in Arabic.

### 🔒 SQL Safety Layer
Blocks dangerous SQL commands (DROP, DELETE, UPDATE).

### ⚡ Groq LLM Acceleration
Fast inference using LLaMA 3.1 8B.

### 🔄 ETL Pipelines
Clean, transform, and load datasets into MySQL.

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-data-engineering-platform.git
cd ai-data-engineering-platform

2. Create Virtual Environment
python -m venv venv

Activate:
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Setup Environment Variables
Create .env file:

GROQ_API_KEY=your_groq_api_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password

5. Initialize Database

mysql -u root -p < sql/schema_covid.sql
mysql -u root -p < sql/schema_playstore.sql

6. Run Application
cd app
streamlit run app.py

💡 Example Queries
Show top 10 countries by total deaths
What are the top categories by installs?

🧪 Testing
pytest tests/ -v

Streamlit
LangChain
Groq (LLaMA 3.1)
MySQL
Plotly
Pandas
SQLAlchemy

🔒 Security
SQL injection protection
Read-only query enforcement
Query sanitization layer
Safe execution pipeline

📦 Deployment
Supports:

Docker
Cloud deployment (AWS / GCP / Render)
Scalable MySQL backend

📝 License
MIT License


