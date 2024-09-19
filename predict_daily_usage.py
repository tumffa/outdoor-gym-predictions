import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline

# Load the data
aggregate_csv_file = "./processed_data/aggregated_daily_data.csv"
aggregated_df = pd.read_csv(aggregate_csv_file)

# Filter only paloheinä
aggregated_df = aggregated_df[aggregated_df['area'] == 'Paloheinä']

# Convert utcdate to datetime
aggregated_df['utcdate'] = pd.to_datetime(aggregated_df['utcdate'])

# Filter data for the years 2022, 2023, and 2024
aggregated_df_filtered = aggregated_df[
    (aggregated_df['utcdate'].dt.year.isin([2022, 2023, 2024]))
]

# Prepare the features and target variable
X = aggregated_df_filtered[['week_of_year', 'day_of_week']]
y = aggregated_df_filtered['total_minutes']

# Create a polynomial regression model with Ridge regularization (degree=3 for cubic)
polynomial_degree = 3
model = Pipeline([
    ('poly_features', PolynomialFeatures(degree=polynomial_degree)),
    ('scaler', StandardScaler()),
    ('ridge_regression', Ridge(alpha=1.0))
])

# Fit the model
model.fit(X, y)

# Predict the total minutes
aggregated_df_filtered['predicted_minutes'] = model.predict(X)

# Clip the predictions to a realistic range (e.g., non-negative values)
aggregated_df_filtered['predicted_minutes'] = aggregated_df_filtered['predicted_minutes'].clip(lower=0)

# Print the model's predictions for weeks = []
for i in range(30, 35):
    print(aggregated_df_filtered[aggregated_df_filtered['week_of_year'] == i])


# Plot the actual vs predicted total minutes with different markers for each day of the week
plt.figure(figsize=(12, 6))

# Actual total minutes
plt.scatter(aggregated_df_filtered['week_of_year'], y, color='blue', label='Actual Total Minutes', alpha=0.5)

# Predicted total minutes for each day of the week
for day in range(7):
    day_mask = aggregated_df_filtered['day_of_week'] == day
    plt.scatter(aggregated_df_filtered[day_mask]['week_of_year'], aggregated_df_filtered[day_mask]['predicted_minutes'], label=f'Predicted Total Minutes (Day {day})', alpha=0.5, marker='o')

plt.xlabel('Week of Year')
plt.ylabel('Total Minutes')
plt.title('Actual vs Predicted Total Minutes (2022-2024)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()