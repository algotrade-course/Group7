import time
import itertools
import sys
import pandas as pd
import os
import json
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

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


def plot_performance(NAV, dates):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, NAV, label="Portfolio Value", color="blue")
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
    NAV_before = results1["NAV Over Time"]
    NAV_after = results2["NAV Over Time"]
    labels = ("Before Tuning", "After Tuning")

    min_len = min(len(NAV_before), len(NAV_after))

    NAV_before = NAV_before[:min_len]
    NAV_after = NAV_after[:min_len]
    dates = dates[:min_len]

    plt.figure(figsize=(12, 6))

    plt.plot(dates, NAV_before, label=labels[0], color="red")
    plt.plot(dates, NAV_after, label=labels[1], color="blue")

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

def plot_drawdown_overtime(results, date):
    # Get drawdown over time from results
    drawdown = results["Drawdown Over Time"]
    date = date[:len(drawdown)]

    # Plot the drawdown
    plt.figure(figsize=(12, 6))
    plt.plot(date, drawdown, color='red')
    plt.title("Drawdown Over Time")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (%)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_standardized_minute_returns_distribution(nav_over_time):
    """
    Plot the distribution of standardized (Z-scored) minute returns using Matplotlib.

    Parameters:
    - nav_over_time (list or np.array): NAV values over time (from 'NAV Over Time').
    """
    nav_over_time = np.array(nav_over_time)

    # Handle constant values or overly stable periods by removing duplicates
    nav_over_time = nav_over_time[np.diff(np.insert(nav_over_time, 0, nav_over_time[0])) != 0]

    # Calculate minute returns
    minute_returns = np.diff(nav_over_time) / nav_over_time[:-1]
    
    # Standardize the minute returns
    mean_return = np.mean(minute_returns)
    std_return = np.std(minute_returns)
    if std_return == 0:
        print("Standard deviation is zero, unable to standardize!")
        return
    
    z_returns = (minute_returns - mean_return) / std_return

    # Filter out extreme Z-scores (e.g., beyond ±5)
    z_returns_filtered = z_returns[np.abs(z_returns) < 5]

    # Plot the improved histogram
    plt.figure(figsize=(12, 7))
    plt.hist(z_returns_filtered, bins=150, color='skyblue', edgecolor='black', alpha=0.75)

    plt.axvline(0, color='black', linestyle='-', linewidth=1.5, label='Mean (Z=0)')
    plt.axvline(1, color='gray', linestyle='--', label='+1 STD (Z=1)')
    plt.axvline(-1, color='gray', linestyle='--', label='-1 STD (Z=-1)')

    plt.title("Distribution of Standardized Minute Returns (Z-Score)")
    plt.xlabel("Standardized Minute Return (Z-Score)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_price_vs_nav(df, nav, date_list):
    """
    Plot the comparison between asset price and NAV over time.

    Args:
        df (pd.DataFrame): The DataFrame with price data.
        nav (list): The NAV over time from the strategy.
        date_list (pd.DatetimeIndex): Corresponding dates for NAV.
    """
    # Align the price series with the same date range as NAV
    aligned_prices = df.loc[date_list, "price"]

    plt.figure(figsize=(14, 6))
    plt.plot(date_list, aligned_prices, label="Price", color='blue', alpha=0.6)
    plt.plot(date_list, nav, label="NAV", color='green', linewidth=2)

    plt.xlabel("Datetime")
    plt.ylabel("Value (VND)")
    plt.title("Price vs NAV Over Time")
    plt.legend()
    plt.grid(True)
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
