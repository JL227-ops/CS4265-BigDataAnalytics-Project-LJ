# CS4265 Project - Online Retail Data Pipeline

## Project Description
This project implements a data pipeline for large-scale retail transaction analysis using the Online Retail dataset from UCI.

The goal is to simulate a Big Data analytics workflow by integrating multiple data sources, expanding the dataset to simulate scale, and storing the final dataset in a distributed-friendly format (Parquet).

The pipeline demonstrates key stages of a modern data engineering workflow:

1.Data ingestion
2.Multi-source data integration
3.Data expansion for large-scale simulation
4.Data processing and transformation
5.Columnar storage for analytical workloads

## Data Sources
The pipeline integrates three data sources:
1.Online Retail Dataset (Primary Data Source)
Source: UCI Machine Learning Repository
Contains transactional records including:
InvoiceNo/StockCode/Description/Quantity/InvoiceDate/UnitPrice/CustomerID/Country
Dataset format: Excel (.xlsx)

2.Exchange Rate API
Source: Exchange Rates API
Provides currency exchange rate data, which can be used for currency normalization and financial analysis.
Data format: JSON → converted to CSV
Example fields:
Currency/Rate

3. Country Metadata
Additional dataset containing regional metadata.
Example fields:
CountryCode/Region
Format: CSV
This dataset enriches the retail data with geographic information.

#Data Pipeline Architecture
The pipeline performs the following steps:
1.Download the Online Retail dataset
2.Expand the dataset to simulate larger scale data
3.Fetch exchange rate data from an API
4.Load country metadata
5.Merge all data sources
6.Store the final dataset in Parquet format
The pipeline architecture diagram is included in the docs/ folder.

#Data Flow Diagram
flowchart TD

%% Data Sources
A[Online Retail Dataset<br>UCI Excel]
B[Exchange Rate API<br>JSON]
C[Country Metadata<br>CSV]

%% Step 1 Download
A -->|download_data downloads Excel| D[Raw Data<br>data/raw/online_retail.xlsx]

%% Step 2 Expand
D -->|expand_data replicates dataset x10| E[Expanded Dataset<br>online_retail_expanded.csv]

%% Step 3 Fetch API
B -->|API request returns exchange rates| F[Exchange Rates Data]

%% Step 4 Load Metadata
C -->|load CSV metadata| G[Country Metadata Loaded]

%% Step 5 Merge
E -->|merge datasets| H[Data Processing & Integration]
F --> H
G --> H

%% Step 6 Storage
H -->|save_to_parquet| I[Parquet Storage<br>data/processed/online_retail_full.parquet]

classDef process fill:#f9f,stroke:#333,stroke-width:1px;
class A,B,C,D,E,F,G,H,I process;

#Project Structure
CS4265_Project_Jia_Liu/

config/
    settings.yaml
    .env.example

src/
    ingestion/
        fetch_data.py
    processing/
        placeholder.py
    storage/
        parquet_handler.py
    main.py

data/
    raw/
        online_retail.xlsx
        exchange_rates.json
        exchange_rates.csv
        country_metadata.csv
    processed/
        online_retail_expanded.csv
        online_retail_full.parquet

docs/
    M2DataFlowDiagram.png
    fetch_data_success.png
    data_records.png
    data_processing.png
    parquet_saved.png
    pipeline_output.png

requirements.txt
README.md
.gitignore

#Big Data Simulation
The original Online Retail dataset is relatively small for Big Data analysis.
To simulate larger-scale data processing:
expand_times = 10
The dataset is replicated multiple times to increase the number of records.
This allows testing of the pipeline with larger datasets before implementing distributed processing frameworks in future milestones.

#Storage Format
Instead of SQLite, the pipeline stores the final dataset as Parquet format
Advantages:
Columnar storage
Efficient compression
Optimized for big data tools
Compatible with Spark / Dask / distributed processing
Output file:
data/processed/online_retail_full.parquet

#How to Run the pipeline

1. **Clone the Repository**  
git clone <repository-url>
cd CS4265_Project_Jia_Liu

#Install dependencies
pip install -r requirements.txt

#Run the pipeline
python src/main.py

Pipeline output will include:
-Expanded dataset
-Processed dataset preview
-Parquet dataset saved successfully

#Evidence Screenshots

The docs/ directory contains screenshots demonstrating the execution of the pipeline.
Included evidence:
Successful dataset download
Data processing preview
Sample processed records
Parquet storage confirmation
Full pipeline execution output

#Next Steps (Milestone 3)
Future development will focus on extending the pipeline to support scalable and production-ready data processing.
Planned improvements:
-Implement full data cleaning and validation
-Integrate exchange rate API and country metadata into automated transformations
-Introduce distributed processing using Spark or Dask
-Store processed data in PostgreSQL for structured querying
-Expand documentation and add the pipeline architecture diagram to the README
-Implement automated tests for pipeline modules


#Notes
.venv is excluded via .gitignore
Environment variables are managed through .env.example

#Author
Jia Liu
CS4265 Big Data Analytics Project
Kennesaw States University