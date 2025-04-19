import pandas as pd
import helper
from helper import threading
import optuna
from optuna.samplers import TPESampler
import strategy
import json

def backtesting(sample, file_path, initial_balance, verbose=True):
    # Read the dataset for in sample testing
    df = pd.read_csv(sample)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index("datetime", inplace=True)

    # Load best parameters from saved JSON
    with open(file_path, "r") as f:
        saved_trial = json.load(f)

    # Extract parameters
    params = saved_trial["params"]

    # Start loading spinner
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=helper.loading_spinner, args=(f"Running backtest on {sample} with {file_path}", stop_event))
    spinner_thread.start()

    try:
        results1 = strategy.strategy(
            df,
            SMA_WINDOW_LENGTH=int(params["sma_window"]),
            TAKE_PROFIT_THRES_MEAN_REVERSION=float(params["tp_mean_rev"]),
            TAKE_PROFIT_THRES_MOMENTUM=float(params["tp_momentum"]),
            CUT_LOSS_THRES_MEAN_REVERSION=float(params["sl_mean_rev"]),
            CUT_LOSS_THRES_MOMENTUM=float(params["sl_momentum"]),
            initial_balance=initial_balance,
        )
    finally:
        # Stop spinner
        stop_event.set()
        spinner_thread.join()

    # Print results
    if verbose:
        for key, value in results1.items():
            if key != "PnL Over Time":
                print(f"{key}: {value}")

    PnL = results1["PnL Over Time"]
    date_list = df.index[int(params["sma_window"]) - 1:]

    return results1, PnL, date_list

def menu():
    while True:
        # Sample type selection menu
        print("\n--- Select Sample Type ---")
        print("1. In-sample testing")
        print("2. Out-of-sample testing")
        print("Q. Quit")

        sample_choice = input("Enter your choice (1, 2, or Q): ").strip().lower()

        if sample_choice == "1":
            sample = "in_sample.csv"
        elif sample_choice == "2":
            sample = "out_sample.csv"
        elif sample_choice == "q":
            print("Exiting program.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or Q.")
            continue

        # Main menu for parameter selection
        while True:
            print(f"\n--- Backtesting Menu ({sample}) ---")
            print("1. Execute on the original parameters")
            print("2. Execute on the optimized parameters")
            print("3. plot the different of original vs optimized backtesting")
            print("4. Go back")
            print("Q. Quit")

            choice = input("Enter your choice (1, 2, 3, or Q): ").strip().lower()

            if choice == "1":
                file_path = "original_params.json"
            elif choice == "2":
                file_path = "best_trial_result.json"
            elif choice == "3":
                try:
                    initial_balance = float(input("Enter the initial balance in VND (e.g., 100000): ").strip())
                except ValueError:
                    print("Invalid input for initial balance. Please enter a numeric value.")
                    continue

                # Run both strategies
                result1, _, date_list = backtesting(sample, "original_params.json", initial_balance, verbose=False)
                result2, _, _ = backtesting(sample, "best_trial_result.json", initial_balance, verbose=False)

                # Plot comparison
                helper.plot_comparison(result1, result2, date_list)

                # Wait for user to go back or quit
                back = input("\nPress B to go back, or Q to quit: ").strip().lower()
                while back not in ["b", "q"]:
                    back = input("Invalid input. Press B to go back to the menu, or Q to quit: ").strip().lower()
                if back == "q":
                    print("Exiting program.")
                    return
                continue
            elif choice == "4":
                break
            elif choice == "q":
                print("Exiting program.")
                return
            else:
                print("Invalid choice. Please enter 1, 2, 3, or Q.")
                continue

            try:
                initial_balance = float(input("Enter the initial balance in VND (e.g., 100000): ").strip())
            except ValueError:
                print("Invalid input for initial balance. Please enter a numeric value.")
                continue

            # Run the strategy
            _, PnL, date_list = backtesting(sample, file_path=file_path, initial_balance=initial_balance)

            # Ask to see the chart
            see_chart = input("\nDo you want to see the PnL over time graph? (y/n): ").strip().lower()
            if see_chart == "y":
                helper.plot_performance(PnL, date_list)

            # Wait for user to go back or quit
            back = input("\nPress B to go back, or Q to quit: ").strip().lower()
            while back not in ["b", "q"]:
                back = input("Invalid input. Press B to go back to the menu, or Q to quit: ").strip().lower()
            if back == "q":
                print("Exiting program.")
                return

# Run the menu
if __name__ == "__main__":
    menu()