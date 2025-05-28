# MultiTF-Trader is a modular trading system built in Python that
implements a multi-timeframe trading strategy using 15-minute entry
signals and 1-hour confirmations. It supports both backtesting via
`backtesting.py` and live trading on the Binance Testnet.

## Key Features 

-   Multi-Timeframe Strategy: Entry signals on 15m; confirmation on
    1h timeframe

-   Robust Backtesting: Simulate trades on historical data with
    logging

-   Live Trading Support: Integrates with Binance Testnet API

-   Detailed Logging: Trade metadata, P&L, timestamps, and more

-   Modular Design: Clean, extensible, class-based architecture

## Strategy Description 

The trading logic consists of:

-   Entry signals generated using indicators on 15-minute candles

-   Confirmation based on 1-hour trend and volatility filters

-   Risk management using stop-loss, take-profit, and dynamic position
    sizing based on volatility and account equity

## Project Structure 

    MultiTF-Trader/
    ├── README.md
    ├── requirements.txt
    ├── config/
    │   └── config.py           # API keys and config
    ├── src/
    │   ├── strategy/
    │   │   ├── base.py         # Base strategy class
    │   │   └── multi_tf.py     # Multi-timeframe strategy logic
    │   ├── backtesting/
    │   │   ├── backtest.py     # Backtesting engine
    │   │   └── analyzer.py     # Backtest analysis
    │   ├── trading/
    │   │   ├── exchange.py     # Binance API interface
    │   │   └── executor.py     # Order execution logic
    │   └── utils/
    │       ├── logger.py       # Logging utility
    │       └── data.py         # Data handling
    └── data/
        ├── backtest_trades.csv # Trade logs (backtest)
        └── live_trades.csv     # Trade logs (live)

## Trade Logging 

Trades (both simulated and live) include the following fields:

-   Timestamp

-   Trade direction (Long/Short)

-   Entry and exit prices

-   Position size

-   Profit and Loss (PnL)

-   Metadata (e.g., indicators, timeframe tags)

## Development Guidelines 

-   Comment and document all public classes and methods

-   Use structured logging for monitoring and debugging

-   Keep API keys in `.env` files and never commit them to version
    control

## Dependencies 

Main Python packages used:

-   `backtesting.py`

-   `python-binance`

-   `pandas`, `numpy`

-   `ta` (Technical Analysis Library)

-   `python-dotenv`

## Notes 

-   Always validate strategy thoroughly using Binance Testnet

-   Monitor execution latency during live trading

-   Regularly analyze performance and update strategy if needed

## Acknowledgments 

-   Binance for providing the Testnet API

-   `backtesting.py` developers

-   Contributors to the `ta` technical analysis library
