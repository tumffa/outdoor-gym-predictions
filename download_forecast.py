import numpy as np
import os
import shutil
from datetime import datetime, timedelta
from fmiopendata.wfs import download_stored_query

# Depending on the current time and availability of the model data, adjusting
# the hours below might be necessary to get any data
# Create datetime objects for the specified times IN FINNISH TIME
# Choose day and month for the daily forecast
year = 2024
month = 10
day = 1
hour1 = 0
hour2 = 0
start_time = datetime(year, month, day, hour1, 0, 0)
end_time = datetime(year, month, day+1, hour2, 0, 0)
#convert to UTC
start_time = start_time - timedelta(hours=3)
end_time = end_time - timedelta(hours=3)

# Tapiola, Espoo (next to Hietaniemi)
# BOUNDING BOX (coordinates) bbox = $$c(E 24°44'12"--E 24°51'12"/N 60°12'30"--N 60°09'24")
# from https://boundingbox.klokantech.com/
bbox = "24.76639,60.21111,24.86083,60.34444"

if not os.path.exists("./forecasts"):
    os.makedirs("./forecasts")

# Create new folder or delete all previous /forecasts/DDMM files
folder = f"./forecasts/d{day:02d}m{month:02d}y{year}"
if not os.path.exists(folder):
    os.makedirs(folder)
else:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Iterate over each hour in the specified time range
current_time = start_time
while current_time < end_time:
    next_time = current_time + timedelta(hours=1)
    start_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = next_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    model_data = download_stored_query("fmi::forecast::harmonie::surface::grid",
                                       args=["starttime=" + start_time_str,
                                             "endtime=" + end_time_str,
                                             "bbox=" + bbox])

    latest_run = max(model_data.data.keys())
    print(latest_run)
    data = model_data.data[latest_run]
    # This will download the data to a temporary file, parse the data and delete the file
    data.parse(delete=True)

    valid_times = data.data.keys()
    print(list(valid_times))

    target_level = 10
    target_dataset_name = "surface precipitation amount, rain, convective"

    for time_step in valid_times:
        datasets = data.data[time_step][target_level]
        if target_dataset_name in datasets:
            unit = datasets[target_dataset_name]["units"]
            data_array = datasets[target_dataset_name]["data"]  # Numpy array of the actual data
            print(f"Time: {time_step}, Level: {target_level}, dataset name: {target_dataset_name}, data unit: {unit}")
            print(data_array)
            # Write out to a file named with the current time step
            filename = f"{folder}/precipitation_data_{time_step.strftime('%Y%m%dT%H%M%S')}.csv"
            np.savetxt(filename, data_array, delimiter=",")

    # Move to the next hour
    current_time = next_time