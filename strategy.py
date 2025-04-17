import numpy as np
import evaluator as eval

def run_vn30f1m_strategy(
    df,
    price_col="Close",
    volume_col="Volume",
    SMA_WINDOW_LENGTH=50,
    BB_BOUND=0.02,
    VOLUME=1.5,
    TAKE_PROFIT_THRES_MEAN_REVERSION=10,
    TAKE_PROFIT_THRES_MOMENTUM=10,
    CUT_LOSS_THRES_MEAN_REVERSION=5,
    CUT_LOSS_THRES_MOMENTUM=5,
    initial_balance=1_000_000_000,
    contract_size=1
):
    # Constants
    MULTIPLIER = 100_000
    MARGIN_RATIO = 0.175
    ACCOUNT_RATIO = 0.8
    FEE_POINTS = 0.47

    # Tracking
    balance = initial_balance
    profit_loss = [balance]
    positions = 0
    entry_price = 0
    total_trades = 0
    winning_trades = 0
    losing_trades = 0

    df = df.copy()

    # Run simulation
    for i in range(SMA_WINDOW_LENGTH, len(df)):
        row = df.iloc[i]
        pt = row[price_col]
        required_capital = pt * MULTIPLIER * MARGIN_RATIO / ACCOUNT_RATIO

        # Entry logic
        if pt < row["LowerBB"] and pt < row["SMA50"] * (1 - BB_BOUND):
            positions += contract_size // 2
            entry_price = pt

        elif pt > row["UpperBB"] and pt > row["SMA50"] * (1 + BB_BOUND):
            positions -= contract_size // 2
            entry_price = pt

        if pt > row["Resistance"] and row[volume_col] > VOLUME * row["AvgVolume20"]:
            positions += contract_size // 2
            entry_price = pt

        elif pt < row["Support"] and row[volume_col] > VOLUME * row["AvgVolume20"]:
            positions -= contract_size // 2
            entry_price = pt

        # Exit logic
        exit_trade = False
        pnl = 0

        if positions > 0:
            if pt >= row["SMA50"] or pt >= entry_price + TAKE_PROFIT_THRES_MEAN_REVERSION or pt >= entry_price + TAKE_PROFIT_THRES_MOMENTUM:
                raw_points = pt - entry_price - FEE_POINTS
                pnl = raw_points * MULTIPLIER * (contract_size // 2)
                exit_trade = True
            elif pt < entry_price - CUT_LOSS_THRES_MEAN_REVERSION or pt < entry_price - CUT_LOSS_THRES_MOMENTUM:
                raw_points = pt - entry_price - FEE_POINTS
                pnl = raw_points * MULTIPLIER * (contract_size // 2)
                exit_trade = True

        elif positions < 0:
            if pt <= row["SMA50"] or pt <= entry_price - TAKE_PROFIT_THRES_MEAN_REVERSION or pt <= entry_price - TAKE_PROFIT_THRES_MOMENTUM:
                raw_points = entry_price - pt - FEE_POINTS
                pnl = raw_points * MULTIPLIER * (contract_size // 2)
                exit_trade = True
            elif pt > entry_price + CUT_LOSS_THRES_MEAN_REVERSION or pt > entry_price + CUT_LOSS_THRES_MOMENTUM:
                raw_points = entry_price - pt - FEE_POINTS
                pnl = raw_points * MULTIPLIER * (contract_size // 2)
                exit_trade = True

        if exit_trade:
            balance += pnl
            total_trades += 1
            winning_trades += 1 if pnl > 0 else 0
            losing_trades += 1 if pnl <= 0 else 0
            positions = 0

        profit_loss.append(balance)

    # Metrics
    returns = np.diff(profit_loss) / profit_loss[:-1]
    final_balance = balance
    accum_return_rate = (final_balance / initial_balance) - 1
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    def sharpe_ratio(ret_list, rf=0.0):
        if len(ret_list) < 2:
            return 0
        mean = np.mean(ret_list)
        std = np.std(ret_list)
        return (mean - rf) / std if std > 0 else 0

    def maximum_drawdown(ret_list):
        cum_returns = np.cumprod([1 + r for r in ret_list])
        peak = np.maximum.accumulate(cum_returns)
        drawdown = (cum_returns - peak) / peak
        return np.min(drawdown)

    mdd = maximum_drawdown(returns.tolist())
    sharpe = sharpe_ratio(returns.tolist())

    return {
        "Initial Balance": initial_balance,
        "Final Balance": final_balance,
        "Win Rate": win_rate,
        "Total Trades": total_trades,
        "Winning Trades": winning_trades,
        "Losing Trades": losing_trades,
        "Accumulated Return": accum_return_rate,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": mdd,
        "PnL Over Time": profit_loss,
    }
