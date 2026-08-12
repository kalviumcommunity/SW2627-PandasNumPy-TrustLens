# TrustLens Dataset Documentation

## 1. Dataset Overview

TrustLens uses the **Brazilian E-Commerce Public Dataset by Olist** as the primary source for historical e-commerce marketplace data.

The dataset contains information about customers, sellers, products, orders, order items, payments, reviews, and product categories.

The dataset is suitable for TrustLens because it provides the relationships required to analyze seller behaviour, delivery performance, customer ratings, and marketplace activity.

TrustLens combines multiple Olist datasets into an analytics layer that enables the calculation of seller-level performance metrics and the Seller Trust Score.

### Dataset Name

**Brazilian E-Commerce Public Dataset by Olist**

### Primary Use

The dataset is used to analyze:

* Seller performance
* Order volume
* Delivery performance
* Delivery delays
* Customer review ratings
* Product categories
* Seller location
* Customer location
* Seller-level trust indicators
* Historical changes in seller performance

### Dataset Type

Historical structured e-commerce transaction data.

### Data Format

CSV

### Primary Processing Technologies

* Python
* Pandas
* NumPy
* SQL
* SQLite

### Dashboard Technologies

* Streamlit
* Plotly

---

# 2. Dataset Files

The following Olist CSV files are used or evaluated for the TrustLens project.

| Dataset                      | File                                    | Primary Purpose                                                        |
| ---------------------------- | --------------------------------------- | ---------------------------------------------------------------------- |
| Customers                    | `olist_customers_dataset.csv`           | Customer information and customer location                             |
| Sellers                      | `olist_sellers_dataset.csv`             | Seller information and seller location                                 |
| Orders                       | `olist_orders_dataset.csv`              | Order status, purchase date, delivery date and estimated delivery date |
| Order Items                  | `olist_order_items_dataset.csv`         | Connects orders with sellers and products                              |
| Reviews                      | `olist_order_reviews_dataset.csv`       | Customer review scores and review text                                 |
| Products                     | `olist_products_dataset.csv`            | Product information                                                    |
| Product Category Translation | `product_category_name_translation.csv` | Translates Portuguese product categories into English                  |
| Payments                     | `olist_order_payments_dataset.csv`      | Order payment information                                              |

---

# 3. Dataset-to-Problem Mapping

The TrustLens problem statement requires the system to identify seller behaviours that consistently reduce customer trust over time.

The following mapping explains how the available dataset supports the problem.

| Problem Statement Requirement | Olist Dataset(s)             | Available Attributes                                                                         | TrustLens Usage                                                                         |
| ----------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Seller performance            | Sellers, Orders, Order Items | `seller_id`, order information                                                               | Seller-level performance analysis                                                       |
| Delivery performance          | Orders                       | `order_purchase_timestamp`, `order_delivered_customer_date`, `order_estimated_delivery_date` | Delivery duration and delay calculation                                                 |
| Customer trust / satisfaction | Reviews                      | `review_score`, review text fields                                                           | Rating analysis and trust indicators                                                    |
| Seller activity               | Order Items, Orders          | `seller_id`, `order_id`, `product_id`                                                        | Seller order volume                                                                     |
| Product/category performance  | Products, Order Items        | `product_id`, `product_category_name`                                                        | Category-level seller analysis                                                          |
| Customer location             | Customers                    | `customer_state`, `customer_city`                                                            | Geographic filtering and analysis                                                       |
| Seller location               | Sellers                      | `seller_state`, `seller_city`                                                                | Seller geographic analysis                                                              |
| Order completion              | Orders                       | `order_status`                                                                               | Seller completion/performance analysis                                                  |
| Customer review trends        | Reviews, Orders              | `review_score`, review creation date, order ID                                               | Monthly and historical rating trends                                                    |
| Seller trust score            | Multiple datasets            | Derived metrics                                                                              | Composite Seller Trust Score                                                            |
| Return requests               | Not directly available       | No dedicated return-request field                                                            | Requires documented limitation or supplementary/synthetic data                          |
| Review sentiment              | Review text available        | `review_comment_title`, `review_comment_message`                                             | Can be derived in a future enhancement or implemented as an optional analytical feature |

---

# 4. Important Dataset Limitation

The Olist dataset does **not contain a dedicated return-request dataset or explicit return-request indicator**.

Therefore, TrustLens will not claim that actual return requests are directly available in the Olist data.

The project will handle this limitation according to the approved PRD.

### Current MVP Approach

The MVP focuses on the seller behaviours that can be reliably measured from the Olist dataset:

