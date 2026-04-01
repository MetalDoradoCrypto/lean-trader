#!/usr/bin/env python3
"""
Binance Data Fetcher for Market Research
=========================================
Fetch historical klines to analyze market patterns.
"""

from binance.client import Client
import pandas as pd
import json
from datetime import datetime, timedelta

def fetch_klines(symbol="BTCUSDT", interval="1d", days=365):
    """Fetch historical klines from Binance."""
    client = Client()  # No API key needed for public data
    
    # Calculate start date
    start_date = (datetime.now() - timedelta(days=days)).strftime("%d %b %Y %H:%M:%S")
    
    try:
        klines = client.get_historical_klines(symbol, interval, start_date)
        
        # Convert to DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Parse timestamps
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date'] = df['datetime'].dt.date
        
        # Select relevant columns
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df = df.astype({'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def analyze_patterns(df):
    """Basic pattern analysis."""
    if df is None or df.empty:
        return
    
    # Simple moving averages
    df['sma_20'] = df['close'].rolling(20).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    
    # RSI calculation
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Latest values
    latest = df.iloc[-1]
    print(f"\nLatest Data for {latest['date']}:")
    print(f"  Close: ${latest['close']:.2f}")
    print(f"  Volume: {latest['volume']:,.0f}")
    print(f"  SMA 20: ${latest['sma_20']:.2f}" if pd.notna(latest['sma_20']) else "  SMA 20: N/A")
    print(f"  SMA 50: ${latest['sma_50']:.2f}" if pd.notna(latest['sma_50']) else "  SMA 50: N/A")
    print(f"  RSI(14): {latest['rsi']:.2f}" if pd.notna(latest['rsi']) else "  RSI: N/A")
    
    # Save to CSV
    output_file = f"data/{symbol.lower()}_daily.csv"
    os.makedirs("data", exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")

if __name__ == "__main__":
    import sys
    import os
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 365
    
    print(f"Fetching {symbol} data for last {days} days...")
    df = fetch_klines(symbol, "1d", days)
    
    if df is not None:
        print(f"Fetched {len(df)} days of data")
        analyze_patterns(df)
