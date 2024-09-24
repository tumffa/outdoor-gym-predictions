import os
import pandas as pd

if not os.path.exists("./processed_data"):
    os.makedirs("./processed_data")
    
# Load the data
hourly_csv_file = "./processed_data/combined_sorted_hourly_data.csv"
hourly_df = pd.read_csv(hourly_csv_file)

# Convert utctimestamp to datetime
hourly_df['utctimestamp'] = pd.to_datetime(hourly_df['utctimestamp'])

# Change column name to localtime
hourly_df.rename(columns={'utctimestamp': 'localtime'}, inplace=True)

# Convert to Finnish time
hourly_df['localtime'] = hourly_df['localtime'] + pd.Timedelta(hours=3)

# Format the localtime to 'YYYY-MM-DD HH:MM:SS'
hourly_df['localtime'] = hourly_df['localtime'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Extract week of the year, month, day of the week, and hour of the day
hourly_df['week_of_year'] = pd.to_datetime(hourly_df['localtime']).dt.isocalendar().week
hourly_df['month'] = pd.to_datetime(hourly_df['localtime']).dt.month
hourly_df['day_of_week'] = pd.to_datetime(hourly_df['localtime']).dt.weekday  # Monday=0, Sunday=6
hourly_df['hour'] = pd.to_datetime(hourly_df['localtime']).dt.hour

# Group by localtime and area and aggregate the total minutes, sets, and repetitions
aggregated_df = hourly_df.groupby(['localtime', 'area']).agg(
    total_minutes=('usageMinutes', 'sum'),
    total_sets=('sets', 'sum'),
    total_reps=('repetitions', 'sum')
).reset_index()

# Merge the week_of_year, month, day_of_week, and hour columns back into the aggregated DataFrame
aggregated_df = pd.merge(aggregated_df, hourly_df[['localtime', 'week_of_year', 'month', 'day_of_week', 'hour']].drop_duplicates(), on='localtime')

# Write the new DataFrame to a CSV file
output_csv_file = "./processed_data/aggregated_hourly_data.csv"
aggregated_df.to_csv(output_csv_file, index=False)

# Display the new DataFrame
print(aggregated_df)