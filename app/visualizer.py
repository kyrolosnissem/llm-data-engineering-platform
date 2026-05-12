"""
visualizer.py — All chart rendering logic.
Takes a DataFrame + chart type and returns a Plotly figure.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ─────────────────────────────────────────
# Color palette
# ─────────────────────────────────────────
PALETTE = px.colors.qualitative.Set2


# ─────────────────────────────────────────
# Internal builders
# ─────────────────────────────────────────
def _base_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title      = dict(text=title, font=dict(size=17), x=0.5),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor  = "rgba(0,0,0,0)",
        margin     = dict(t=60, b=40, l=40, r=40),
        legend     = dict(orientation="h", yanchor="bottom", y=-0.3),
    )
    return fig


def _line_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    fig = px.line(df, x=x, y=y, title=title, markers=True,
                  color_discrete_sequence=PALETTE)
    return _base_layout(fig, title)


def _bar_chart(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    fig = px.bar(df, x=x, y=y, title=title,
                 color=x, color_discrete_sequence=PALETTE,
                 text_auto=True)
    fig.update_traces(textposition="outside")
    return _base_layout(fig, title)


def _pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    fig = px.pie(df, names=names, values=values, title=title,
                 color_discrete_sequence=PALETTE, hole=0.35)   # donut style
    return _base_layout(fig, title)


# ─────────────────────────────────────────
# Public interface
# ─────────────────────────────────────────
SUPPORTED_CHARTS = {"line", "bar", "pie"}


def render_chart(chart_type: str, df: pd.DataFrame, title: str) -> None:
    """
    Render the appropriate Plotly chart in Streamlit.
    Does nothing if chart_type is 'none' or df has fewer than 2 columns.
    """
    if chart_type not in SUPPORTED_CHARTS:
        return

    if len(df.columns) < 2:
        st.info("⚠️ البيانات لا تكفي لرسم مخطط (أقل من عمودين).")
        return

    x_col, y_col = df.columns[0], df.columns[1]

    try:
        if chart_type == "line":
            fig = _line_chart(df, x_col, y_col, title)
        elif chart_type == "bar":
            fig = _bar_chart(df, x_col, y_col, title)
        elif chart_type == "pie":
            fig = _pie_chart(df, x_col, y_col, title)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"⚠️ تعذّر رسم المخطط: {e}")
        st.dataframe(df, use_container_width=True)


def render_summary_metrics(df: pd.DataFrame) -> None:
    """Show quick top-line KPI metrics for a numeric DataFrame."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        return

    cols = st.columns(min(len(numeric_cols), 4))
    for col_ui, col_name in zip(cols, numeric_cols[:4]):
        total = df[col_name].sum()
        col_ui.metric(
            label=col_name.replace("_", " ").title(),
            value=f"{total:,.0f}",
        )
