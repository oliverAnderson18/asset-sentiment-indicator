from src.finance import get_financial_data
from src.news import get_news
from src.sentiment import sentiment_score
import streamlit as st 
import pandas as pd

st.title("Asset Sentiment Indicator")
asset = st.text_input("Introduce your asset (preferably the ticker)")

if st.button("Start analysis"):
    with st.spinner("Analysing..."):
        df = get_news(asset)
        df_prices = get_financial_data(asset)
        df["publishedAt"] = pd.to_datetime(df["publishedAt"]).dt.date
        df_prices["Date"] = pd.to_datetime(df_prices["Date"]).dt.date
        df["sentiment"] = df.apply(sentiment_score, axis=1)
        merged_df = df.merge(df_prices, left_on="publishedAt", right_on="Date", how="left")
        merged_df = merged_df.sort_values(by="publishedAt", ascending=False)
    st.success("Task completed!")
    st.dataframe(merged_df)


