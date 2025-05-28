from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_SECRET_KEY, BASE_URL

class BinanceClient:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
        self.client.API_URL = BASE_URL

    def get_balance(self, asset):
        balances = self.client.get_account()['balances']
        for b in balances:
            if b['asset'] == asset:
                return float(b['free'])
        return 0

    def place_market_order(self, symbol, side, quantity):
        return self.client.create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )

    def get_symbol_price(self, symbol):
        return float(self.client.get_symbol_ticker(symbol=symbol)['price'])
