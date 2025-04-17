from typing import List
import numpy as np

# Define Sharpe Ratio function
def sharpe_ratio(period_returns: List[float], risk_free_return: float = 0.0) -> float:
    if not period_returns:
        raise ValueError("The input period_returns must not be None or an empty list.")
    
    excess_returns = np.array(period_returns) - risk_free_return
    std_dev = np.std(period_returns, ddof=1)
    
    return np.mean(excess_returns) / std_dev if std_dev != 0 else 0  # Avoid division by zero

# Define Maximum Drawdown function
def maximum_drawdown(period_returns: List[float]) -> float:
    # Your function should raise ValueError according to the docstrings
    # Initial and peak asset
    peak = 1
    cur_asset = 1
    
    if not period_returns:
        raise ValueError("period_returns cannot be None or empty.")
    
    if 1 in period_returns:
        raise ValueError("period_returns should not contain 1.")
    
    max_drawdown = 0

    for r in period_returns:
        cur_asset *= (1 + r)  
        peak = max(peak, cur_asset)
        drawdown = (peak - cur_asset) / peak
        max_drawdown = max(max_drawdown, drawdown)

    return -max_drawdown
    
    raise NotImplementedError()