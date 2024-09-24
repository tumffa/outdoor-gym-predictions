import os
import glob
import numpy as np

def precipitation_by_date(day, month, year):
    folder = f'./forecasts/d{day:02d}m{month:02d}y{year}'
    precipitation = precipitation_by_folder(folder)
    return precipitation

def precipitation_by_folder(folder):
    print(f"\nProcessing day: {folder}")
    # List all CSV files in the directory
    csv_files = glob.glob(os.path.join(folder, '*.csv'))

    # Initialize a dictionary to store precipitation data by hour
    hourly_data = {}
    # Iterate over each CSV file
    for csv_file in csv_files:
        # Extract the hour from the filename
        filename = os.path.basename(csv_file)
        hour_str = filename.split('_')[2]  # Assuming the format is precipitation_data_YYYYMMDDTHHMMSS.csv
        hour = hour_str[:11]  # Extract YYYYMMDDTHH

        # Read the CSV data
        data = np.loadtxt(csv_file, delimiter=',')
        
        # Flatten the data to a 1D array
        flattened_data = data.flatten()
        
        # Convert the data to millimeters (assuming the data is already in kg/m², which is equivalent to mm)
        data_in_mm = flattened_data
        # Add the data to the corresponding hour in the dictionary
        if hour not in hourly_data:
            hourly_data[hour] = []
        hourly_data[hour].extend(data_in_mm)

    # Calculate the average precipitation for each hour
    hourly_averages = {hour: np.mean(values) for hour, values in hourly_data.items()}

    # Note: downloading the data for a given hour seems to give
    # the cumulative amount up to that point since the last model run

    # The raw data is in kg/m² (mm) per grid cell inside the bbox
    # calculating np.mean of the grid values gives the cumulative amount
    # up to that hour. To get the precipitation for the hour, we need to
    # calculate the difference between consecutive hours.

    # Print the average precipitation for each hour
    hourly_precipitation = []
    print("\nAverage precipitation by hour (in mm):")
    hour = sorted(hourly_averages.items())
    for i in range(1, len(hour)):
        hourly_precipitation.append(abs(hour[i][1] - hour[i-1][1]))

    return hourly_precipitation

def main():
    # Directory containing the CSV files
    folder = './forecasts'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Process each day's precipitation data
    for day_folder in os.listdir(folder):
        prec = precipitation_by_folder(os.path.join(folder, day_folder))
        for i in range(len(prec)):
            print(f"Hour {i+1}: {prec[i]:.2f} mm")
        print(f"Total precipitation: {sum(prec):.2f} mm")

if __name__ == "__main__":
    main()