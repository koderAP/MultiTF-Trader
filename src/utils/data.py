import pandas as pd

def load_ohlcv_csv(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df

def save_trades_to_csv(trades, path):
    df = pd.DataFrame(trades)
    df.to_csv(path, index=False)

def resample_to_1h(df):
    df.columns = df.columns.str.lower()

    required_columns = ['open', 'high', 'low', 'close', 'volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise KeyError(f"Missing columns: {', '.join(missing_columns)}")

    return df.resample('1H').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

