from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from calc_precipitation_test import precipitation_by_date
import matplotlib.pyplot as plt
import pandas as pd

# Load the data
files = ["./processed_data/combined_hourly_processed_espoo_weather.csv", "./processed_data/combined_hourly_processed_helsinkivantaa_weather.csv", "./processed_data/combined_hourly_processed_kumpula_weather.csv"]
aggregated_df = pd.read_csv(files[0])

# Filter only Hietaniemi
aggregated_df = aggregated_df[aggregated_df['area'] == 'Paloheinä']

# Convert localtime to datetime
aggregated_df['localtime'] = pd.to_datetime(aggregated_df['localtime'])

# Training 2022 and 2023
# test 2024
# summer months
train_df = aggregated_df[(aggregated_df['localtime'].dt.year == 2022) | (aggregated_df['localtime'].dt.year == 2023)]
test_df = aggregated_df[aggregated_df['localtime'].dt.year == 2024]

train_columns = ['week_of_year', 'hour', 'day_of_week', 'temperature_c', 'precipitation_mm']
if 'snow_depth_cm' in aggregated_df.columns:
    train_columns.append('snow_depth_cm')

# Prepare the features and target variable for training
X_train_weather = train_df[train_columns]
y_train_weather = train_df['total_minutes']

X_test_weather = test_df[train_columns]
y_test_weather = test_df['total_minutes']

# Without weather data
X_train = train_df[['week_of_year', 'hour', 'day_of_week']]
y_train = train_df['total_minutes']
X_test = test_df[['week_of_year', 'hour', 'day_of_week']]
y_test = test_df['total_minutes']

# Create a polynomial regression model with Ridge regularization (degree=5 for cubic)
polynomial_degree = 3
model_weather = Pipeline([
    ('poly_features', PolynomialFeatures(degree=polynomial_degree)),
    ('scaler', StandardScaler()),
    ('ridge_regression', Ridge(alpha=1.0))
])
model = Pipeline([
    ('poly_features', PolynomialFeatures(degree=polynomial_degree)),
    ('scaler', StandardScaler()),
    ('ridge_regression', Ridge(alpha=1.0))
])

# Fit the model
model_weather.fit(X_train_weather, y_train_weather)
model.fit(X_train, y_train)

# Make predictions using the testing set
y_pred_weather = model_weather.predict(X_test_weather)

# Calculate and print the mean squared error and R^2 score
mse = mean_squared_error(y_test_weather, y_pred_weather)
r2 = r2_score(y_test_weather, y_pred_weather)
print('Mean Squared Error (with weather): %.2f' % mse)
print('Coefficient of Determination: %.2f' % r2)

# Make predictions without weather data
y_pred = model.predict(X_test)

# Calculate and print the mean squared error and R^2 score
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print('Mean Squared Error (without weather): %.2f' % mse)
print('Coefficient of Determination: %.2f' % r2)

# Train with 2021-2023 and predict 2023
predict_df_weather = aggregated_df[(aggregated_df['localtime'].dt.year == 2023) & (aggregated_df['localtime'].dt.month <= 8)]
X_predict = predict_df_weather[train_columns]
predict_df_weather['predicted_minutes'] = model_weather.predict(X_predict)

predict_df = aggregated_df[(aggregated_df['localtime'].dt.year == 2023) & (aggregated_df['localtime'].dt.month <= 8)]
X_predict = predict_df[['week_of_year', 'hour', 'day_of_week']]
predict_df['predicted_minutes'] = model.predict(X_predict)

# Function to draw plots for given weeks and days. 
# Plot temperature, rainfall, snow depth, actual total minutes, and predicted total minutes.
# Compare to prediction without weather
def plot_weather_and_usage(weeks, days, year):
    for week_number in weeks:
        for day_of_week in days:
            # Filter data for the specified week and day
            week_data_weather = predict_df_weather[(predict_df_weather['week_of_year'] == week_number) &
                                      (predict_df_weather['day_of_week'] == day_of_week) &
                                      (predict_df_weather['localtime'].dt.year == year)]
            week_data = predict_df[(predict_df['week_of_year'] == week_number) &
                                        (predict_df['day_of_week'] == day_of_week) &
                                        (predict_df['localtime'].dt.year == year)]
            
            plt.figure(figsize=(15, 8))
            
            # Plot actual total minutes
            plt.plot(week_data_weather['localtime'], week_data_weather['total_minutes'], color='blue', label='Actual Total Minutes', alpha=0.5)
            
            # Plot predicted total minutes with weather data
            plt.plot(week_data_weather['localtime'], week_data_weather['predicted_minutes'], color='red', label='Predicted Total Minutes', alpha=0.5)

            # Plot prediction without weather
            plt.plot(week_data['localtime'], week_data['predicted_minutes'], color='black', label='Predicted Total Minutes (No Weather)', alpha=0.5)

            # Plot temperature
            plt.plot(week_data_weather['localtime'], week_data_weather['temperature_c'], color='green', label='Temperature (°C)', alpha=0.5)

            # Plot rainfall
            plt.plot(week_data_weather['localtime'], week_data_weather['precipitation_mm']*100, color='orange', label='Rainfall (mm) * 100', alpha=0.5)

            # Plot snow depth
            if 'snow_depth_cm' in week_data_weather.columns:
                plt.plot(week_data_weather['localtime'], week_data_weather['snow_depth_cm']*10, color='purple', label='Snow Depth (cm)', alpha=0.5)

            plt.xlabel('Date and Hour')
            plt.ylabel('Total Minutes')
            plt.title(f'Actual vs Predicted Total Minutes for Week {week_number}, Day {day_of_week}')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.xticks(rotation=45)
            
            # Save the plot with a unique filename
            filename = f'plot_week_{week_number}_day_{day_of_week}.png'
            plt.show()

# Example: Plot predicted hourly usage for multiple weeks and days
weeks = [39]
days = [2]
year = 2024
plot_weather_and_usage(weeks, days, year)