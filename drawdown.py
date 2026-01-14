import numpy as np
def drawdown_indicator(equity_curve):
    equity=np.array(equity_curve)
    peak=np.maximum.accumulate(equity_curve)
    drawdown_series=((equity-peak)/peak)
    current_drawdown=abs(drawdown_series[-1]) 
    max_drawdown=abs(drawdown_series.min())
    if current_drawdown<0.05:
        risk_level="LOW"
        
    elif current_drawdown<0.10:
        risk_level="MEDIUM"
        
    elif current_drawdown<0.20:
        risk_level="HIGH"

    else:
        risk_level="EXTREME"    
   
    return {
        "indicator": "Drawdown Risk",
        "current_drawdown_%": round(current_drawdown * 100, 2),
        "maximum_drawdown_%": round(max_drawdown * 100, 2),
        "risk_level": risk_level
    }  
