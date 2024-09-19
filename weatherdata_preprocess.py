import pandas as pd

# Load the weather data
weather_csv_files = ["espoo_weather.csv", "helsinkivantaa_weather.csv", "kumpula_weather.csv"]

for weather_csv_file in weather_csv_files:
    weather_df = pd.read_csv(f"./weather_data/{weather_csv_file}")

    # Convert the date and time columns to a single datetime column
    if "Aika [Paikallinen aika]" in weather_df.columns:
        weather_df['localtime'] = pd.to_datetime(weather_df[['Vuosi', 'Kuukausi', 'Päivä']].astype(str).agg('-'.join, axis=1) + ' ' + weather_df['Aika [Paikallinen aika]'])
        # Drop the original date and time columns
        weather_df.drop(columns=['Vuosi', 'Kuukausi', 'Päivä', 'Aika [Paikallinen aika]'], inplace=True)
    elif "Aika [UTC]" in weather_df.columns:
        weather_df['localtime'] = pd.to_datetime(weather_df[['Vuosi', 'Kuukausi', 'Päivä']].astype(str).agg('-'.join, axis=1) + ' ' + weather_df['Aika [UTC]'])
        # Drop the original date and time columns
        weather_df.drop(columns=['Vuosi', 'Kuukausi', 'Päivä', 'Aika [UTC]'], inplace=True)

    # Rename the columns for clarity (helsinkivantaa doensnt have snow depth, thus if statement)
    if weather_csv_file == weather_csv_files[0] or weather_csv_file == weather_csv_files[2]:
        weather_df.rename(columns={
            'Havaintoasema': 'station',
            'Ilman lämpötila maksimi [°C]': 'temperature_c',
            'Sademäärä maksimi [mm]': 'precipitation_mm',
            "Lumensyvyys maksimi [cm]" : "snow_depth_cm"
        }, inplace=True)
    else:
        weather_df.rename(columns={
            'Havaintoasema': 'station',
            'Ylin lämpötila [°C]': 'temperature_c',
            'Tunnin sademäärä [mm]': 'precipitation_mm'
        }, inplace=True)

    # Convert values to numeric
    weather_df['temperature_c'] = pd.to_numeric(weather_df['temperature_c'], errors='coerce')
    weather_df['precipitation_mm'] = pd.to_numeric(weather_df['precipitation_mm'], errors='coerce')
    
    if 'snow_depth_cm' in weather_df.columns:
        weather_df['snow_depth_cm'] = pd.to_numeric(weather_df['snow_depth_cm'], errors='coerce')

    # Fill missing values with the average of the closest 3 values
    weather_df['temperature_c'] = weather_df['temperature_c'].interpolate(method='nearest', limit_direction='both')
    weather_df['precipitation_mm'] = weather_df['precipitation_mm'].interpolate(method='nearest', limit_direction='both')
    
    if 'snow_depth_cm' in weather_df.columns:
        weather_df['snow_depth_cm'] = weather_df['snow_depth_cm'].interpolate(method='nearest', limit_direction='both')

    # Save the processed weather data to a new CSV file
    output_csv_file = f"./processed_data/processed_{weather_csv_file}"
    weather_df.to_csv(output_csv_file, index=False)