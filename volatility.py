import numpy as np
import pandas as pd


class VolatilityRisk:

    def __init__(self, periods_per_year=252, vol_cap=0.5, epsilon=1e-8):
        self.periods_per_year = periods_per_year
        self.vol_cap = vol_cap
        self.epsilon = epsilon

    # ---------------------------------------------------
    # 1. RAW VOLATILITY
    # ---------------------------------------------------
    def raw_volatility(self, returns, annualized=True):
        returns = np.array(returns)

        vol = np.std(returns) + self.epsilon

        if annualized:
            vol *= np.sqrt(self.periods_per_year)

        return float(vol)

    # ---------------------------------------------------
    # 2. ROLLING VOLATILITY (REGIME AWARE)
    # ---------------------------------------------------
    def rolling_volatility(self, returns, window=20, annualized=True):
        returns = pd.Series(returns)
        vol = returns.rolling(window).std() + self.epsilon

        if annualized:
            vol *= np.sqrt(self.periods_per_year)

        return vol

    # ---------------------------------------------------
    # 3. VOLATILITY → RISK CONVERSION
    # ---------------------------------------------------
    def volatility_risk(self, returns):
        vol = self.raw_volatility(returns)

        # Normalize using cap
        risk = vol / (self.vol_cap + self.epsilon)
        return float(np.clip(risk, 0.0, 1.0))

    # ---------------------------------------------------
    # 4. ROLLING VOLATILITY RISK
    # ---------------------------------------------------
    def rolling_volatility_risk(self, returns, window=20):
        vol_series = self.rolling_volatility(returns, window)
        return np.clip(vol_series / (self.vol_cap + self.epsilon), 0.0, 1.0)
