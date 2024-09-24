First download all csv-files:
- Run download_csv.py

To run all data processing files run:
- PROCESS_ALL.py

or

1. Run dataframe.py
2. Run aggregate_hourly_data.py
3. Run weatherdata_preprocess.py
4. Run combine_weather_and_hourly_data.py

For predictions + tests, run:
- predict_hourly_usage_and_validation.py

For weather forecasts:
```bash
pip install fmiopendata
pip install eccodes
```
- Run download_forecast.py to download forecast for a given day and hour range
- Run calc_precipitation_test.py to calculate the precipitation for all day forecasts
