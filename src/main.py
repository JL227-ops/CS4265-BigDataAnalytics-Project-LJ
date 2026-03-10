import os
import yaml
from ingestion.fetch_data import download_data, expand_data
from storage.db_handler import save_to_db
from processing.placeholder import basic_processing

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    url = config["data_source"]["url"]
    raw_path = os.path.join(config["paths"]["raw_data"], "online_retail.xlsx")
    big_path = os.path.join(config["paths"]["processed_data"], "online_retail_big.csv")
    db_path = config["database"]["db_path"]
    expand_times = config["pipeline"]["expand_times"]

    print("Downloading dataset...")
    download_data(url, raw_path)

    print("Expanding dataset to simulate Big Data...")
    expand_data(raw_path, big_path, times=expand_times)

    print("Processing data...")
    basic_processing(big_path)

    print("Saving to database...")
    save_to_db(big_path, db_path)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
