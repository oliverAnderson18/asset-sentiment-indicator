from src.finance import options, get_financial_records, get_ta_records
from src.news import get_news
from src.sentiment import sentiment_score
from src.auxiliar import mean_average_score, plot_ta_columns_in_rows
import streamlit as st
import pandas as pd

st.title("Asset Sentiment Indicator")

asset = st.text_input("Introduce your asset (ticker symbol)")

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "df" not in st.session_state:
    st.session_state.df = None
if "mean_sentiment" not in st.session_state:
    st.session_state.mean_sentiment = None
if "result" not in st.session_state:
    st.session_state.result = None
if "selected_indicators" not in st.session_state:
    st.session_state.selected_indicators = []
if "run_ta" not in st.session_state:
    st.session_state.run_ta = False

if st.button("Start analysis"):
    with st.spinner("Analysing..."):
        try:
            df = get_news(asset)
            if df.empty:
                st.error("No news found for this ticker")
            else:
                df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.date
                df["sentiment"] = df.apply(sentiment_score, axis=1)
                mean_sentiment = df["sentiment"].mean()
                first_date = str(df["publishedAt"].iloc[0])
                df["source_name"] = df["source"].apply(lambda x: x["name"] if isinstance(x, dict) and "name" in x else str(x))
                top3_values = df["source_name"].value_counts().index[:3]
                result = ', '.join(map(str, top3_values))
                st.session_state.df = df
                st.session_state.mean_sentiment = mean_sentiment
                st.session_state.result = result
                st.session_state.first_date = first_date
                st.session_state.analysis_done = True
        except Exception:
            st.error("Error fetching news")

if st.session_state.analysis_done:
    st.caption(f"Fetching dates up to {st.session_state.first_date}")
    st.caption(f"News from sources like {st.session_state.result}")
    st.header(f"Average sentiment score is: {st.session_state.mean_sentiment:.2f}")
    st.subheader(f"{mean_average_score(st.session_state.mean_sentiment)}")

    st.write("Select the indicators desired:")

    st.session_state.selected_indicators = []
    rows = [options[:4], options[4:7], options[7:]]
    for row in rows:
        cols = st.columns(len(row))
        for i, ind in enumerate(row):
            if cols[i].checkbox(ind, value=(ind in st.session_state.selected_indicators)):
                st.session_state.selected_indicators.append(ind)

    if st.button("Confirm Picks"):
        st.session_state.run_ta = True

if st.session_state.run_ta and st.session_state.selected_indicators:
    with st.spinner("Analysing TA..."):
        try:
            df_ta = get_ta_records(get_financial_records(asset), st.session_state.selected_indicators)
            st.success(f"Running technical analysis with: {', '.join(st.session_state.selected_indicators)}")
            plot_ta_columns_in_rows(df_ta, columns_to_plot=st.session_state.selected_indicators)
            st.session_state.run_ta = False
        except ValueError as e:
            st.error(str(e))
            st.session_state.run_ta = False
        except Exception as e:
            st.error(f"Error calculating TA: {e}")
            st.session_state.run_ta = False
