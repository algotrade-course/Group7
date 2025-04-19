import subprocess
import sys
import pkg_resources

# Ensure pkg_resources is available
try:
    import pkg_resources
except ImportError:
    print("pkg_resources not found. Installing setuptools...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        import pkg_resources
        print("setuptools installed successfully.")
    except Exception as e:
        print(f"Failed to install setuptools: {e}")
        sys.exit(1)

def check_and_install_requirements():
    required = {'matplotlib', 'numpy', 'optuna', 'pandas', 'psycopg-binary'}
    installed = {pkg.key for pkg in pkg_resources.working_set}

    # Find missing packages
    missing = required - installed

    if missing:
        print(f"\nMissing the following required libraries: {', '.join(missing)}")
        install_choice = input("\nWould you like to install them? (y/n): ").strip().lower()
        if install_choice == 'y':
            # Install missing packages
            try:
                print("Installing missing libraries...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
                print("Libraries installed successfully.")
            except subprocess.CalledProcessError:
                print("Failed to install some libraries. Exiting program.")
                sys.exit(1)
        else:
            print("Exiting program.")
            sys.exit(0)
    else:
        print("All required libraries are installed.")

def main_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Initiate all data")
        print("2. Run Finetuning")
        print("3. Run Backtesting")
        print("4. Quit")

        choice = input("Choose an option (1, 2, 3, or 4): ").strip().lower()

        if choice == "1":
            print("Initiating all data...")
            subprocess.run(["python", "data_prep.py"])
        elif choice == "2":
            import finetuning
            finetuning.menu()
        elif choice == "3":
            import backtesting
            backtesting.menu() 
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    # Check and install required libraries
    check_and_install_requirements()
    
    # If everything is fine, show the main menu
    main_menu()