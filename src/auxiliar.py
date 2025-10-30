import streamlit as st
import plotly.graph_objects as go


def mean_average_score(score: int) -> str:
    if score <= 25:
        return "Strongly negative sentiment"
    elif score <= 49:
        return "Moderately negative sentiment"
    elif score <= 51:
        return "Neutral sentiment"
    elif score <= 75:
        return "Moderately positive sentiment"
    else:
        return "Strongly positive sentiment"


def plot_ta_columns_in_rows(df, columns_to_plot=None, title_prefix="TA Plot"):
    if columns_to_plot is None:
        columns_to_plot = df.select_dtypes(include="number").columns.tolist()
    n_cols = 3
    for i in range(0, len(columns_to_plot), n_cols):
        row_cols = st.columns(min(n_cols, len(columns_to_plot) - i))
        for j, col_name in enumerate(columns_to_plot[i:i+n_cols]):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df[col_name], mode='lines', name=col_name))
            fig.update_layout(
                title=f"{title_prefix}: {col_name}",
                xaxis_title="Date",
                yaxis_title="Value",
                template="plotly_white"
            )
            row_cols[j].plotly_chart(fig, use_container_width=True)
