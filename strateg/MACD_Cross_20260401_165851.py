from AlgorithmImports import *

class MACDCross(QCAlgorithm):
    """MACD>Signal indicates momentum shift"""
    
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(100000)
        self.sym = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.sma200 = self.SMA(self.sym, 200, Resolution.Daily)
        self.rsi = self.RSI(self.sym, 14, Resolution.Daily)
        self.bb = self.BB(self.sym, 20, 2, MovingAverageType.Simple, Resolution.Daily)
        self.macd = self.MACD(self.sym, 12, 26, 9, Resolution.Daily)
        self.vol_sma = self.SMA(self.sym, 20, Resolution.Daily)
        self.SetWarmUp(200)
    
    def OnData(self, data):
        if self.IsWarmingUp: return
        if not self.Portfolio.Invested:
            if self.ShouldEntry(data): self.SetHoldings(self.sym, 1)
        else:
            if self.ShouldExit(data): self.Liquidate()
    
    def ShouldEntry(self, data):
        if not data.ContainsKey(self.sym): return False
        bar = data[self.sym]
        p = bar.Close
        rsi_ok = self.rsi.IsReady and self.rsi.Current.Value < 30
        price_ok = self.sma200.IsReady and p > self.sma200.Current.Value
        macd_ok = self.macd.IsReady and self.macd.Current.Value > self.macd.Signal.Current.Value
        vol_ok = self.vol_sma.IsReady and bar.Volume > self.vol_sma.Current.Value * 2
        if "MACD_Cross" == "RSI_Momentum": return rsi_ok and price_ok
        elif "MACD_Cross" == "MACD_Cross": return macd_ok
        elif "MACD_Cross" == "BB_Bounce":
            bb_ok = self.bb.IsReady and p < self.bb.LowerBand.Current.Value
            return bb_ok and rsi_ok
        elif "MACD_Cross" == "Volume_Surge": return vol_ok and p > bar.Open
        elif "MACD_Cross" == "EMA_Cross":
            e9 = self.EMA(self.sym, 9, Resolution.Daily)
            e21 = self.EMA(self.sym, 21, Resolution.Daily)
            return e9.Current.Value > e21.Current.Value if e9.IsReady and e21.IsReady else False
        return False
    
    def ShouldExit(self, data):
        if not data.ContainsKey(self.sym): return True
        bar = data[self.sym]
        entry = self.Portfolio[self.sym].AveragePrice
        curr = bar.Close
        loss = (entry - curr) / entry * 100
        if loss > 2.0: return True
        gain = (curr - entry) / entry * 100
        if gain > 4.0: return True
        if self.Time.hour >= 15 and self.Time.minute >= 45: return True
        return False