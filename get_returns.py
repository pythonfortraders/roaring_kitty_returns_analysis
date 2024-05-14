import pandas as pd
from datetime import datetime, timedelta
import alpaca_trade_api as tradeapi
import os
import logging

API_KEY = os.environ.get("ALPACA_API_KEY")
API_SECRET = os.environ.get("ALPACA_API_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"

logging.basicConfig(
    filename="data_fetch_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

df_tweets = pd.read_csv("roaring_kitty_tweets.csv", usecols=["timestamp"])
df_tweets["timestamp"] = pd.to_datetime(df_tweets["timestamp"])


def fetch_stock_data(symbol, start, end):
    start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end.strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        data = api.get_bars(symbol, "1Min", start=start, end=end).df
        return data["close"] if "close" in data.columns else pd.Series(dtype="float64")
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return pd.Series(dtype="float64")


def process_data(df, symbol):
    time_deltas = [
        timedelta(minutes=1),
        timedelta(minutes=5),
        timedelta(minutes=15),
        timedelta(hours=1),
    ]
    df["price_at_tweet"] = None
    for delta in time_deltas:
        returns_column = f"return_{delta.total_seconds()/60}min"
        df[returns_column] = None

        for index, row in df.iterrows():
            tweet_time = row["timestamp"]
            future_time = tweet_time + delta

            # Fetch stock data
            stock_prices = fetch_stock_data(symbol, tweet_time, future_time)

            if not stock_prices.empty:
                initial_price = stock_prices.iloc[0] if not stock_prices.empty else None
                future_price = stock_prices.iloc[-1] if not stock_prices.empty else None

                df.at[index, "price_at_tweet"] = initial_price
                if initial_price and future_price:
                    df.at[index, returns_column] = (
                        future_price - initial_price
                    ) / initial_price


process_data(df_tweets, "GME")


df_tweets.sort_values(by="timestamp", ascending=False, inplace=True)

df_tweets.to_csv("tweet_data_with_returns.csv", index=False)

