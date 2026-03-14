# src/ingestion/fetch_data.py

import requests

def download_data(url, save_path):
    """
    Download data from a URL and save to local path
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded file to {save_path}")

    except Exception as e:
        print(f"Download failed: {e}")
