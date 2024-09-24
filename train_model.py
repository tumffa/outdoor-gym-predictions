from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
import pandas as pd


def train_model():
    # Load the data
    files = ["./processed_data/combined_hourly_processed_espoo_weather.csv", "./processed_data/combined_hourly_processed_helsinkivantaa_weather.csv", "./processed_data/combined_hourly_processed_kumpula_weather.csv"]
    aggregated_df = pd.read_csv(files[0])

    # Filter only Hietaniemi
    aggregated_df = aggregated_df[aggregated_df['area'] == 'Hietaniemi']

    # Convert localtime to datetime
    aggregated_df['localtime'] = pd.to_datetime(aggregated_df['localtime'])

    train_columns = ['week_of_year', 'hour', 'day_of_week', 'precipitation_mm']

    # Prepare the features and target variable for training
    X_train_weather = aggregated_df[train_columns]
    y_train_weather = aggregated_df['total_minutes']

    # Create a polynomial regression model with Ridge regularization (degree=3 for cubic)
    polynomial_degree = 3
    model_weather = Pipeline([
        ('poly_features', PolynomialFeatures(degree=polynomial_degree)),
        ('scaler', StandardScaler()),
        ('ridge_regression', Ridge(alpha=1.0))
    ])

    # Fit the model
    model_weather.fit(X_train_weather, y_train_weather)

    return model_weather