* Delivery delays
* On-time delivery
* Order completion
* Customer review ratings
* Seller order volume
* Seller review volume
* Seller-level performance trends

These variables are sufficient to build the initial Seller Trust Score.

### Return Analytics

Return-request analysis is treated as a **future enhancement** unless an approved supplementary dataset is introduced.

If return-related analysis is required during development, a clearly documented synthetic/derived return indicator may be considered, but it must not be presented as original Olist data.

---

# 5. Review Sentiment Limitation

The Olist reviews dataset contains customer review text fields:

* `review_comment_title`
* `review_comment_message`

However, the Olist dataset does not provide a pre-computed sentiment label.

Therefore, the initial TrustLens implementation will primarily use:

* `review_score`
* Rating distribution
* Average seller rating
* Rating trends

Text-based sentiment analysis may be implemented as a future enhancement if it remains within the approved project scope.

The project will distinguish between **customer rating analysis** and **NLP-based sentiment analysis**.

---

# 6. Dataset Relationships

The main relationships between the datasets are:

```text
Customers
    |
    | customer_id
    ↓
Orders
    |
    | order_id
    ├──────────────→ Order Reviews
    |
    └──────────────→ Order Items
                         |
                         ├── seller_id ──→ Sellers
                         |
                         └── product_id ─→ Products
```

Products can additionally be connected to:

```text
Products
    |
    | product_category_name
    ↓
Product Category Translation
```

The primary seller-performance relationship is:

```text
Seller
   ↓
Order Items
   ↓
Orders
   ↓
Reviews
```

This relationship allows TrustLens to connect seller activity with delivery outcomes and customer ratings.

---

# 7. Key Dataset Attributes

## 7.1 Orders Dataset

### File

`olist_orders_dataset.csv`

### Important Attributes

| Attribute                       | Description                      | TrustLens Usage                 |
| ------------------------------- | -------------------------------- | ------------------------------- |
| `order_id`                      | Unique order identifier          | Primary order key               |
| `customer_id`                   | Customer identifier              | Connects orders with customers  |
| `order_status`                  | Current order status             | Completion/performance analysis |
| `order_purchase_timestamp`      | Order purchase date/time         | Time-based analysis             |
| `order_approved_at`             | Order approval timestamp         | Order processing analysis       |
| `order_delivered_carrier_date`  | Date order was handed to carrier | Delivery process analysis       |
| `order_delivered_customer_date` | Date delivered to customer       | Delivery duration               |
| `order_estimated_delivery_date` | Estimated delivery date          | Delivery delay calculation      |

### Derived Attributes

The following TrustLens attributes can be calculated from the Orders dataset:

* `order_month`
* `delivery_days`
* `delivery_delay_days`
* `on_time_delivery`

---

# 8. Order Items Dataset

### File

`olist_order_items_dataset.csv`

### Important Attributes

| Attribute             | Description                | TrustLens Usage                    |
| --------------------- | -------------------------- | ---------------------------------- |
| `order_id`            | Order identifier           | Connects item to order             |
| `order_item_id`       | Item sequence within order | Item-level identification          |
| `product_id`          | Product identifier         | Connects item to product           |
| `seller_id`           | Seller identifier          | Connects orders to sellers         |
| `shipping_limit_date` | Seller shipping deadline   | Potential seller shipping analysis |
| `price`               | Product/item price         | Transaction analysis               |
| `freight_value`       | Freight cost               | Delivery-related analysis          |

The `seller_id` field is particularly important because it establishes the relationship between sellers and orders.

---

# 9. Sellers Dataset

### File

`olist_sellers_dataset.csv`

### Important Attributes

| Attribute                | Description              | TrustLens Usage      |
| ------------------------ | ------------------------ | -------------------- |
| `seller_id`              | Unique seller identifier | Primary seller key   |
| `seller_zip_code_prefix` | Seller ZIP prefix        | Geographic analysis  |
| `seller_city`            | Seller city              | Geographic filtering |
| `seller_state`           | Seller state             | Geographic filtering |

Seller-level metrics will be calculated by joining seller information with order items, orders, and reviews.

---

# 10. Reviews Dataset

### File

`olist_order_reviews_dataset.csv`

### Important Attributes

| Attribute                 | Description               | TrustLens Usage             |
| ------------------------- | ------------------------- | --------------------------- |
| `review_id`               | Review identifier         | Review identification       |
| `order_id`                | Associated order          | Connects review with order  |
| `review_score`            | Customer rating from 1–5  | Customer trust indicator    |
| `review_comment_title`    | Review title              | Optional text analysis      |
| `review_comment_message`  | Review message            | Optional sentiment analysis |
| `review_creation_date`    | Review creation timestamp | Review trend analysis       |
| `review_answer_timestamp` | Review response timestamp | Optional response analysis  |

