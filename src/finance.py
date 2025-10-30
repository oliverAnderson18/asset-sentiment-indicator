import yfinance as yf
import pandas as pd
import ta

options = ["SMA50", "SMA200", "MACD", "ADX", "RSI", "Stochastic Oscillator",
           "OBV", "MA50", "Bollinger Bands", "ATR"]


def get_financial_records(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period="500d", interval="1d")
    if df.empty:
        raise ValueError("Ticker not found")
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"})
    df = df.dropna()
    return df


def get_ta_records(df: pd.DataFrame, options: list) -> pd.DataFrame:
    df = df.copy()
    close = df["close"].squeeze()   # fuerza a Serie 1D
    high = df["high"].squeeze()
    low = df["low"].squeeze()
    volume = df["volume"].squeeze()

    if "SMA50" in options:
        df["SMA50"] = close.rolling(window=50).mean()
    if "SMA200" in options:
        df["SMA200"] = close.rolling(window=200).mean()
    if "MACD" in options:
        macd = ta.trend.MACD(close)
        df["MACD"] = macd.macd()
        df["MACD_signal"] = macd.macd_signal()
    if "ADX" in options:
        adx = ta.trend.ADXIndicator(high, low, close)
        df["ADX"] = adx.adx()
    if "RSI" in options:
        rsi = ta.momentum.RSIIndicator(close)
        df["RSI"] = rsi.rsi()
    if "Stochastic Oscillator" in options:
        stoch = ta.momentum.StochasticOscillator(high, low, close)
        df["Stoch"] = stoch.stoch()
        df["Stoch_signal"] = stoch.stoch_signal()
    if "OBV" in options:
        obv = ta.volume.OnBalanceVolumeIndicator(close, volume)
        df["OBV"] = obv.on_balance_volume()
    if "MA50" in options:
        df["MA50"] = close.rolling(window=50).mean()
    if "Bollinger Bands" in options:
        bb = ta.volatility.BollingerBands(close)
        df["BB_high"] = bb.bollinger_hband()
        df["BB_low"] = bb.bollinger_lband()
    if "ATR" in options:
        atr = ta.volatility.AverageTrueRange(high, low, close)
        df["ATR"] = atr.average_true_range()

    return df.dropna()
