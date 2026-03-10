import requests
import os
import pandas as pd
import time


def download_data(url, save_path, retries=3, delay=5):

    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Data downloaded successfully to: {save_path}")
            return
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All download attempts failed.")
                raise


def expand_data(input_file, output_file, times=1000):

    df = pd.read_excel(input_file)
    df_big = pd.concat([df] * times, ignore_index=True)

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    df_big.to_csv(output_file, index=False)
    print(f"Expanded dataset saved to {output_file}, shape: {df_big.shape}")