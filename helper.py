import time
import threading
import itertools
import sys
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def loading_spinner(message, stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 2) + "\r")  # Clear line


def plot_dataset(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index.to_pydatetime(),
             df['price'], label='Price', color='blue')

    # Labeling
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title('Price movement of VN30F1M')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_performance(PnL, dates):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, PnL, label="Portfolio Value", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Balance (VND)")
    plt.title("Backtest Performance")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis for better readability
    formatter = FuncFormatter(lambda x, _: f"{x:,.0f}")
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.show()


def plot_comparison(results1, results2, dates):
    PnL_before = results1["PnL Over Time"]
    PnL_after = results2["PnL Over Time"]
    labels = ("Before Tuning", "After Tuning")

    min_len = min(len(PnL_before), len(PnL_after))

    PnL_before = PnL_before[:min_len]
    PnL_after = PnL_after[:min_len]
    dates = dates[:min_len]

    plt.figure(figsize=(12, 6))

    plt.plot(dates, PnL_before, label=labels[0], color="red")
    plt.plot(dates, PnL_after, label=labels[1], color="blue")

    plt.xlabel("Date")
    plt.ylabel("Balance (VND)")
    plt.title("Backtest Performance Comparison")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    formatter = FuncFormatter(lambda x, _: f"{x:,.0f}")
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    plt.show()


def compute_indicators(df, df_name, time_range, price_col="price", volume_col="quantity", save_path=None):
    df['datetime'] = pd.to_datetime(df['datetime'])

    df_train = df[df['datetime'].dt.year.isin(time_range)].copy()
    df_train.set_index("datetime", inplace=True)

    if not isinstance(df_train.index, pd.DatetimeIndex):
        df_train.index = pd.to_datetime(df_train.index)

    df_train["SMA50"] = df_train[price_col].rolling(window=50).mean()
    df_train["SMA20"] = df_train[price_col].rolling(window=20).mean()
    df_train["STD20"] = df_train[price_col].rolling(window=20).std()

    df_train["UpperBB"] = df_train["SMA20"] + 2 * df_train["STD20"]
    df_train["LowerBB"] = df_train["SMA20"] - 2 * df_train["STD20"]

    df_train["Resistance"] = df_train[price_col].rolling(window=30).max()
    df_train["Support"] = df_train[price_col].rolling(window=30).min()

    df_train["AvgVolume20"] = df_train[volume_col].rolling(window=20).mean()

    if save_path:
        dir_name = os.path.dirname(
            save_path) if os.path.dirname(save_path) else "."

        os.makedirs(dir_name, exist_ok=True)

        df_train.to_csv(save_path)
        print(f"{df_name} saved to {save_path}")

    return df_train


def base_param_reset():
    base_result = {
        "value": None,
        "params": {
            "sma_window": 50,
            "tp_mean_rev": 5,
            "tp_momentum": 10,
            "sl_mean_rev": 5,
            "sl_momentum": 4
        }
    }

    with open("original_params.json", "w") as f:
        json.dump(base_result, f, indent=4)
