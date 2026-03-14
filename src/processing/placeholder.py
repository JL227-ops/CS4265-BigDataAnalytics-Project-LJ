import pandas as pd
import os

pd.set_option('display.max_rows', 20)

def basic_processing(online_csv, exchange_df=None, country_df=None, output_path=None):
    """
    Process and merge multiple data sources, then save as Parquet.

    Parameters:
        online_csv (str): Path to expanded Online Retail CSV.
        exchange_df (pd.DataFrame): Exchange rates DataFrame (optional).
        country_df (pd.DataFrame): Country metadata DataFrame (optional).
        output_path (str): Path to save final Parquet file (optional).

    Returns:
        pd.DataFrame: Merged and processed DataFrame.
    """

    # 1. Load expanded Online Retail
    df = pd.read_csv(online_csv)

    # 2. Merge Exchange Rates
    if exchange_df is not None and 'Currency' in df.columns:
        df = df.merge(exchange_df, on='Currency', how='left')

    # 3. Merge Country Metadata
    if country_df is not None and 'CountryCode' in df.columns:
        df = df.merge(country_df, on='CountryCode', how='left')

    # 4. Basic cleaning
    df = df.drop_duplicates().reset_index(drop=True)

    # 5. Preview
    print("Processed data shape:", df.shape)
    print("First 20 rows:")
    print(df.head(20))

    # 6. Save as Parquet
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_parquet(output_path, index=False)
        print(f"Saved merged dataset as Parquet: {output_path}")

    return df
