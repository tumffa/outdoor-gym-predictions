import os
import pandas as pd

# Directory containing the daily CSV files
daily_csv_dir = './daily_csv'
hours_csv_dir = './hourly_csv'

# List to hold individual DataFrames
daily_dataframes = []
hourly_dataframes = []

# Iterate over all daily CSV files in the directory
for filename in os.listdir(daily_csv_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(daily_csv_dir, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # Append the DataFrame to the list
        daily_dataframes.append(df)

# Concatenate all daily DataFrames in the list into a single DataFrame
all_daily_data_df = pd.concat(daily_dataframes, ignore_index=True)
# Sort the combined DataFrame by utcdate and area
all_daily_data_df = all_daily_data_df.sort_values(by=['utcdate', 'area'])

# Display the first few rows of the combined and sorted DataFrame
print(all_daily_data_df.head())

# Optionally, save the combined and sorted DataFrame to a new CSV file
all_daily_data_df.to_csv('./processed_data/combined_sorted_daily_data.csv', index=False)

# Iterate over all hourly CSV files in the directory
for filename in os.listdir(hours_csv_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(hours_csv_dir, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # Append the DataFrame to the list
        hourly_dataframes.append(df)

# Concatenate all hourly DataFrames in the list into a single DataFrame
all_hourly_data_df = pd.concat(hourly_dataframes, ignore_index=True)
# Sort the combined DataFrame by utctimestamp and area
all_hourly_data_df = all_hourly_data_df.sort_values(by=['utctimestamp', 'area'])

# Display the first few rows of the combined and sorted DataFrame
print(all_hourly_data_df.head())

# Optionally, save the combined and sorted DataFrame to a new CSV file
all_hourly_data_df.to_csv('./processed_data/combined_sorted_hourly_data.csv', index=False)