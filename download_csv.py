import os
import requests
import gzip
import shutil

# List of file URLs
daily_file_urls = [
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20211001-20211101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20211101-20211201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20211201-20220101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220101-20220201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220201-20220301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220301-20220401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220401-20220501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220501-20220601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220601-20220701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220701-20220801.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220801-20220901.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20220901-20221001.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20221001-20221101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20221101-20221201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20221201-20230101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230101-20230201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230201-20230301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230301-20230401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230401-20230501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230501-20230601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230601-20230701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230701-20230801.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230801-20230901.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20230901-20231001.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20231001-20231101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20231101-20231201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20231201-20240101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240101-20240201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240201-20240301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240301-20240401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240401-20240501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240501-20240601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240601-20240616.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240616-20240701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240701-20240708.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240708-20240715.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240715-20240722.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240722-20240729.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240729-20240805.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240805-20240812.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240812-20240819.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240819-20240826.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240826-20240902.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240902-20240909.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-daily-20240909-20240916.csv.gz"
]
# List of hourly CSV file URLs
hourly_file_urls = [
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20210501-20210601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20210601-20210701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20210701-20210801.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20210801-20210901.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20210901-20211001.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20211001-20211101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20211101-20211201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20211201-20220101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220101-20220201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220201-20220301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220301-20220401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220401-20220501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220501-20220601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220601-20220701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220701-20220801.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220801-20220901.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20220901-20221001.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20221001-20221101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20221101-20221201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20221201-20230101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230101-20230201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230201-20230301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230301-20230401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230401-20230501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230501-20230601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230601-20230701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230701-20230801.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230801-20230901.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20230901-20231001.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20231001-20231101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20231101-20231201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20231201-20240101.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240101-20240201.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240201-20240301.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240301-20240401.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240401-20240501.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240501-20240516.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240516-20240601.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240601-20240616.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240616-20240701.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240701-20240708.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240708-20240715.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240715-20240722.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240722-20240729.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240729-20240805.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240805-20240812.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240812-20240819.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240819-20240826.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240826-20240902.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240902-20240909.csv.gz",
    "https://hkikanslialiikuntapaikat.z6.web.core.windows.net/ulkokuntosali/ulkoliikunta-hourly-20240909-20240916.csv.gz"
]

# Create directories if they don't exist
os.makedirs('./daily_csv', exist_ok=True)
os.makedirs('./hourly_csv', exist_ok=True)

# Function to download and decompress a file
def download_and_decompress_file(url, directory):
    try:
        local_filename = os.path.join(directory, url.split('/')[-1].replace('.gz', ''))
        compressed_filename = local_filename + '.gz'
        
        # Download the file
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(compressed_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Decompress the file
        with gzip.open(compressed_filename, 'rb') as f_in:
            with open(local_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove the compressed file
        os.remove(compressed_filename)
        
        print(f"Downloaded and decompressed: {local_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Download and decompress each daily file
for url in daily_file_urls:
    download_and_decompress_file(url, './daily_csv')

# Download and decompress each hourly file
for url in hourly_file_urls:
    download_and_decompress_file(url, './hourly_csv')
