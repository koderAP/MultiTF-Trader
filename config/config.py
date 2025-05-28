import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
BASE_URL = "https://testnet.binance.vision"
SYMBOL = "BTCUSDT"
QUOTE_ASSET = "USDT"
BASE_ASSET = "BTC"
TRADE_QUANTITY = 0.001
