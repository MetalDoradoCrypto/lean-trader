#!/usr/bin/env python3
"""
Yahoo Finance Data Fetcher for Market Research
================================================
Fetch historical data for stocks, ETFs, crypto, and more.
"""

import yfinance as yf
import pandas as pd
import sys

def fetch_data(ticker, start="2020-01-01", end=None):
    """Fetch historical data from Yahoo Finance."""
    try:
        data = yf.download(ticker, start=start, end=end, progress=False)
        return data
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def analyze(data, ticker):
    """Basic technical analysis."""
    if data is None or data.empty:
        return
    
    # Simple moving averages
    data['SMA_20'] = data['Close'].rolling(20).mean()
    data['SMA_50'] = data['Close'].rolling(50).mean()
    data['SMA_200'] = data['Close'].rolling(200).mean()
    
    # Bollinger Bands
    data['BB_Mid'] = data['Close'].rolling(20).mean()
    data['BB_Std'] = data['Close'].rolling(20).std()
    data['BB_Upper'] = data['BB_Mid'] + (data['BB_Std'] * 2)
    data['BB_Lower'] = data['BB_Mid'] - (data['BB_Std'] * 2)
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Latest values
    latest = data.iloc[-1]
    print(f"\n=== {ticker} Analysis ===")
    print(f"Date: {latest.name}")
    print(f"Close: ${latest['Close']:.2f}")
    print(f"Volume: {latest['Volume']:,.0f}")
    print(f"\nMoving Averages:")
    print(f"  SMA 20:  ${latest['SMA_20']:.2f}" if pd.notna(latest['SMA_20']) else "  SMA 20: N/A")
    print(f"  SMA 50:  ${latest['SMA_50']:.2f}" if pd.notna(latest['SMA_50']) else "  SMA 50: N/A")
    print(f"  SMA 200: ${latest['SMA_200']:.2f}" if pd.notna(latest['SMA_200']) else "  SMA 200: N/A")
    print(f"\nTechnical Indicators:")
    print(f"  RSI(14):    {latest['RSI']:.2f}" if pd.notna(latest['RSI']) else "  RSI: N/A")
    print(f"  MACD:       {latest['MACD']:.4f}" if pd.notna(latest['MACD']) else "  MACD: N/A")
    print(f"  Signal:     {latest['Signal']:.4f}" if pd.notna(latest['Signal']) else "  Signal: N/A")
    print(f"\nBollinger Bands:")
    print(f"  Upper: ${latest['BB_Upper']:.2f}" if pd.notna(latest['BB_Upper']) else "  Upper: N/A")
    print(f"  Mid:   ${latest['BB_Mid']:.2f}" if pd.notna(latest['BB_Mid']) else "  Mid: N/A")
    print(f"  Lower: ${latest['BB_Lower']:.2f}" if pd.notna(latest['BB_Lower']) else "  Lower: N/A")
    
    # Save
    output_file = f"data/{ticker.replace('/', '_')}_daily.csv"
    os.makedirs("data", exist_ok=True)
    data.to_csv(output_file)
    print(f"\nSaved to {output_file}")
    
    return data

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "BTC-USD"
    start = sys.argv[2] if len(sys.argv) > 2 else "2020-01-01"
    
    print(f"Fetching {ticker} from {start}...")
    data = fetch_data(ticker, start)
    
    if data is not None:
        print(f"Fetched {len(data)} days of data")
        analyze(data, ticker)
