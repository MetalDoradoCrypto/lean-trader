#lean/include: ../../
class Strategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(100000)
        
        # Add equity
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol
        
        # Simple moving average
        self.sma = self.SMA(self.symbol, 30, Resolution.Daily)
        
    def OnData(self, data):
        if not self.sma.IsReady:
            return
            
        if not self.Portfolio.Invested and self.Time.weekday == 0:  # Buy Monday
            if self.Securities[self.symbol].Close > self.sma.Current.Value:
                self.SetHoldings(self.symbol, 1)
                
        elif self.Portfolio.Invested and self.Time.weekday == 4:  # Sell Friday
            self.Liquidate()
