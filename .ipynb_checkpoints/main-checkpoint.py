import numpy as np
import matplotlib.pyplot
import pandas as pd
import sys
import os

DRIVERS_FILE = "f1_data/drivers.csv"
DRIVER_STANDINGS_FILE = "f1_data/driver_standings.csv"
RESULTS_FILE = "f1_data/results.csv"
RACES_FILE = "f1_data/races.csv"

def main():
    drivers_df = pd.read_csv(DRIVERS_FILE)
    drivers_standings_df = pd.read_csv(DRIVER_STANDINGS_FILE)
    results_df = pd.read_csv(RESULTS_FILE)
    races_df = pd.read_csv(RACES_FILE)

    drivers_df = drivers_df[["driverId", "forename", "surname"]]

    while True:
        
        first_name = input("Enter first name of driver, or ENTER/RETURN to skip.. ").strip().lower()
        last_name = input("Enter last name of driver: ").strip().lower()

        driver = find_driver(drivers_df, last_name, first_name or None)

        if driver is None:
            print("Unable to find given driver,", last_name.capitalize())
            continue

        print(driver)

        driver_id = driver.iloc[0]["driverId"]
        driver_races = get_driver_races(results_df, driver_id)

        #print(driver_races)
        
        races_id = driver_races["raceId"].to_numpy(dtype=int) # type: ignore
        positions = pd.to_numeric(driver_races["position"], errors='coerce').to_numpy(dtype=float) # type: ignore

        #print(races_id)
        print(positions)
        
        wins = sum(positions == 1)
        podiums = sum(positions <= 3)

        # print("wins:", wins)
        # print("podiums:", podiums)

        win_streak = greatest_win_streak(positions)
        print("Greatest win streak:", win_streak)

        # get driver standings with year
        standings_df = drivers_standings_df.loc[
            (drivers_standings_df['driverId'] == driver_id), ['raceId', 'driverId', 'position', 'wins']
        ]

        standings_df = standings_df.merge(races_df[['raceId', 'year']], on='raceId')

        print(standings_df)
        
        break # end program


        


def find_driver(df, surname: str, forename=None):
    """
    Finds driver from given dataframe, surname, and/or optional forename.
    If forename is given, looks for data with forename AND surname, otherwise search for only surname.
    Will return dataframe if data is found, might return multiple rows.

    Args:
        df - DataFrame to search into
        surname - Surname, or last name of driver to search
        forename (optional) - Forename, or firstname of driver to search

    Returns:
        DataFrame of found data if found, otherwise None
    """
    if forename:
        driver = df.loc[
            (df['forename'].str.lower() == forename.lower()) &
            (df['surname'].str.lower() == surname.lower())
        ]
    else:
        driver = df.loc[
            (df['surname'].str.lower() == surname.lower())
        ]
    
    return driver if not driver.empty else None


def get_driver_races(df, driverId):
    races = df.loc[
        (df['driverId'] == driverId)
    ]
    if races.empty:
        print("Unable to find races with given driverId:", driverId)
        return None
    
    return races


def greatest_win_streak(positions):
    largest = 0
    current = 0

    for pos in positions:
        if np.isnan(pos):
            current = 0

        if pos == 1:
            current += 1

            if current > largest:
                largest = current
        else:
            current = 0

    return largest
            


if __name__ == '__main__':
    main()
