import pandas as pd
import helper

data = pd.read_csv("data.csv")

# Ensure datetime is in datetime format
data['datetime'] = pd.to_datetime(data['datetime'])

# Set datetime as index
data.set_index('datetime', inplace=True)

# Resample to 1-minute intervals
# You can customize what you want to aggregate for each column
data = data.resample('1T').agg({
    'tickersymbol': 'first',  # or maybe mode or last
    'price': 'last',          # closing price of the minute
    'quantity': 'sum'         # total volume in the minute
}).dropna(subset=['price'])   # optional: drop minutes without price

# Reset index if you want datetime back as a column
data = data.reset_index()

data_train_in_sample = helper.compute_indicators(
    data, "in sample data", [2021, 2022], save_path="in_sample_data.csv")
data_train_out_sample = helper.compute_indicators(
    data, "out sample data", [2023], save_path="out_sample_data.csv")

print("In sample data", data_train_in_sample.head(3))
print("Out sample data", data_train_out_sample.head(3))


helper.plot_dataset(data_train_in_sample, "in_sample_data")
helper.plot_dataset(data_train_out_sample, "out_sample_data")
