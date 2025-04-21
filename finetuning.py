import optuna
from optuna.samplers import TPESampler
import strategy
import pandas as pd
import json
import optuna.visualization.matplotlib as vis
import matplotlib.pyplot as plt

def optuna_objective(trial):
    df = pd.read_csv("data/in_sample_data.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index("datetime", inplace=True)

    sma_window = trial.suggest_int("sma_window", 30, 100)
    tp_mean_rev = trial.suggest_float("tp_mean_rev", 3, 10, step=0.5)
    tp_momentum = trial.suggest_float("tp_momentum", 5, 15, step=0.5)
    sl_mean_rev = trial.suggest_float("sl_mean_rev", 3, 10, step=0.5)
    sl_momentum = trial.suggest_float("sl_momentum", 2, 8, step=0.5)

    result = strategy.strategy(
        df,
        SMA_WINDOW_LENGTH=sma_window,
        TAKE_PROFIT_THRES_MEAN_REVERSION=tp_mean_rev,
        TAKE_PROFIT_THRES_MOMENTUM=tp_momentum,
        CUT_LOSS_THRES_MEAN_REVERSION=sl_mean_rev,
        CUT_LOSS_THRES_MOMENTUM=sl_momentum,
        initial_balance=40_000_000
    )

    return result["Sharpe Ratio"]

# Store the global study object for reuse
global_study = None

def finetune(n):
    global global_study
    sampler = TPESampler(seed=710)
    study = optuna.create_study(sampler=sampler, direction='maximize')
    study.optimize(optuna_objective, n_trials=n, show_progress_bar=True)

    global_study = study

    print("\nBest trial:")
    print("  Value:", study.best_trial.value)
    print("  Params:")
    for key, value in study.best_trial.params.items():
        print(f"    {key}: {value}")

    save_choice = input(
        "\nDo you want to save this result? The old result will be deleted. (y/n): ").strip().lower()
    if save_choice in ["yes", "y"]:
        result_to_save = {
            "value": study.best_trial.value,
            "params": study.best_trial.params
        }
        with open("best_trial_result.json", "w") as f:
            json.dump(result_to_save, f, indent=4)
        print("Result saved to best_trial_result.json.")
    else:
        print("Result not saved.")

def show_dot_plot():
    global global_study
    if global_study is None:
        print("⚠️  No Optuna study available. Run fine-tuning first.")
        return

    ax = vis.plot_optimization_history(global_study)
    fig = ax.figure
    fig.set_size_inches(12, 6)

    ax.set_ylabel("Sharpe Ratio")
    ax.set_title("Optuna Optimization History")
    fig.tight_layout()

    plt.show()

def menu():
    while True:
        print("\n=== Optuna Fine-Tuning Menu ===")
        print("1. Run fine-tuning")
        print("2. Show dot plot of trials")
        print("3. Back to main menu")

        user_input = input("Enter your choice: ").strip().lower()

        if user_input == "3":
            print("Returning to main menu...")
            return

        elif user_input == "1":
            try:
                trials_num = int(input("Enter the number of trials (Note: ~6s per trial): ").strip())
                finetune(trials_num)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        elif user_input == "2":
            show_dot_plot()
            continue
        else:
            print("Invalid choice. Please try again.")

# Run the menu
# if __name__ == "__main__":
#     menu()
