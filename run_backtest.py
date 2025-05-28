import pandas as pd
from src.utils.data import load_ohlcv_csv, save_trades_to_csv, resample_to_1h
from src.strategy.multi_tf import MultiTimeframeStrategy
from src.backtesting.backtest import run_backtest
from src.backtesting.analyzer import extract_trade_log

def resample_to_1h(df):
    """
    Resample 15-minute data to 1-hour intervals.
    Ensures the 'Date' column is set as the index for resampling.
    """
    df.reset_index(inplace=True)
    print("Columns before renaming:", df.columns)

    df.rename(columns={
        'timestamp': 'Date',  # Ensure 'timestamp' is renamed to 'Date'
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)

    print("Columns after renaming:", df.columns)

    df.set_index('Date', inplace=True)

    print("Data after setting 'Date' as index:", df.head())

    return df.resample('1H').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()

def main():
    data_15m = load_ohlcv_csv("data/BTCUSDT_15m.csv")
    
    print("Loaded data (first few rows):", data_15m.head())

    data_1h = resample_to_1h(data_15m)

    strategy = MultiTimeframeStrategy(data_15m, data_1h)
    
    signals = strategy.generate_signals()
    print(f"Generated {len(signals)} signals")

    bt_result, bt_obj = run_backtest(data_15m)

    print("Backtest statistics:", bt_result)

    trades = extract_trade_log(bt_result)

    save_trades_to_csv(trades, "data/backtest_trades.csv")

if __name__ == "__main__":
    main()
