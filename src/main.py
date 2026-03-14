# src/main.py

import os
import json
import pandas as pd
from pathlib import Path
import yaml
import requests

from ingestion.fetch_data import download_data
from storage.db_handler import save_to_parquet


# -----------------------
# Load configuration
# -----------------------
def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)


def main():

    config = load_config()

    raw_dir = config["paths"]["raw_data"]
    processed_dir = config["paths"]["processed_data"]
    expand_times = config["pipeline"]["expand_times"]
    parquet_path = config["pipeline"]["output_path"]

    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    Path(processed_dir).mkdir(parents=True, exist_ok=True)

    # Online Retail

    online_source = config['data_sources'][0]

    online_path = os.path.join(raw_dir, "online_retail.xlsx")

    if not os.path.exists(online_path):
        print("Downloading Online Retail dataset...")
        download_data(online_source['url'], online_path)
    else:
        print(f"Online Retail dataset already exists at {online_path}")

    online_df = pd.read_excel(online_path)
    online_big = pd.concat([online_df]*expand_times, ignore_index=True)

    for col in ['InvoiceNo', 'CustomerID', 'StockCode', 'Description', 'Country']:
        if col in online_big.columns:
           online_big[col] = online_big[col].astype(str)

    for col in ['UnitPrice', 'Quantity']:
        if col in online_big.columns:
           online_big[col] = pd.to_numeric(online_big[col], errors='coerce')
        

    online_csv = os.path.join(processed_dir, "online_retail_expanded.csv")
    Path(processed_dir).mkdir(parents=True, exist_ok=True)
    online_big.to_csv(online_csv, index=False)

    print(f"Expanded dataset saved to {online_csv}, shape={online_big.shape}")

    #Exchange Rate API

    exchange_source = config['data_sources'][1]

    exchange_json = os.path.join(raw_dir, "exchange_rates.json")
    exchange_csv = os.path.join(raw_dir, "exchange_rates.csv")

    exchange_df = pd.DataFrame(columns=["Currency","Rate"])

    try:

        print("Fetching Exchange Rate API data...")

        response = requests.get(exchange_source['url'], timeout=10)

        response.raise_for_status()

        data = response.json()

        with open(exchange_json,"w") as f:
            json.dump(data,f,indent=2)

        if "rates" in data:

            exchange_df = pd.DataFrame(
                data["rates"].items(),
                columns=["Currency","Rate"]
            )

            exchange_df.to_csv(exchange_csv,index=False)

            print(f"Exchange rates saved: {exchange_csv}")

        else:

            print("API missing rates, using fallback")

            if os.path.exists(exchange_csv):

                exchange_df = pd.read_csv(exchange_csv)

            else:

                exchange_df = pd.DataFrame([
                    ("USD",1.12),
                    ("GBP",0.86),
                    ("EUR",1.0),
                    ("JPY",146.25),
                    ("CNY",7.89)
                ],columns=["Currency","Rate"])

                exchange_df.to_csv(exchange_csv,index=False)

    except Exception as e:

        print("Exchange API failed:",e)

        if os.path.exists(exchange_csv):

            exchange_df = pd.read_csv(exchange_csv)

        else:

            exchange_df = pd.DataFrame([
                ("USD",1.12),
                ("GBP",0.86),
                ("EUR",1.0),
                ("JPY",146.25),
                ("CNY",7.89)
            ],columns=["Currency","Rate"])

    #  Country Metadata

    country_path = os.path.join(raw_dir,"country_metadata.csv")

    if os.path.exists(country_path):
        country_df = pd.read_csv(country_path)
        # rename column to match Online Retail dataset
        country_df = country_df.rename(columns={
            "CLDR display name": "Country",
            "ISO4217-currency_alphabetic_code": "Currency"
        })

        print(f"Country metadata loaded from {country_path}")
    else:

        print("Country metadata not found")

        country_df = pd.DataFrame(columns=["Country","Currency"])

    #Merge Sources

    print("Online columns:",online_big.columns)
    print("Country columns:",country_df.columns)
    print("Exchange columns:",exchange_df.columns)

    merged_df = online_big.merge(
        country_df,
        on="Country",
        how="left"
    )

    if "Currency" in merged_df.columns:

        merged_df = merged_df.merge(
            exchange_df,
            on="Currency",
            how="left"
        )

    else:

        print("Currency column missing, skip exchange merge")

    #Save Parquet

    save_to_parquet(merged_df,parquet_path)

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()
