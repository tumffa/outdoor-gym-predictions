import pandas as pd
import matplotlib.pyplot as plt

# Function to plot total minutes for a 24-hour range for a given date
def plot_total_minutes(csv_file, date, area='Paloheinä'):
    # Read the CSV data into a DataFrame
    df = pd.read_csv(csv_file)

    # Pick a specific area
    df = df[df['area'] == area]

    # Ensure the 'localtime' column is in datetime format
    df['localtime'] = pd.to_datetime(df['localtime'])

    # Filter the DataFrame for the given date
    df = df[df['localtime'].dt.date == date]

    # Extract the hour from the 'localtime' column
    df['hour'] = df['localtime'].dt.hour

    # Plot the total minutes for each hour
    plt.figure(figsize=(12, 6))
    plt.plot(df['hour'], df['total_minutes'], marker='o', linestyle='-', color='b', label='Total Minutes')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Minutes')
    plt.title(f'Total Minutes for Each Hour of the Day on {date}')
    plt.xticks(range(24))  # Ensure x-axis has 24 ticks for each hour
    plt.grid(True)
    plt.legend()
    plt.show()

# Example usage
csv_file = './processed_data/aggregated_hourly_data.csv'  # Replace with the path to your CSV file
date = pd.to_datetime('2024-09-26').date()  # Replace with the desired date
plot_total_minutes(csv_file, date)