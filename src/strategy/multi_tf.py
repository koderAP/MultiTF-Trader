import pandas as pd
from ta.momentum import RSIIndicator
from .base import BaseStrategy

class MultiTimeframeStrategy(BaseStrategy):
    def __init__(self, data_15m, data_1h):
        super().__init__(data_15m, data_1h)

    def generate_signals(self):
        self.data_15m['rsi'] = RSIIndicator(self.data_15m['Close']).rsi()
        self.data_1h['rsi'] = RSIIndicator(self.data_1h['Close']).rsi()

        signals = []

        for timestamp, row in self.data_15m.iterrows():
            if row['rsi'] < 30:
                confirm_window = self.data_1h[self.data_1h.index <= timestamp]
                if not confirm_window.empty:
                    last_rsi_1h = confirm_window['rsi'].iloc[-1]
                    if last_rsi_1h < 35:
                        signals.append({
                            'timestamp': timestamp,
                            'direction': 'long',
                            'price': row['Close']
                        })
            elif row['rsi'] > 70:
                confirm_window = self.data_1h[self.data_1h.index <= timestamp]
                if not confirm_window.empty:
                    last_rsi_1h = confirm_window['rsi'].iloc[-1]
                    if last_rsi_1h > 65:
                        signals.append({
                            'timestamp': timestamp,
                            'direction': 'short',
                            'price': row['Close']
                        })

        # Remove duplicate signals
        unique_signals = []
        seen_timestamps = set()
        for signal in signals:
            if signal['timestamp'] not in seen_timestamps:
                unique_signals.append(signal)
                seen_timestamps.add(signal['timestamp'])

        # # Sort signals by timestamp
        # unique_signals.sort(key=lambda x: x['timestamp'])
        # # Filter out signals that are too close together
        # filtered_signals = []
        # for i in range(len(unique_signals)):
        #     if i == 0 or (unique_signals[i]['timestamp'] - unique_signals[i-1]['timestamp']).total_seconds() > 3600:
        #         filtered_signals.append(unique_signals[i])
        # # Return the filtered signals
        # signals = pd.DataFrame(filtered_signals)
        # signals['timestamp'] = pd.to_datetime(signals['timestamp'])
        # signals.set_index('timestamp', inplace=True)
        # signals['price'] = signals['price'].astype(float)
        # signals['direction'] = signals['direction'].astype(str)
        # signals['signal'] = signals['direction'].apply(lambda x: 1 if x == 'long' else -1)
        # signals['signal'] = signals['signal'].astype(int)
        # signals['rsi_15m'] = self.data_15m.loc[signals.index]['rsi'].values
        # signals['rsi_1h'] = self.data_1h.loc[signals.index]['rsi'].values
        # signals['rsi_15m'] = signals['rsi_15m'].astype(float)
        # signals['rsi_1h'] = signals['rsi_1h'].astype(float)
        # signals['rsi_15m'] = signals['rsi_15m'].round(2)
        # signals['rsi_1h'] = signals['rsi_1h'].round(2)
        # signals['signal'] = signals['signal'].astype(int)
        # signals['price'] = signals['price'].astype(float)
        # signals['direction'] = signals['direction'].astype(str)

        return signals
