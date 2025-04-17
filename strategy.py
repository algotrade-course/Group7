import numpy as np
import evaluator as eval

def strategy(
    df,
    SMA_WINDOW_LENGTH,
    TAKE_PROFIT_THRES_MEAN_REVERSION,
    TAKE_PROFIT_THRES_MOMENTUM,
    CUT_LOSS_THRES_MEAN_REVERSION,
    CUT_LOSS_THRES_MOMENTUM,
    initial_balance,
    contract_size,
    price_col="price",
    volume_col="quantity",
    BB_BOUND=0.02,
    VOLUME=1.5,
):

    # Tracking
    balance = initial_balance
    profit_loss = [balance]
    positions = 0
    entry_price = 0

    total_trades = 0
    winning_trades = 0
    losing_trades = 0

    # Run simulation
    for i in range(SMA_WINDOW_LENGTH, len(df)):
        row = df.iloc[i]
        pt = row[price_col]
        vol = row[volume_col]

        # Entry conditions
        if pt < row["LowerBB"] and pt < row["SMA50"] * (1 - BB_BOUND):
            positions += contract_size // 2
            entry_price = pt
        elif pt > row["UpperBB"] and pt > row["SMA50"] * (1 + BB_BOUND):
            positions -= contract_size // 2
            entry_price = pt
        elif pt > row["Resistance"] and vol > VOLUME * row["AvgVolume20"]:
            positions += contract_size // 2
            entry_price = pt
        elif pt < row["Support"] and vol > VOLUME * row["AvgVolume20"]:
            positions -= contract_size // 2
            entry_price = pt

        # Exit and stop-loss
        if positions > 0:  # Long
            if pt >= row["SMA50"] or pt >= entry_price + TAKE_PROFIT_THRES_MEAN_REVERSION:
                profit = (pt - entry_price) * (contract_size // 2)
                balance += profit
                total_trades += 1
                winning_trades += 1 if profit > 0 else 0
                losing_trades += 1 if profit <= 0 else 0
                positions = 0
            elif pt >= entry_price + TAKE_PROFIT_THRES_MOMENTUM:
                profit = (pt - entry_price) * (contract_size // 2)
                balance += profit
                total_trades += 1
                winning_trades += 1 if profit > 0 else 0
                losing_trades += 1 if profit <= 0 else 0
                positions = 0
            elif pt < entry_price - CUT_LOSS_THRES_MEAN_REVERSION or pt < entry_price - CUT_LOSS_THRES_MOMENTUM:
                loss = (CUT_LOSS_THRES_MEAN_REVERSION if pt < entry_price - CUT_LOSS_THRES_MEAN_REVERSION else CUT_LOSS_THRES_MOMENTUM) * (contract_size // 2)
                balance -= loss
                total_trades += 1
                losing_trades += 1
                positions = 0

        elif positions < 0:  # Short
            if pt <= row["SMA50"] or pt <= entry_price - TAKE_PROFIT_THRES_MEAN_REVERSION:
                profit = (entry_price - pt) * (contract_size // 2)
                balance += profit
                total_trades += 1
                winning_trades += 1 if profit > 0 else 0
                losing_trades += 1 if profit <= 0 else 0
                positions = 0
            elif pt <= entry_price - TAKE_PROFIT_THRES_MOMENTUM:
                profit = (entry_price - pt) * (contract_size // 2)
                balance += profit
                total_trades += 1
                winning_trades += 1 if profit > 0 else 0
                losing_trades += 1 if profit <= 0 else 0
                positions = 0
            elif pt > entry_price + CUT_LOSS_THRES_MEAN_REVERSION or pt > entry_price + CUT_LOSS_THRES_MOMENTUM:
                loss = (CUT_LOSS_THRES_MEAN_REVERSION if pt > entry_price + CUT_LOSS_THRES_MEAN_REVERSION else CUT_LOSS_THRES_MOMENTUM) * (contract_size // 2)
                balance -= loss
                total_trades += 1
                losing_trades += 1
                positions = 0

        profit_loss.append(balance)

    final_balance = balance
    returns = np.diff(profit_loss) / profit_loss[:-1]
    total_return = (final_balance - initial_balance) / initial_balance

    sharpe = eval.sharpe_ratio(returns.tolist())
    mdd = eval.maximum_drawdown(returns.tolist())

    accum_return_rate = (final_balance / initial_balance) - 1

    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

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
