# src/storage/parquet_handler.py

import pandas as pd
from pathlib import Path

def save_to_parquet(df, output_path):
    """
    Save dataframe to parquet
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(output_path, index=False)

    print(f"Parquet file saved at {output_path}, shape={df.shape}")
