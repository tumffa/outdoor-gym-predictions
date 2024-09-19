# take processed_weather_data.csv and aggregated_hourly_data.csv and combine them into one file

import pandas as pd
import numpy as np

# read in the data
files = ["processed_espoo_weather.csv", "processed_helsinkivantaa_weather.csv", "processed_kumpula_weather.csv"]
for file in files:
    weather_data = pd.read_csv(f"./processed_data/{file}")
    hourly_data = pd.read_csv('./processed_data/aggregated_hourly_data.csv')

    # drop the station column from weather_data
    weather_data = weather_data.drop(columns=['station'])

    # merge the data
    combined_data = pd.merge(weather_data, hourly_data, on='localtime')

    # Save the combined data to a new CSV file
    output_csv_file = f"./processed_data/combined_hourly_{file}"
    combined_data.to_csv(output_csv_file, index=False)

    # Display the combined DataFrame
    print(combined_data)