The `review_score` is one of the main inputs to the Seller Trust Score.

---

# 11. Products Dataset

### File

`olist_products_dataset.csv`

### Important Attributes

| Attribute               | Description               | TrustLens Usage               |
| ----------------------- | ------------------------- | ----------------------------- |
| `product_id`            | Unique product identifier | Connects products with orders |
| `product_category_name` | Product category          | Category-level performance    |
| `product_weight_g`      | Product weight            | Optional delivery analysis    |
| `product_length_cm`     | Product length            | Optional product analysis     |
| `product_height_cm`     | Product height            | Optional product analysis     |
| `product_width_cm`      | Product width             | Optional product analysis     |

The primary attribute required for the TrustLens MVP is `product_category_name`.

---

# 12. Customers Dataset

### File

`olist_customers_dataset.csv`

### Important Attributes

| Attribute                  | Description                   | TrustLens Usage      |
| -------------------------- | ----------------------------- | -------------------- |
| `customer_id`              | Unique customer identifier    | Customer key         |
| `customer_unique_id`       | Unique customer across orders | Customer analysis    |
| `customer_zip_code_prefix` | Customer ZIP prefix           | Geographic analysis  |
| `customer_city`            | Customer city                 | Geographic filtering |
| `customer_state`           | Customer state                | Geographic filtering |

Customer state is included as a global dashboard filter according to the approved product requirements.

---

# 13. Product Category Translation Dataset

### File

`product_category_name_translation.csv`

This dataset maps Portuguese product category names to English category names.

| Attribute                       | Description                  |
| ------------------------------- | ---------------------------- |
| `product_category_name`         | Original Portuguese category |
| `product_category_name_english` | English category name        |

The translated category name will be used in the TrustLens dashboard to improve usability.

---

# 14. Data Processing Strategy

The TrustLens data pipeline will follow this process:

```text
Raw Olist CSV Files
        ↓
Schema Inspection
        ↓
Data Cleaning
        ↓
Missing Value Handling
        ↓
Duplicate Detection
        ↓
Date Conversion
        ↓
Relationship Validation
        ↓
Dataset Joining
        ↓
Feature Engineering
        ↓
Seller-Level Aggregation
        ↓
SQLite Database
        ↓
SQL Analytics
        ↓
Streamlit Dashboard
```

---

# 15. Data Cleaning Requirements

The following cleaning operations will be performed before analytics.

| Cleaning Operation       | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| Missing value inspection | Identify missing values in important columns             |
| Duplicate detection      | Identify duplicate records                               |
| Date conversion          | Convert timestamp columns to appropriate datetime format |
| Invalid rating detection | Verify that review scores are within the expected range  |
| Join validation          | Verify that dataset relationships are valid              |
| Null handling            | Apply documented handling strategies                     |
| Category standardization | Standardize product category values                      |
| Data type validation     | Ensure columns have appropriate data types               |

---

# 16. Feature Engineering

TrustLens will generate additional analytical attributes from the raw datasets.

| Derived Attribute        | Description                                                              |
| ------------------------ | ------------------------------------------------------------------------ |
| `order_month`            | Month extracted from order purchase date                                 |
| `delivery_days`          | Number of days between purchase and customer delivery                    |
| `delivery_delay_days`    | Difference between actual and estimated delivery                         |
| `on_time_delivery`       | Indicates whether an order was delivered on or before the estimated date |
| `seller_total_orders`    | Total orders associated with a seller                                    |
| `seller_review_count`    | Number of reviews associated with a seller                               |
| `seller_average_rating`  | Average customer review score for a seller                               |
| `seller_on_time_rate`    | Percentage of seller orders delivered on time                            |
| `seller_completion_rate` | Percentage of seller orders considered successfully completed            |
| `seller_trust_score`     | Composite seller trust metric                                            |
| `trust_band`             | Trust classification based on Seller Trust Score                         |

---

# 17. Seller Trust Score Inputs

The Seller Trust Score is designed as a transparent composite metric.

The initial weighting defined in the PRD is:

| Component        |   Weight |
| ---------------- | -------: |
| Rating Score     |      40% |
| On-Time Delivery |      30% |
| Completion Rate  |      20% |
| Review Volume    |      10% |
| **Total**        | **100%** |

The resulting Seller Trust Score will be normalized to a range of **0–100**.

### Trust Bands

| Trust Score | Trust Band |
| ----------: | ---------- |
|      80–100 | High       |
|       60–79 | Monitor    |
|        0–59 | High Risk  |

