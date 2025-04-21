import backtesting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import helper

# Run the backtest
result, PnL, date_list = backtesting.backtesting("data/in_sample_data.csv", "best_trial_result.json", 100000000)

helper.plot_standardized_minute_returns_distribution(result["NAV Over Time"])
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