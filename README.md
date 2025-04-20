# Group7

# Data

The data using in this project is tick data of VN30F1M from 2020-12-18 to 2023-12-21. After being collected from the Algotrade database, the data is aggregated to time interval of 1 minute.

## Data collection

- The tick price and quantity of VN30F1M are collected from Algotrade database using SQL queries.
- The file query.py contains the function to get the data and save the data to a csv file at the path <DATA_PATH>/data/data.csv

**Figure 1: Full Data Graph**

![Full data](graph/data.png)

## Data processing

- The data will be aggregated into minute data. Then it will be splited into in_sample_data and out_sample_data. The in_sample_data will contain data from 2021 to 2022, and out_sample data will contain data in 2023.
- The in_sample_data and out_sample_data are stored in <DATA_PATH>/data/in_sample_data.csv and <DATA_PATH>/data/out_sample_data.csv

**Figure 2: In Sample Data Graph**

![Full data](graph/in_sample_data.png)

**Figure 3: Out Sample Data Graph**

![Full data](graph/out_sample_data.png)

# Implementation

**Requirements:** This implementation requires `pip` to work properly

## Clone project's repository

```bash
git clone https://github.com/algotrade-course/Group7.git
cd Group7
```

## Set up Python virtual environment

**1. Create the virtual environment**
```bash
python -m venv myenv 
```

**2. Activate the virtual environment**

- For Windows:
```bash
myenv\Scripts\activate
```

- For Linux/MacOS:
```bash
source myenv/bin/activate
```

## Start application

**1. Start the program**
```bash
python main.py
```

**2. Libraries**
If you do not have the requisite libraries needed for this application, it will ask you to install those libraries. Here is an example:
```
Missing the following required libraries: numpy, matplotlib, optuna, psycopg-binary, pandas

Would you like to install them? (y/n):
```
Enter `y` will automatically install all the required libraries and proceed to the main menu.

**3. The main menu**
- Enter `1` will initiate all the data needed for future simulation and optimization. This will include initiating the dataset, in sample data, out of sample data, and delete the currently saved optimized simulation values.
- Enter `2` will take the user to the Fine tune section.
- Enter `3` will take the user to the Backtesting section.
- Enter `4` to quit the program.
```
=== MAIN MENU ===
1. Initiate all data (recommended before finetuning and backtesting)
2. Run Finetuning
3. Run Backtesting
4. Quit
Choose an option (1-4):
```