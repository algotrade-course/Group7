import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_dataset(df_train):
    plt.figure(figsize=(12, 6))
    plt.plot(df_train.index.to_pydatetime(), df_train['price'], label='Price', color='blue')

    # Labeling
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Price movement of {df_train["tickersymbol"].iloc[0]}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_performance(PnL, dates):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, PnL, label="Portfolio Value", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Balance ($)")
    plt.title("Backtest Performance")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis for better readability
    plt.tight_layout()
    plt.show()

def compute_indicators(df, time_range, price_col="price", volume_col="quantity", save_path=None):
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
        dir_name = os.path.dirname(save_path) if os.path.dirname(save_path) else "."

        os.makedirs(dir_name, exist_ok=True)

        if not os.path.exists(save_path):
            df_train.to_csv(save_path) 
        else:
            print(f"File '{save_path}' already exists.")

    return df_train
