import pandas as pd
import streamlit as st
import sys
from pathlib import Path


root_path = str(Path(__file__).parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)


from config import APP, DATABASES, validate
from db import is_connected, run_query, get_table_names
from agent import run_agent, AgentError
from visualizer import render_chart, render_summary_metrics


st.set_page_config(
    page_title = APP.title,
    page_icon  = APP.page_icon,
    layout     = APP.layout,
)


errors = validate()
if errors:
    for err in errors:
        st.error(f"❌ {err}")
    st.stop()


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.title("⚙️ الإعدادات")

    db_choice = st.selectbox(
        "🗄️ قاعدة البيانات",
        options = list(DATABASES.keys()),
        index   = list(DATABASES.keys()).index(APP.default_db),
    )

    # Connection status
    status = "🟢 متصل" if is_connected(db_choice) else "🔴 غير متصل"
    st.caption(f"الحالة: {status}")

    # Table explorer
    with st.expander("📋 الجداول المتاحة"):
        try:
            tables = get_table_names(db_choice)
            for t in tables:
                st.markdown(f"- `{t}`")
        except Exception:
            st.warning("تعذّر تحميل الجداول.")

    st.markdown("---")

    # Example questions
    st.markdown("**💡 أمثلة:**")
    examples = {
        "covid_db": [
            "ما أعلى 10 دول في الإصابات؟",
            "ارسم خطاً زمنياً للوفيات",
            "قارن نسب التعافي بين الدول",
        ],
        "playstore_db": [
            "أعلى 10 تطبيقات في التقييم؟",
            "توزيع التطبيقات حسب الـ genre",
             "مقارنة التطبيقات المجانية والمدفوعة",
        ],
    }
    for ex in examples.get(db_choice, []):
        st.markdown(f"- {ex}")

    st.markdown("---")
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


st.title(APP.title)
st.caption(f"متصل بـ: **{db_choice}** | النموذج: llama-3.1-8b-instant")
st.divider()


for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "dataframe" in msg:
            df_restored = pd.DataFrame(msg["dataframe"])
            st.dataframe(df_restored, use_container_width=True)


placeholder = (
    "اسأل عن بيانات COVID..."
    if db_choice == "covid_db"
    else "اسأل عن بيانات Play Store..."
)
user_question = st.chat_input(placeholder)

if user_question:
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("🔍 جاري تحليل البيانات..."):
            try:
                response = run_agent(user_question, db_choice)
                df = run_query(response.sql, db_choice)

                if df.empty:
                    st.warning("⚠️ لم يتم العثور على بيانات لهذا السؤال.")
                else:
                    render_summary_metrics(df)
                    st.markdown("### 🧠 التحليل")
                    st.info(response.insight)
                    render_chart(response.chart, df, response.title)

                    with st.expander("📋 البيانات الخام"):
                        st.dataframe(df, use_container_width=True)

                    with st.expander("🔍 استعلام SQL"):
                        st.code(response.sql, language="sql")

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"**{response.title}**\n\n{response.insight}",
                        "dataframe": df.head(APP.max_history_rows).to_dict(),
                    })

            except AgentError as e:
                st.error(f"❌ {e}")
                st.info("💡 حاول إعادة صياغة السؤال.")
            except Exception as e:
                st.error(f"❌ خطأ غير متوقع: {e}")