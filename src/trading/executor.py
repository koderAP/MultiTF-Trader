from datetime import datetime
from config.config import SYMBOL, TRADE_QUANTITY
from .exchange import BinanceClient

class TradeExecutor:
    def __init__(self):
        self.client = BinanceClient()

    def execute_signal(self, signal):
        if signal['direction'] == 'long':
            order = self.client.place_market_order(SYMBOL, 'BUY', TRADE_QUANTITY)
            return {
                'timestamp': datetime.utcnow(),
                'direction': 'long',
                'entry_price': float(order['fills'][0]['price']),
                'position_size': TRADE_QUANTITY,
                'status': order['status']
            }
        elif signal['direction'] == 'short':
            order = self.client.place_market_order(SYMBOL, 'SELL', TRADE_QUANTITY)
            return {
                'timestamp': datetime.utcnow(),
                'direction': 'short',
                'entry_price': float(order['fills'][0]['price']),
                'position_size': -TRADE_QUANTITY,
                'status': order['status']
            }
        else:
            raise ValueError("Invalid signal direction. Must be 'long' or 'short'.")
        return None
