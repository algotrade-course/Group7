import backtesting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import helper
import pandas as pd

# Run the backtest
df_temp = pd.read_csv("data/in_sample_data.csv")
df_temp['datetime'] = pd.to_datetime(df_temp['datetime'])
df_temp.set_index("datetime", inplace=True)
df_temp["price"] *= 100_000
initial_balance = df_temp["price"].iloc[0]
result, NAV, date_list = backtesting.backtesting("data/in_sample_data.csv", "best_trial_result.json", initial_balance)

helper.plot_price_vs_nav(df_temp, NAV, date_list)




# helper.plot_standardized_minute_returns_distribution(result["NAV Over Time"])
# with open("output.txt", "w") as f:
#     print(result["NAV Over Time"], file=f)
'''# Get drawdown over time from results
drawdown = result["Drawdown Over Time"]
date_list = date_list[:len(drawdown)]

# Plot the drawdown
plt.figure(figsize=(12, 6))
plt.plot(date_list, drawdown, color='red')
plt.title("Drawdown Over Time")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()'''

# Old plot option in backtesting.py code
'''
            see_chart = input("\nDo you want to see the PnL over time graph? (y/n): ").strip().lower()
            if see_chart == "y":
                helper.plot_performance(PnL, date_list)

            see_chart = input("\nDo you want to see the Drawdown over time graph? (y/n): ").strip().lower()
            if see_chart == "y":
                helper.plot_drawdown_overtime(result, date_list)

            # Wait for user to go back or quit
            back = input("\nPress B to go back, or Q to quit: ").strip().lower()
            while back not in ["b", "q"]:
                back = input("Invalid input. Press B to go back to the menu, or Q to quit: ").strip().lower()
            if back == "q":
                print("Exiting program.")
                exit()
'''

# Old optuna trial menu
'''
    while True:
        user_input = input(
            "\nEnter the number of trials (Note: ~6s per trial) or type B to go back to main menu: ").strip().lower()

        if user_input in ["b", "back"]:
            print("Returning to main menu...")
            return  # Just return instead of exiting the program

        try:
            trials_num = int(user_input)
            finetune(trials_num)
        except ValueError:
            print("Invalid input. Please enter an integer or 'b' to go back.")
'''

# Old README draft
'''
## Data collection

- The tick price and quantity of VN30F1M are collected from a private database using SQL queries, then was uploaded to a public Google Drive link.
- The file query.py contains the function to download the data from the Google Drive link and save it to a csv file at the path <DATA_PATH>/data/data.csv

**Figure 1: Full Data Graph**

![full_data](graph/data.png)

## Data processing

- The data will be aggregated into minute data. Then it will be splited into in_sample_data and out_sample_data. The in_sample_data will contain data from 2021 to 2022, and out_sample data will contain data in 2023.
- The in_sample_data and out_sample_data are stored in <DATA_PATH>/data/in_sample_data.csv and <DATA_PATH>/data/out_sample_data.csv

**Figure 2: In Sample Data Graph**

![in_sample_data](graph/in_sample_data.png)

**Figure 3: Out Sample Data Graph**

![out_sample_data](graph/out_sample_data.png)

## Testing

The default parameters are as follows:

```
{
    "value": null,
    "params": {
        "sma_window": 50,
        "tp_mean_rev": 5,
        "tp_momentum": 10,
        "sl_mean_rev": 5,
        "sl_momentum": 4
    }
}
```

### In sample backtesting

The testing result with default parameters and the initial balance of 40,000,000VND:

```
Initial Balance: 40000000.0
Final Balance: 341921999.99999994
Win Rate: 83.33333333333334
Total Trades: 144
Winning Trades: 120
Losing Trades: 24
Accumulated Return: 7.548049999999998
Sharpe Ratio: 0.013550733578558087
Annualized Sharpe Ratio: 3.5205838556838356
Max Drawdown: -0.1457418178661343
```

**Figure 4: The PnL value over time**

![in_sample_default_PnL](graph/in_sample_original_PnL.png)

**Figure 5: The Drawdown value over time**

![in_sample_default_Drawdown](graph/in_sample_original_drawdown.png)

**Figure 6: The Distribution of standardized minute returns (Z-Score)**

![in_sample_default_Drawdown](graph/in_sample_original_zscore.png)

### Out sample backtesting

The testing result with default parameters and the initial balance of 40,000,000VND:

```
Initial Balance: 40000000.0
Final Balance: 105258000.00000004
Win Rate: 93.47826086956522
Total Trades: 46
Winning Trades: 43
Losing Trades: 3
Accumulated Return: 1.631450000000001
Sharpe Ratio: 0.019119642119491697
Annualized Sharpe Ratio: 4.9674287360240275
Max Drawdown: -0.015752822662429847
```

**Figure 7: The PnL value over time**

![out_sample_default_PnL](graph/out_sample_original_PnL.png)

**Figure 8: The Drawdown value over time**

![in_sample_default_Drawdown](graph/out_sample_original_drawdown.png)

**Figure 9: The Distribution of standardized minute returns (Z-Score)**

![in_sample_default_Drawdown](graph/out_sample_original_zscore.png)

## Finetuning

After using in-sample data on finetuning with 100 trial and the initial balance of 40,000,000VND, the optimized parameters are:

```
{
    "value": 0.014838635780793847,
    "params": {
        "sma_window": 64,
        "tp_mean_rev": 10.0,
        "tp_momentum": 12.0,
        "sl_mean_rev": 6.5,
        "sl_momentum": 7.5
    }
}
```

**Figure 10: The Optuna trials**

![in_sample_diff](graph/optuna-trials.png)

**Figure 11: The PnL value over time different on in sample data**

![in_sample_diff](graph/in_sample_diff.png)

**Figure 12: The PnL value over time different on out sample data**

![in_sample_diff](graph/out_sample_diff.png)

**Figure 13: The Drawdown value over time with optimized parameters on in sample data**

![in_sample_diff](graph/in_sample_optimized_drawdown.png)

**Figure 14: The Drawdown value over time with optimized parameters on out sample data**

![in_sample_diff](graph/out_sample_optimized_drawdown.png)

**Figure 15: The Distribution of standardized minute returns (Z-Score) with optimized parameters on in sample data**

![in_sample_diff](graph/in_sample_optimized_zscore.png)

**Figure 16: The Distribution of standardized minute returns (Z-Score) with optimized parameters on out sample data**

![in_sample_diff](graph/out_sample_optimized_zscore.png)

'''