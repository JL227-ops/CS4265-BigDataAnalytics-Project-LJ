# CS4265 Project - Online Retail Data Pipeline

## Project Description
This project implements a data processing pipeline for the UCI Online Retail dataset:  
[https://archive.ics.uci.edu/ml/datasets/online+retail](https://archive.ics.uci.edu/ml/datasets/online+retail)

The pipeline downloads, expands, processes, and stores data in a SQLite database,  
simulating a "Big Data" workflow. It demonstrates key steps in data ingestion, processing, and storage,  
and is designed for learning and experimentation in data engineering.

## Setup Instructions

1. **Clone the Repository**  
git clone <repository-url>
cd CS4265_Project_Jia_Liu

Create a Python Virtual Environment

python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux

Upgrade pip, setuptools, and wheel

pip install --upgrade pip setuptools wheel

Install Dependencies
pip install -r requirements.txt
Environment Setup

No API keys are needed for this project.

Configuration is done via config/settings.yaml. Example:
data_source:
url: "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

paths:
  raw_data: "data/raw/"
  processed_data: "data/processed/"

database:
  db_path: "data/processed/retail.db"

pipeline:
expand_times: 10   # number of times to replicate data for Big Data simulation
Make sure folders data/raw/ and data/processed/ exist, or the script will create them automatically.

#How to Run
Run the main pipeline script:
python src/main.py

This will:

Download online_retail.xlsx to data/raw/.
Expand the dataset to create online_retail_big.csv in data/processed/.
Perform basic processing (prints the first 20 rows).
Save the processed data to data/processed/retail.db (SQLite database).
Print Pipeline completed successfully!.

Current Status
Step	Status
Download raw dataset	-Works
Expand dataset	-Works
Basic processing	-Works (prints 20 rows)
Save to SQLite database	-Works
Advanced processing	⚠ In progress (placeholder)
Analytics/queries	⚠ In progress

#Notes
online_retail_big.csv is stored in data/processed/ to simulate a large dataset for processing.
Processed data is not written to a separate CSV—only previewed and stored in the database.
The pipeline is modular, so you can extend processing/placeholder.py with more transformations.

#Author
Jia Liu
CS4265 Big Data Analytics Project
Kennesaw States University