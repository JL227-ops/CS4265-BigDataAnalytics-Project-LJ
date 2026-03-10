import sqlite3
import pandas as pd

def save_to_db(csv_file, db_path, table_name="retail_data"):
    """
    Save CSV dataset to SQLite database
    """
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data saved to database: {db_path}")