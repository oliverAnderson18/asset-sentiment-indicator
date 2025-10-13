import yfinance as yf
import pandas as pd

def get_financial_data(asset: str) -> pd.DataFrame:
    ticker = yf.Ticker(asset)
    df = ticker.history(period="100d")
    if df.empty:
        print("Ticker not found.")
        return pd.DataFrame()
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df
