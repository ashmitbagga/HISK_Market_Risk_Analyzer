import numpy as np

from volatility import VolatilityRisk
from kelly_factor import KellyRisk
from drawdown import drawdown_indicator
from trend_strength_indicator import strength  # Backtrader indicator


def main():

    returns = np.array([0.01, -0.005, 0.02, -0.01, 0.015, 0.007, -0.004])
    equity_curve = np.cumprod(1 + returns)

    trend_risk = 0.40

    vol_model = VolatilityRisk(vol_cap=0.4)
    kelly_model = KellyRisk(cap=1.0)

    volatility_risk = vol_model.volatility_risk(returns)
    kelly_risk = kelly_model.kelly_risk(returns)

    drawdown_data = drawdown_indicator(equity_curve)
    drawdown_risk = min(drawdown_data["maximum_drawdown_%"] / 30.0, 1.0)

    final_risk_score = (
        0.30 * volatility_risk +
        0.30 * drawdown_risk +
        0.20 * kelly_risk +
        0.20 * trend_risk
    )

    print("\n===== FINAL RISK BREAKDOWN =====")
    print(f"Volatility Risk : {volatility_risk:.3f}")
    print(f"Drawdown Risk   : {drawdown_risk:.3f}")
    print(f"Kelly Risk      : {kelly_risk:.3f}")
    print(f"Trend Risk      : {trend_risk:.3f}")

    print("\n🔥 FINAL RISK SCORE:", round(final_risk_score, 3))


if __name__ == "__main__":
    main()
