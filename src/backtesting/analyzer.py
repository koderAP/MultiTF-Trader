import pandas as pd

def extract_trade_log(bt_result):
    trades = bt_result['_trades']
    trades['PnL'] = trades['ExitPrice'] - trades['EntryPrice']
    trades.rename(columns={
        'EntryTime': 'timestamp',
        'Size': 'position_size',
        'EntryPrice': 'entry_price',
        'ExitPrice': 'exit_price',
        'PnL': 'pnl'
    }, inplace=True)
    trades['direction'] = trades['position_size'].apply(lambda x: 'long' if x > 0 else 'short')
    return trades[['timestamp', 'direction', 'entry_price', 'exit_price', 'position_size', 'pnl']]
