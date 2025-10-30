import requests as r
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

apiKey = os.getenv("NEWSAPI_KEY")

def get_news(asset: str) -> pd.DataFrame:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": asset,
        "apiKey": apiKey
    }
    
    response = r.get(url, params=params)
    data = response.json() 
    
    df = pd.DataFrame(data["articles"])[["publishedAt", "title", "description", "content", "source"]]
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    return df