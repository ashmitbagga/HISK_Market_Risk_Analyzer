import backtrader as bt
import math

class strength(bt.Indicator):
    lines = ("strength", "risk")
    params = dict(
        adx_p=14,
        ma_p=20, 
        slope_p=5,
        adx_w=0.6, 
        ma_w=0.4,)
    
    def __init__(self):
        self.adx = bt.ind.ADX(self.data,period=self.p.adx_p)
        self.ma = bt.ind.EMA(self.data.close,period=self.p.ma_p)
        self.ma_slope = self.ma - self.ma(-self.p.slope_p) 
        
    def next(self):
        adx_s = min(self.adx[0]/50.0,1.0) 
        slope = abs(self.ma_slope[0])/self.data.close[0]
        slope_s = math.tanh(slope*10)
        s = (self.p.adx_w*adx_s+self.p.ma_w*slope_s) 
        self.lines.strength[0] = s #final strength
        self.lines.risk[0] = 1.0 - s #final risk
