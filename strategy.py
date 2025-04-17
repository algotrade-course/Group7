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
    price_col="price",
    volume_col="quantity",
    BB_BOUND=0.02,
    VOLUME=1.5,
    margin_ratio=0.175,
    ar_ratio=0.8,
    multiplier=100000,
    point_fee=0.47,
):
    contract_margin = 1300 * multiplier * margin_ratio
    required_deposit = contract_margin / ar_ratio

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

        # Entry condition
        if positions == 0 and balance >= required_deposit:
            if pt < row["LowerBB"] and pt < row["SMA50"] * (1 - BB_BOUND):
                positions = 1
                entry_price = pt
            elif pt > row["UpperBB"] and pt > row["SMA50"] * (1 + BB_BOUND):
                positions = -1
                entry_price = pt
            elif pt > row["Resistance"] and vol > VOLUME * row["AvgVolume20"]:
                positions = 1
                entry_price = pt
            elif pt < row["Support"] and vol > VOLUME * row["AvgVolume20"]:
                positions = -1
                entry_price = pt

        # Exit logic
        if positions != 0:
            exit = False
            is_long = positions > 0

            if is_long:
                if pt >= row["SMA50"] or pt >= entry_price + TAKE_PROFIT_THRES_MEAN_REVERSION:
                    exit = True
                elif pt >= entry_price + TAKE_PROFIT_THRES_MOMENTUM:
                    exit = True
                elif pt < entry_price - CUT_LOSS_THRES_MEAN_REVERSION or pt < entry_price - CUT_LOSS_THRES_MOMENTUM:
                    exit = True
            else:  # Short
                if pt <= row["SMA50"] or pt <= entry_price - TAKE_PROFIT_THRES_MEAN_REVERSION:
                    exit = True
                elif pt <= entry_price - TAKE_PROFIT_THRES_MOMENTUM:
                    exit = True
                elif pt > entry_price + CUT_LOSS_THRES_MEAN_REVERSION or pt > entry_price + CUT_LOSS_THRES_MOMENTUM:
                    exit = True

            if exit:
                price_diff = pt - entry_price if is_long else entry_price - pt
                net_points = price_diff - point_fee  # include cost (0.47 for round trip)
                profit_vnd = net_points * multiplier
                profit_percent = profit_vnd / required_deposit

                balance += profit_percent * required_deposit

                total_trades += 1
                if profit_vnd > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1

                positions = 0  # close position
                entry_price = 0

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
