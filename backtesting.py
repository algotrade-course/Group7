import pandas as pd
import helper
import threading
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
            if key != "NAV Over Time" and key != "Drawdown Over Time":
                print(f"{key}: {value}")

    NAV = results1["NAV Over Time"]
    DD_overtime = results1["Drawdown Over Time"]
    date_list = df.index[int(params["sma_window"]) - 1:]

    return results1, NAV, date_list

def menu():
    while True:
        # Sample type selection menu
        print("\n--- Select Sample Type ---")
        print("1. In-sample testing")
        print("2. Out-of-sample testing")
        print("3. Back to main menu")
        print("4. Quit")

        sample_choice = input("Enter your choice (1-4): ").strip().lower()

        if sample_choice == "1":
            sample = "data/in_sample_data.csv"
        elif sample_choice == "2":
            sample = "data/out_sample_data.csv"
        elif sample_choice == "3":
            print("Returning to main menu...")
            return
        elif sample_choice == "4":
            print("Exiting program.")
            exit()
        else:
            print("Invalid choice. Please try again.")
            continue

        # Main menu for parameter selection
        while True:
            print(f"\n--- Backtesting Menu ({sample}) ---")
            print("1. Execute on the original parameters")
            print("2. Execute on the optimized parameters")
            print("3. plot the different of original vs optimized backtesting")
            print("4. Go back")
            print("5. Quit")

            choice = input("Enter your choice (1-5): ").strip().lower()

            if choice == "1":
                file_path = "original_params.json"
            elif choice == "2":
                file_path = "best_trial_result.json"
            elif choice == "3":
                try:
                    initial_balance = float(input("Enter the initial balance in VND (>30000000 is recommended for better results): ").strip())
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
            elif choice == "5":
                print("Exiting program.")
                exit()
            else:
                print("Invalid choice. Please try again.")
                continue

            try:
                initial_balance = float(input("Enter the initial balance in VND (>30000000 is recommended for better results): ").strip())
            except ValueError:
                print("Invalid input for initial balance. Please enter a numeric value.")
                continue

            # Run the strategy
            result, NAV, date_list = backtesting(sample, file_path=file_path, initial_balance=initial_balance)

            # Ask to see the chart
            while True:
                print("1. View the Net Asset Value (NAV) over time graph")
                print("2. View the Drawdown over time graph")
                print("3. View standardized minutely returns distribution")
                print("4. Go back")
                print("5. Quit")

                plot_choice = input("Enter your choice (1-5): ").strip().lower()

                if plot_choice == "1":
                    helper.plot_performance(NAV, date_list)
                elif plot_choice == "2":
                    helper.plot_drawdown_overtime(result, date_list)
                elif plot_choice == "3":
                    helper.plot_standardized_minute_returns_distribution(result["NAV Over Time"])
                elif plot_choice == "4":
                    break
                elif plot_choice == "5":
                    print("Exiting program.")
                    exit()


# Run the menu
# if __name__ == "__main__":
#     menu()