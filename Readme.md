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

| Layer           | Technology    |
| --------------- | ------------- |
| Programming     | Python        |
| Data Processing | Pandas, NumPy |
| Database        | SQLite        |
| Querying        | SQL           |
| Dashboard       | Streamlit     |
| Visualization   | Plotly        |
| Version Control | Git & GitHub  |

---

## Project Structure

```text
TrustLens/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── analytics/
│   └── database/
│
├── dashboard/
│   ├── Home.py
│   └── pages/
│
├── docs/
│   └── PRD.md
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

| Metric           | Weight |
| ---------------- | ------ |
| Average Rating   | 40%    |
| On-Time Delivery | 30%    |
| Completion Rate  | 20%    |
| Review Volume    | 10%    |

**Formula**

```text
STI = (Rating × 0.40)
    + (On-Time Delivery × 0.30)
    + (Completion Rate × 0.20)
    + (Review Volume × 0.10)
```