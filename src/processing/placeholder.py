import pandas as pd

pd.set_option('display.max_rows', 20)

def basic_processing(csv_file):

    df = pd.read_csv(csv_file)


    print("Data shape:", df.shape)
    print("First 20 rows:")
    print(df.head(20))
    return df
