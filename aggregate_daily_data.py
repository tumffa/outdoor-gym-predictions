import pandas as pd

# Load the data
daily_csv_file = "./processed_data/combined_sorted_daily_data.csv"
daily_df = pd.read_csv(daily_csv_file)

# Convert utcdate to datetime
daily_df['utcdate'] = pd.to_datetime(daily_df['utcdate'])

# Extract week of the year, month, and day of the week
daily_df['week_of_year'] = daily_df['utcdate'].dt.isocalendar().week
daily_df['month'] = daily_df['utcdate'].dt.month
daily_df['day_of_week'] = daily_df['utcdate'].dt.weekday  # Monday=0, Sunday=6

# Group by utcdate and area and aggregate the total minutes, sets, and repetitions
aggregated_df = daily_df.groupby(['utcdate', 'area']).agg(
    total_minutes=('usageMinutes', 'sum'),
    total_sets=('sets', 'sum'),
    total_reps=('repetitions', 'sum')
).reset_index()

# Merge the week_of_year, month, and day_of_week columns back into the aggregated DataFrame
aggregated_df = pd.merge(aggregated_df, daily_df[['utcdate', 'week_of_year', 'month', 'day_of_week']].drop_duplicates(), on='utcdate')

# Write the new DataFrame to a CSV file
output_csv_file = "./processed_data/aggregated_daily_data.csv"
aggregated_df.to_csv(output_csv_file, index=False)

# Display the new DataFrame
print(aggregated_df)