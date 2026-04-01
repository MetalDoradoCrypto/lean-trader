# Market Research Module

This module fetches and analyzes market data from multiple sources.

## Sources

- **Binance**: Crypto data (no API key needed)
- **Yahoo Finance**: Stocks, ETFs, crypto, forex

## Usage

```bash
# Fetch crypto data from Binance
python research/binance_data.py BTCUSDT 365

# Fetch stock/crypto data from Yahoo Finance
python research/yfinance_data.py BTC-USD 2020-01-01
python research/yfinance_data.py AAPL 2020-01-01
```

## Output

Data is saved to `data/` directory as CSV files with:
- OHLCV data
- Technical indicators (SMA, RSI, MACD, Bollinger Bands)
