import time
import pandas as pd
from datetime import datetime
from src.utils.data import load_ohlcv_csv, save_trades_to_csv
from src.strategy.multi_tf import MultiTimeframeStrategy
from src.trading.executor import TradeExecutor

def resample_to_1h(df):
    """
    Resample 15-minute data to 1-hour intervals.
    Ensures the 'Date' column is set as the index for resampling.
    """
    # Reset the index to make 'timestamp' a column
    df.reset_index(inplace=True)

    # Check the columns before renaming
    print("Columns before renaming:", df.columns)

    # Rename columns
    df.rename(columns={
        'timestamp': 'Date',  # Ensure 'timestamp' is renamed to 'Date'
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)

    # Check the columns after renaming
    print("Columns after renaming:", df.columns)

    # Set 'Date' as the index
    df.set_index('Date', inplace=True)

    # Print to confirm the structure
    print("Data after setting 'Date' as index:", df.head())

    # Perform resampling and aggregate
    return df.resample('1H').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()

def fetch_latest_data():
    df = pd.read_csv("data/BTCUSDT_15m.csv", parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    df = df.last("2D")  # Most recent 2 days for TA stability
    df.rename(columns={
        'timestamp': 'Date',  # Ensure 'timestamp' is renamed to 'Date'
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)

    # Print the column names to verify
    print(f"Columns before resampling: {df.columns}")
    
    return df, resample_to_1h(df)




def main():
    executor = TradeExecutor()
    live_trades = []

    while True:
        data_15m, data_1h = fetch_latest_data()
        strategy = MultiTimeframeStrategy(data_15m, data_1h)
        signals = strategy.generate_signals()

        if signals:
            last_signal = signals[-1]
            if last_signal['timestamp'] > data_15m.index[-2]:
                result = executor.execute_signal(last_signal)
                result['exit_price'] = None
                result['pnl'] = None
                live_trades.append(result)
                save_trades_to_csv(live_trades, "data/live_trades.csv")
                print(f"Executed trade: {result}")
        else:
            print(f"{datetime.utcnow()} - No new signals")

        time.sleep(1)

if __name__ == "__main__":
    main()
