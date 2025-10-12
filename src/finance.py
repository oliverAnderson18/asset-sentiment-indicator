import yfinance as yf
import pandas as pd

def get_financial_data(asset: str) -> pd.DataFrame:
    ticker = yf.Ticker(asset)
    df = ticker.history(period="7d")
    if df.empty:
        print("Ticker not found.")
        return None
    df["Date"] = pd.to_datetime(df["Date"])
    return df
    
    