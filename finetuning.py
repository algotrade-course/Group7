import optuna
from optuna.samplers import TPESampler
import strategy
import pandas as pd
import json

def optuna_objective(trial):
    df = pd.read_csv("in_sample.csv")
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

def finetune(n):
    sampler = TPESampler(seed=710)
    study = optuna.create_study(sampler=sampler, direction='maximize')
    study.optimize(optuna_objective, n_trials=n, show_progress_bar=True)

    print("\nBest trial:")
    print("  Value:", study.best_trial.value)
    print("  Params:")
    for key, value in study.best_trial.params.items():
        print(f"    {key}: {value}")

    save_choice = input("\nDo you want to save this result? The old result will be deleted. (y/n): ").strip().lower()
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

def menu():
    while True:
        user_input = input("\nNumber of trials (Note: ~6s per trial). Type B to go back to main menu: ").strip().lower()

        if user_input in ["b", "back"]:
            print("Returning to main menu...")
            return  # Just return instead of exiting the program

        try:
            trials_num = int(user_input)
            finetune(trials_num)
        except ValueError:
            print("Invalid input. Please enter an integer or 'b' to go back.")

# Run the menu
# if __name__ == "__main__":
#     menu()