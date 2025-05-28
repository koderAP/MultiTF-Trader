from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from ta.momentum import RSIIndicator

class MultiTFBacktestStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        close_prices = pd.Series(self.data.Close)
        rsi_indicator = RSIIndicator(close_prices, window=14)
        
        if len(rsi_indicator.rsi()) > 0:
            rsi = rsi_indicator.rsi().iloc[-1] 
            
            if rsi < 30 and not self.position:
                self.buy()
            elif rsi > 70 and self.position.is_long:
                self.position.close()
            elif rsi > 70 and not self.position:
                self.sell()
            elif rsi < 30 and self.position.is_short:
                self.position.close()


    
class MACDStrategy(Strategy):
    def init(self):
        close_prices = pd.Series(self.data.Close)
        self.macd_diff = self.I(
            lambda x: pd.Series(x).ewm(span=12, adjust=False).mean() - pd.Series(x).ewm(span=26, adjust=False).mean(),
            close_prices
        )
        self.signal_line = self.I(
            lambda x: pd.Series(x).ewm(span=9, adjust=False).mean(),
            self.macd_diff
        )

    def next(self):
        if crossover(self.macd_diff, self.signal_line) and not self.position:
            self.buy()
        elif crossover(self.signal_line, self.macd_diff) and self.position:
            self.position.close()
        elif crossover(self.macd_diff, self.signal_line) and not self.position:
            self.sell()
        elif crossover(self.signal_line, self.macd_diff) and self.position:
            self.position.close()

        

def extract_trade_log(bt):
    trades = bt.trades
    trade_log = []
    for trade in trades:
        trade_log.append({
            'entry_time': trade.entry_time,
            'exit_time': trade.exit_time,
            'entry_price': trade.entry_price,
            'exit_price': trade.exit_price,
            'profit': trade.pnl,
            'direction': 'long' if trade.is_long else 'short'
        })
    return pd.DataFrame(trade_log)

def run_backtest(df):
    # bt = Backtest(df, MultiTFBacktestStrategy, cash=5000000, commission=0.0002)  # Increase cash

    bt = Backtest(df, MACDStrategy, cash=5000000, commission=0.0002)  # Increase cash

    stats = bt.run()
    bt.plot()
    return stats, bt 






