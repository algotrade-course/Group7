import pandas as pd
import helper

data = pd.read_csv("df.csv")
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
    data, "in sample data", [2021, 2022], save_path="in_sample.csv")

print("Making out sample data")
data_train_out_sample = helper.compute_indicators(
    data, "out sample data", [2023], save_path="out_sample.csv")

print("In sample data", data_train_in_sample.head(3))
print("Out sample data", data_train_out_sample.head(3))
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
