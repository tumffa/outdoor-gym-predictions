import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from train_model import train_model
from calc_precipitation_test import precipitation_by_date


def predict(date):
    # Load the model    
    model = train_model()
    day, month, year = date.day, date.month, date.year
    print(day, month, year)
    precipitation = precipitation_by_date(day, month, year)
    print(len(precipitation))

    # Create a DataFrame with 24 rows, each representing an hour of the day
    week_of_year = date.isocalendar()[1]
    day_of_week = date.weekday()

    df = pd.DataFrame({
        'week_of_year': [week_of_year] * 24,
        'day_of_week': [day_of_week] * 24,
        'hour': range(24),
        'precipitation_mm': precipitation
    })

    # Predict the total minutes for each hour of the day
    df['total_minutes'] = model.predict(df[['week_of_year', 'hour', 'day_of_week', 'precipitation_mm']])
    return df

def plot_predictions(df):
    # Plot the predicted total minutes for each hour of the day
    plt.figure(figsize=(12, 6))
    plt.plot(df['hour'], df['total_minutes'], marker='o', label='Predicted Total Minutes', color='red')
    plt.plot(df['precipitation_mm']*100, marker='o', label='Precipitation (mm) * 100', color='blue')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Minutes')
    plt.title('Predicted Total Minutes for Each Hour of the Day')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    date = dt.datetime(2024, 9, 25)
    df = predict(date)
    plot_predictions(df)