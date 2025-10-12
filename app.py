from src.finance import get_financial_data
from src.news import get_news
from src.sentiment import sentiment_score





df["sentiment"] = df.apply(sentiment_score, axis=1)