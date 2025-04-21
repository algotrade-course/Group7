import backtesting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Run the backtest
result, PnL, date_list = backtesting.backtesting("data/in_sample_data.csv", "best_trial_result.json", 30000000)

# Get drawdown over time from results
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
plt.show()

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