The final implementation will document the exact normalization method used for each component.

---

# 18. Dataset Storage Strategy

Raw datasets are stored locally for development and processing but are **not committed to the Git repository** because some Olist CSV files contain a large number of records.

The raw dataset directory is excluded through `.gitignore`.

Example:

```text
data/
├── raw/
├── processed/
└── database/
```

### Raw Data

Contains the original Olist CSV files used for processing.

### Processed Data

Contains cleaned and transformed datasets generated by the TrustLens pipeline.

### Database

Contains the SQLite database used by the dashboard.

---

# 19. Repository Data Policy

Large raw CSV files will not be committed to GitHub.

This prevents:

* Large repository size
* Slow cloning and pulling
* Unnecessary duplication of public data
* Repository performance issues

The repository will instead contain:

* Dataset documentation
* Data dictionary
* Data relationship documentation
* Data processing scripts
* Feature engineering logic
* Database schema
* Instructions for obtaining the dataset

The dataset itself can be obtained separately from the original Olist dataset source.

---

# 20. Data Validation Requirements

Before the data is used by the analytics layer, the following checks must be performed:

1. Required files must exist.
2. Required columns must be present.
3. Data types must be validated.
4. Date columns must be parseable.
5. Review scores must be within the expected range.
6. Duplicate records must be identified.
7. Primary/foreign key relationships must be checked.
8. Missing values must be quantified.
9. Join results must be validated.
10. Record counts before and after processing must be logged.

---

# 21. Expected Dataset Relationships

The following relationships will be validated during preprocessing:

| Parent Dataset | Parent Key              | Child Dataset        | Child Key               |
| -------------- | ----------------------- | -------------------- | ----------------------- |
| Customers      | `customer_id`           | Orders               | `customer_id`           |
| Orders         | `order_id`              | Order Items          | `order_id`              |
| Orders         | `order_id`              | Reviews              | `order_id`              |
| Sellers        | `seller_id`             | Order Items          | `seller_id`             |
| Products       | `product_id`            | Order Items          | `product_id`            |
| Products       | `product_category_name` | Category Translation | `product_category_name` |

These relationships form the foundation for seller-level TrustLens analytics.

---

# 22. Dataset Sufficiency for TrustLens MVP

The Olist dataset is considered sufficient for the core TrustLens MVP because it provides the necessary information to calculate:

* Seller order volume
* Seller review volume
* Seller average rating
* Delivery duration
* Delivery delay
* On-time delivery rate
* Order completion rate
* Category-level seller performance
* Customer-state analysis
* Seller Trust Score
* Trust bands
* Historical seller performance trends

However, the dataset does not directly provide dedicated return-request records or pre-computed sentiment labels.

These limitations are explicitly documented and will not be represented as native Olist attributes.

---

# 23. Dataset Inspection Status

| Inspection Area                 | Status                                           |
| ------------------------------- | ------------------------------------------------ |
| Dataset acquisition             | Completed                                        |
| Raw CSV availability            | Completed                                        |
| File structure inspection       | Completed                                        |
| Column/schema inspection        | Completed                                        |
| Dataset relationship inspection | Completed                                        |
| Missing-value inspection        | Completed / To be validated during preprocessing |
| Duplicate inspection            | To be performed during preprocessing             |
| Data type validation            | To be performed during preprocessing             |
| Join validation                 | To be performed during preprocessing             |
| Feature engineering validation  | To be performed during development               |

---

# 24. Dataset Usage Summary

The Olist dataset provides the primary historical data foundation for TrustLens.

The project will transform the raw marketplace data into seller-level analytical metrics and use those metrics to identify seller behaviours associated with lower customer trust.

The main analytical flow is:

```text
Seller Activity
      +
Delivery Performance
      +
Customer Ratings
      +
Order Completion
      +
Review Volume
      ↓
Seller-Level Metrics
      ↓
Seller Trust Score
      ↓
Trust Band
      ↓
TrustLens Dashboard
      ↓
Identification of High-Risk Seller Behaviour
```

---

# 25. Scope Boundary

TrustLens will focus on **historical descriptive and diagnostic analytics** for the MVP.

The MVP will not claim to:

* Predict future seller behaviour
* Automatically take action against sellers
* Make final business decisions about sellers
* Represent missing return data as actual Olist return records
* Perform advanced NLP sentiment analysis unless explicitly included in the approved implementation scope
* Provide real-time marketplace monitoring

The dashboard is intended to support marketplace managers and analysts by providing a consolidated view of seller performance and customer trust indicators.

---

