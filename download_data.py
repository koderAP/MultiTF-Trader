from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_SECRET_KEY
import pandas as pd
import os
from datetime import datetime

def get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_15MINUTE, start_str="30 days ago UTC"):
    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    klines = client.get_historical_klines(symbol, interval, start_str)

    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df = df.astype({
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": float
    })
    return df

def main():
    df = get_klines()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/BTCUSDT_15m.csv", index=False)
    print(f"Saved {len(df)} rows to data/BTCUSDT_15m.csv")

if __name__ == "__main__":
    main()
