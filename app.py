from src.finance import options, get_financial_records, get_ta_records
from src.news import get_news
from src.sentiment import sentiment_score
from src.auxiliar import mean_average_score, plot_ta_columns_in_rows
from src.keyfrases import keyfrases
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

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
if "df_ta" not in st.session_state:
    st.session_state.df_ta = None

@st.cache_data(show_spinner=False)
def get_cached_news(asset):
    df = get_news(asset)
    if df is None or df.empty:
        return pd.DataFrame()
    df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.date
    df["sentiment"] = df.apply(sentiment_score, axis=1)
    df["source_name"] = df["source"].apply(lambda x: x["name"] if isinstance(x, dict) and "name" in x else str(x))
    return df

@st.cache_data(show_spinner=False)
def get_cached_financial_records(asset):
    return get_financial_records(asset)

@st.cache_data(show_spinner=False)
def get_cached_ta_records(ticker, indicators_tuple):
    df = get_cached_financial_records(ticker)
    return get_ta_records(df, list(indicators_tuple))

def extract_keywords_from_content(df, keywords):
    text = " ".join(df["content"].dropna().astype(str)).lower()
    found = [kw for kw in keywords if kw in text]
    counter = Counter(found)
    return pd.DataFrame(counter.most_common(10), columns=["Keyword", "Count"])

if st.button("Start analysis"):
    with st.spinner("Analysing..."):
        try:
            df = get_cached_news(asset)
            if df.empty:
                st.error("No news found for this ticker")
            else:
                mean_sentiment = df["sentiment"].mean()
                first_date = str(df["publishedAt"].iloc[0])
                top3_values = df["source_name"].value_counts().index[:3]
                result = ', '.join(map(str, top3_values))
                st.session_state.df = df
                st.session_state.mean_sentiment = mean_sentiment
                st.session_state.result = result
                st.session_state.first_date = first_date
                st.session_state.analysis_done = True
        except Exception as e:
            st.error(f"Error fetching news: {e}")

if st.session_state.analysis_done:
    df = st.session_state.df
    st.caption(f"Fetching dates up to {st.session_state.first_date}")
    st.caption(f"News from sources like {st.session_state.result}")
    st.header(f"Average sentiment score is: {st.session_state.mean_sentiment:.2f}")
    st.markdown(f"{mean_average_score(st.session_state.mean_sentiment)}")

    col1, col2 = st.columns(2)

    with col1:
        fig_hist = px.histogram(
            df, x="sentiment", nbins=20, range_x=[0, 100],
            title="Sentiment Distribution",
            labels={"sentiment": "Sentiment Score", "count": "Frequency"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        df_kw = extract_keywords_from_content(df, keyfrases)
        if not df_kw.empty:
            fig_pie = px.pie(df_kw, names="Keyword", values="Count", title="Most Frequent Financial Phrases")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No financial phrases found in news content.")

    with st.form("ta_form"):
        st.header("TA analysis:")
        selected = st.multiselect("Select the indicators desired", options, default=st.session_state.selected_indicators)
        submitted = st.form_submit_button("Confirm Picks")
    if submitted:
        st.session_state.selected_indicators = selected
        if st.session_state.selected_indicators:
            st.session_state.run_ta = True

if st.session_state.run_ta and st.session_state.selected_indicators:
    with st.spinner("Analysing TA..."):
        try:
            df_ta = get_cached_ta_records(asset, tuple(st.session_state.selected_indicators))
            st.session_state.df_ta = df_ta
            st.success(f"Running technical analysis with: {', '.join(st.session_state.selected_indicators)}")
            plot_ta_columns_in_rows(df_ta, columns_to_plot=st.session_state.selected_indicators)
            st.session_state.run_ta = False
        except ValueError as e:
            st.error(str(e))
            st.session_state.run_ta = False
        except Exception as e:
            st.error(f"Error calculating TA: {e}")
            st.session_state.run_ta = False
