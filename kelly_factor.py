import numpy as np
import pandas as pd


class KellyRisk:

    def __init__(self, cap=1.0, epsilon=1e-8):
        self.cap = cap
        self.epsilon = epsilon

    # ---------------------------------------------------
    # 1. RAW KELLY COMPUTATION
    # ---------------------------------------------------
    def raw_kelly(self, returns):
        returns = np.array(returns)

        mu = np.mean(returns)
        var = np.var(returns) + self.epsilon

        kelly = mu / var
        return float(np.clip(kelly, -self.cap, self.cap))

    # ---------------------------------------------------
    # 2. ROLLING KELLY (REGIME AWARE)
    # ---------------------------------------------------
    def rolling_kelly(self, returns, window=50):
        returns = pd.Series(returns)

        def _kelly(x):
            mu = x.mean()
            var = x.var() + self.epsilon
            return np.clip(mu / var, -self.cap, self.cap)

        return returns.rolling(window).apply(_kelly, raw=False)

    # ---------------------------------------------------
    # 3. KELLY → RISK CONVERSION
    # ---------------------------------------------------
    def kelly_risk(self, returns):
        kelly = self.raw_kelly(returns)

        # Normalize Kelly to [0, 1]
        kelly_norm = (kelly + self.cap) / (2 * self.cap)

        # Invert to risk
        risk = 1.0 - kelly_norm
        return float(np.clip(risk, 0.0, 1.0))

    # ---------------------------------------------------
    # 4. ROLLING KELLY RISK
    # ---------------------------------------------------
    def rolling_kelly_risk(self, returns, window=50):
        kelly_series = self.rolling_kelly(returns, window)
        return 1.0 - ((kelly_series + self.cap) / (2 * self.cap))
    


    #Kinda estimated sht : 
    """
    final_risk_score = (
    0.25 * volatility_risk +
    0.25 * drawdown_risk +
    0.20 * regime_risk +
    0.15 * kelly_risk +
    0.15 * trend_risk
    ) """

