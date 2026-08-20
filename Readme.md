# TrustLens – Seller Behaviour & Customer Trust Analytics Dashboard

## Project Overview

TrustLens is a **Business Intelligence (BI) & Data Analytics Dashboard** that analyzes historical e-commerce marketplace data to identify seller behaviours that influence customer trust over time.

The platform consolidates orders, deliveries, reviews, sellers, customers, and products into a unified analytics system and computes a **Seller Trust Index (STI)** to identify high-performing and high-risk sellers.

### Problem Statement

An e-commerce marketplace tracks seller performance, return requests, and customer review sentiment, but no operational dashboard identifies which seller behaviours consistently reduce customer trust over time.

TrustLens addresses this gap through interactive analytics dashboards and standardized trust metrics.

---

## Key Features

* Marketplace KPI Dashboard
* Seller Performance Analytics
* Delivery Performance Analytics
* Customer Review Analytics
* Seller Trust Index (STI)
* Trust Band Classification
* Interactive Filters
* CSV Export
* SQLite Analytics Database

---

## Technology Stack

| Layer           | Technology    |
| --------------- | ------------- |
| Programming     | Python        |
| Data Processing | Pandas, NumPy |
| Database        | SQLite        |
| Querying        | SQL           |
| Dashboard       | Streamlit     |
| Visualization   | Plotly        |
| Version Control | Git & GitHub  |

---

## Project Structure

```text
TrustLens/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── analytics/
│   └── database/
│
├── dashboard/
│   ├── Home.py
│   └── pages/
│
├── docs/
│   └── PRD.md
│
├── tests/
├── requirements.txt
├── README.md
└── run_pipeline.py
```
---

## Dashboard Modules

### Dashboard Overview

* Total Orders
* Total Sellers
* Average Rating
* Average Delivery Time
* On-Time Delivery Rate
* Seller Trust Index

### Seller Performance

* Seller Ranking
* Seller Comparison
* Completion Rate
* On-Time Delivery Rate

### Delivery Performance

* Delivery Trends
* Delay Analysis
* Category Delivery Analysis

### Customer Reviews

* Rating Distribution
* Review Trends
* Seller Rating Analysis

### Trust Insights

* Trust Score Distribution
* Trust Bands
* High-Risk Sellers

---

## Seller Trust Index (STI)

| Metric           | Weight |
| ---------------- | ------ |
| Average Rating   | 40%    |
| On-Time Delivery | 30%    |
| Completion Rate  | 20%    |
| Review Volume    | 10%    |

**Formula**

```text
STI = (Rating × 0.40)
    + (On-Time Delivery × 0.30)
    + (Completion Rate × 0.20)
    + (Review Volume × 0.10)
```
---

## Dataset Setup

TrustLens uses the Brazilian E-Commerce Public Dataset by Olist.

The complete raw dataset is not stored in this GitHub repository because the CSV files are relatively large.

## Data Processing Pipeline

TrustLens processes the Olist dataset through a structured data pipeline before analytics and dashboard development.

### Processing Stages

1. **Raw Data Ingestion**
   - Loads the Olist CSV datasets from `data/raw/`.
   - Validates the presence of required datasets and columns.

2. **Data Cleaning & Preprocessing**
   - Handles missing values according to dataset-specific rules.
   - Removes duplicate records where applicable.
   - Standardizes column names and data types.
   - Converts timestamp fields into consistent datetime formats.
   - Validates key fields required for joining datasets.

3. **Data Quality Validation**
   - Checks required columns and expected data types.
   - Identifies missing and duplicate records.
   - Validates primary and foreign key relationships.
   - Checks date and numeric field consistency.
   - Records data-quality issues for review.

4. **Processed Data**
   - Cleaned datasets are written to `data/processed/`.
   - Processed data will be used for feature engineering, SQLite database creation, and analytics.

### Data Flow

```text
Olist Raw CSV Files
        ↓
Data Ingestion
        ↓
Schema Validation
        ↓
Data Cleaning
        ↓
Data Quality Validation
        ↓
Processed Datasets
        ↓
Feature Engineering
        ↓
SQLite Database
        ↓
SQL Analytics
        ↓
Streamlit Dashboard

### Dataset Files Required

Place the following CSV files inside:

data/raw/

- olist_customers_dataset.csv
- olist_geolocation_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv
- olist_order_reviews_dataset.csv
- olist_orders_dataset.csv
- olist_products_dataset.csv
- olist_sellers_dataset.csv
- product_category_name_translation.csv

The dataset can be obtained from the Brazilian E-Commerce Public Dataset by Olist.

After downloading the files, place them in the `data/raw/` directory before running the data pipeline.

---

## Setup Instructions

### Clone Repository

bash
git clone https://github.com/kalviumcommunity/SW2627-PandasNumPy-TrustLens.git
cd TrustLens


### Create Virtual Environment

#### Windows

bash
python -m venv .venv
.venv\Scripts\activate


#### macOS / Linux

bash
python3 -m venv .venv
source .venv/bin/activate


### Install Dependencies

bash
pip install -r requirements.txt


### Run Data Pipeline

bash
python run_pipeline.py


### Launch Dashboard

bash
streamlit run dashboard/Home.py


---

## Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**.

Main datasets:

* Orders
* Order Items
* Sellers
* Customers
* Products
* Reviews

---



## Development Roadmap

* [✅] Product Requirements Document (PRD)
* [✅] Low-Fidelity Wireframes
* [✅] Project Setup
* [✅] Dataset Acquisition & Initial Schema Validation
* [✅] Data Cleaning & Preprocessing
* [✅] Data Quality Validation
* [✅] Feature Engineering & Seller Trust Index Calculation
* [✅] SQLite Database
* [✅] SQL Analytics Layer
* [ ] Streamlit Dashboard
* [ ] UI Polishing
* [ ] Testing
* [ ] Final Presentation

---

## Team Members

* **Sathvika Dharani Bhartu**
* **Yashuwant John M Vijay**

---

## Repository Workflow

Each contributor works on a feature branch and submits a Pull Request (PR).

Example:

bash
git checkout -b feature/seller-dashboard
git add .
git commit -m "feat: add seller dashboard"
git push origin feature/seller-dashboard


---

## License

This project is developed for academic and educational purposes.

---

## Current Status

**PRD Approved · Low-Fidelity Design Approved · Project Initialized · Dataset Acquired · Ingestion & Schema Validation Completed · Data Cleaning & Quality Validation **

## Low-Fidelity Design

The low-fidelity wireframes for TrustLens are available here:

**Figma / Design Link:** https://www.figma.com/proto/MdDLx7WbDgd6ix2doYOhS4/Figma-agent-Playground--Community-?page-id=7%3A2&node-id=1035347-3052&p=f&viewport=-744%2C79%2C0.24&t=67RpHkRW4L7VW9sN-1&scaling=min-zoom&content-scaling=fixed&starting-point-node-id=1035347%3A1853&show-proto-sidebar=1


The wireframes include:
- Dashboard Overview
- Seller Performance
- Delivery Performance
- Customer Reviews
- Trust Insights


