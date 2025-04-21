import os
import pandas as pd
import helper
import json

# Check if data.csv exists, if not, run query.py to create it
if not os.path.exists("data/data.csv"):
    import subprocess
    print("data not found. Running query.py to generate it...")
    subprocess.run(["python", "query.py"], check=True)

data = pd.read_csv("data/data.csv")
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

data = data.resample('1T').agg({
    'tickersymbol': 'first',
    'price': 'last',
    'quantity': 'sum'
}).dropna(subset=['price'])

data = data.reset_index()

print("Making in sample data")
data_train_in_sample = helper.compute_indicators(
    data, "in sample data", [2021, 2022], save_path="data/in_sample_data.csv")

print("Making out sample data")
data_train_out_sample = helper.compute_indicators(
    data, "out sample data", [2023], save_path="data/out_sample_data.csv")

print("In sample data\n", data_train_in_sample.head(3))
print("Out sample data\n", data_train_out_sample.head(3))

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

with open("best_trial_result.json", "w") as f:
    json.dump(base_result, f, indent=4)

1
while True:
    print("\nMenu:")
    print("1. View In-Sample Data")
    print("2. View Out-of-Sample Data")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        print("\nIn-Sample Data:")
        print(data_train_in_sample.head(10))
        helper.plot_dataset(data_train_in_sample)
    elif choice == '2':
        print("\nOut-of-Sample Data:")
        print(data_train_out_sample.head(10))
        helper.plot_dataset(data_train_out_sample)
    elif choice == '3':
        print("Exiting.")
        break
    else:
        print("Invalid choice. Please try again.")
