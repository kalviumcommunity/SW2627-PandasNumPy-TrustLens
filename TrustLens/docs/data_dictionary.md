# TrustLens — Olist Dataset Data Dictionary

## 1. Purpose

This document describes the datasets used by TrustLens and identifies the attributes relevant to seller behaviour, delivery performance, customer satisfaction, product categories, geographical analysis, and Seller Trust Index (STI) calculation.

The primary dataset selected for TrustLens is the **Brazilian E-Commerce Public Dataset by Olist**.

The purpose of this document is to establish the data requirements and schema mapping before implementation of the TrustLens data ingestion, preprocessing, analytics, and dashboard modules.

The dictionary identifies:

* Source datasets used by TrustLens
* Important attributes from each dataset
* Relationships between datasets
* Attributes required for seller-level analysis
* Derived metrics required for the Seller Trust Index
* Dataset limitations
* Data validation requirements

---

# 2. Dataset Overview

TrustLens uses the following Olist datasets:

| Dataset        | Purpose in TrustLens                                        |
| -------------- | ----------------------------------------------------------- |
| Orders         | Order lifecycle and delivery performance analysis           |
| Order Items    | Seller-product-order relationship and seller order activity |
| Reviews        | Customer rating and review analysis                         |
| Sellers        | Seller identification and geographical analysis             |
| Customers      | Customer identification and geographical analysis           |
| Products       | Product category and product-level analysis                 |
| Order Payments | Supporting order/payment analysis                           |

The following datasets form the **core TrustLens MVP analysis layer**:

* Orders
* Order Items
* Reviews
* Sellers
* Customers
* Products

The Order Payments dataset is retained as a supporting dataset and may be used for additional analysis if required.

---

# 3. Orders Dataset

## Purpose

The Orders dataset provides information about the order lifecycle and delivery timeline.

## Important Attributes

| Attribute                       | Description                                  | TrustLens Usage                                 |
| ------------------------------- | -------------------------------------------- | ----------------------------------------------- |
| `order_id`                      | Unique identifier of an order                | Order identification and joins                  |
| `customer_id`                   | Customer associated with the order           | Customer linkage                                |
| `order_status`                  | Current order status                         | Order completion analysis                       |
| `order_purchase_timestamp`      | Time when order was placed                   | Time-based analysis                             |
| `order_approved_at`             | Order approval timestamp                     | Order lifecycle analysis                        |
| `order_delivered_carrier_date`  | Date the order was handed to the carrier     | Shipping and delivery analysis                  |
| `order_delivered_customer_date` | Date the order was delivered to the customer | Delivery duration calculation                   |
| `order_estimated_delivery_date` | Estimated delivery date                      | Delivery delay and on-time delivery calculation |

## Key TrustLens Metrics Derived

The Orders dataset will contribute to:

* Delivery duration
* Delivery delay
* On-time delivery
* Order completion
* Monthly order trends
* Seller-level delivery performance after joining with Order Items

---

# 4. Order Items Dataset

## Purpose

The Order Items dataset connects orders with sellers and products.

It is one of the most important datasets for TrustLens because the `seller_id` is used to connect order activity and delivery performance to individual sellers.

## Important Attributes

| Attribute             | Description                   | TrustLens Usage                       |
| --------------------- | ----------------------------- | ------------------------------------- |
| `order_id`            | Unique order identifier       | Join with Orders                      |
| `order_item_id`       | Item sequence within an order | Item identification                   |
| `product_id`          | Product identifier            | Join with Products                    |
| `seller_id`           | Seller identifier             | Seller-level analysis                 |
| `shipping_limit_date` | Seller shipping deadline      | Shipping performance analysis         |
| `price`               | Item price                    | Order and seller transaction analysis |
| `freight_value`       | Freight/shipping cost         | Supporting delivery analysis          |

## Key TrustLens Metrics Derived

The Order Items dataset will contribute to:

* Seller order volume
* Seller-product relationships
* Seller transaction activity
* Seller shipping performance
* Category-level seller analysis

---

# 5. Reviews Dataset

## Purpose

The Reviews dataset provides customer feedback associated with orders.

Customer ratings are a major input to the Seller Trust Index.

## Important Attributes

| Attribute                 | Description               | TrustLens Usage                           |
| ------------------------- | ------------------------- | ----------------------------------------- |
| `review_id`               | Review identifier         | Review identification                     |
| `order_id`                | Associated order          | Join with Orders                          |
| `review_score`            | Customer rating from 1–5  | Customer satisfaction and STI             |
| `review_comment_title`    | Review title              | Future sentiment analysis                 |
| `review_comment_message`  | Review text               | Future sentiment analysis                 |
| `review_creation_date`    | Review creation date      | Review trend analysis                     |
| `review_answer_timestamp` | Review response timestamp | Supporting seller responsiveness analysis |

## Key TrustLens Metrics Derived

The Reviews dataset will contribute to:

* Average seller rating
* Review count
* Rating distribution
* Low-rating percentage
* Rating trends over time
* Seller-level customer satisfaction analysis

Review text is available in the dataset and may be used for sentiment analysis in a future version.

---

# 6. Sellers Dataset

## Purpose

The Sellers dataset provides seller identification and geographical information.

## Important Attributes

| Attribute                | Description              | TrustLens Usage          |
| ------------------------ | ------------------------ | ------------------------ |
| `seller_id`              | Unique seller identifier | Seller identification    |
| `seller_zip_code_prefix` | Seller ZIP code prefix   | Geographic analysis      |
| `seller_city`            | Seller city              | Geographic analysis      |
| `seller_state`           | Seller state             | Seller location analysis |

## Key TrustLens Metrics Derived

The Sellers dataset will contribute to:

* Seller identification
* Seller location
* Seller state filtering
* Geographic seller analysis

---

# 7. Customers Dataset

## Purpose

The Customers dataset provides customer identity and geographical information.

## Important Attributes

| Attribute                  | Description                | TrustLens Usage            |
| -------------------------- | -------------------------- | -------------------------- |
| `customer_id`              | Unique customer identifier | Customer linkage           |
| `customer_unique_id`       | Unique customer identity   | Customer-level analysis    |
| `customer_zip_code_prefix` | Customer ZIP code prefix   | Geographic analysis        |
| `customer_city`            | Customer city              | Customer location analysis |
| `customer_state`           | Customer state             | Customer state filtering   |

## Key TrustLens Metrics Derived

The Customers dataset will contribute to:

* Customer location analysis
* Customer state filtering
* Seller-customer geographical analysis
* Regional trust analysis

---

# 8. Products Dataset

## Purpose

The Products dataset provides product-level information required for category analysis.

## Important Attributes

| Attribute                    | Description                | TrustLens Usage         |
| ---------------------------- | -------------------------- | ----------------------- |
| `product_id`                 | Unique product identifier  | Product linkage         |
| `product_category_name`      | Product category           | Category-level analysis |
| `product_name_lenght`        | Product name length        | Supporting attribute    |
| `product_description_lenght` | Product description length | Supporting attribute    |
| `product_photos_qty`         | Number of product photos   | Supporting attribute    |
| `product_weight_g`           | Product weight             | Supporting attribute    |
| `product_length_cm`          | Product length             | Supporting attribute    |
| `product_height_cm`          | Product height             | Supporting attribute    |
| `product_width_cm`           | Product width              | Supporting attribute    |

## Key TrustLens Metrics Derived

The Products dataset will contribute to:

* Product category analysis
* Seller-category performance analysis
* Category-level ratings
* Category-level delivery performance

---

# 9. Order Payments Dataset

## Purpose

The Order Payments dataset contains payment information associated with customer orders.

It is not a primary input to the Seller Trust Index but can provide supporting context for order and transaction analysis.

## Important Attributes

| Attribute              | Description                         | TrustLens Usage                 |
| ---------------------- | ----------------------------------- | ------------------------------- |
| `order_id`             | Unique order identifier             | Join with Orders                |
| `payment_sequential`   | Sequence of payment within an order | Payment identification          |
| `payment_type`         | Type of payment used                | Supporting transaction analysis |
| `payment_installments` | Number of payment installments      | Supporting transaction analysis |
| `payment_value`        | Value of the payment                | Supporting transaction analysis |

## MVP Usage

The Order Payments dataset is considered a **supporting dataset**.

It is not required for the initial Seller Trust Index calculation but may be incorporated into additional seller/order analysis if useful during implementation.

---

# 10. Dataset Relationship and Join Mapping

TrustLens requires multiple Olist datasets to be joined to create a unified seller-level analytical dataset.

| Source Dataset | Join Key      | Target Dataset | Relationship Purpose                         |
| -------------- | ------------- | -------------- | -------------------------------------------- |
| Orders         | `order_id`    | Order Items    | Connect orders to sellers and products       |
| Orders         | `order_id`    | Reviews        | Connect customer reviews to orders           |
| Orders         | `customer_id` | Customers      | Connect orders to customer geography         |
| Order Items    | `seller_id`   | Sellers        | Connect orders/items to sellers              |
| Order Items    | `product_id`  | Products       | Connect sellers/orders to product categories |
| Orders         | `order_id`    | Order Payments | Connect orders to payment information        |

### Primary Analytical Relationship

The core TrustLens relationship is:

`Orders → Order Items → Sellers`

This allows order and delivery behaviour to be attributed to individual sellers.

Additional relationships are used to enrich seller analysis:

`Orders → Reviews`

`Orders → Customers`

`Order Items → Products`

---

# 11. TrustLens Attribute Mapping

The following mapping connects the available Olist attributes with the TrustLens product requirements.

| TrustLens Requirement     | Source Attribute(s)                             | Derived Metric           |
| ------------------------- | ----------------------------------------------- | ------------------------ |
| Seller identification     | `seller_id`                                     | `seller_id`              |
| Seller order volume       | `seller_id`, `order_id`                         | `seller_total_orders`    |
| Seller item volume        | `seller_id`, `order_id`, `order_item_id`        | `seller_total_items`     |
| Delivery performance      | Purchase and delivery timestamps                | `delivery_days`          |
| Delivery delay            | Delivered date, estimated date                  | `delivery_delay_days`    |
| On-time delivery          | Delivered date, estimated date                  | `on_time_delivery`       |
| Customer satisfaction     | `review_score`                                  | `seller_average_rating`  |
| Review volume             | `review_id`, `seller_id`                        | `seller_review_count`    |
| Low-rating behaviour      | `review_score`                                  | `low_rating_rate`        |
| Order completion          | `order_status`                                  | `seller_completion_rate` |
| Seller shipping behaviour | `shipping_limit_date`, delivery timestamps      | `shipping_delay`         |
| Category performance      | `product_category_name`                         | Category-level metrics   |
| Customer geography        | `customer_state`                                | Customer state filtering |
| Seller geography          | `seller_state`                                  | Seller location analysis |
| Seller trust              | Rating, delivery, completion and review signals | `seller_trust_index`     |
| Trust classification      | `seller_trust_index`                            | `trust_band`             |

---

# 12. Derived Attributes

TrustLens will create the following derived attributes during the data processing phase.

| Derived Attribute        | Description                                                                              |
| ------------------------ | ---------------------------------------------------------------------------------------- |
| `order_month`            | Month extracted from order purchase timestamp                                            |
| `delivery_days`          | Number of days between purchase and customer delivery                                    |
| `delivery_delay_days`    | Difference between actual delivery date and estimated delivery date                      |
| `on_time_delivery`       | Indicates whether delivery occurred on or before the estimated delivery date             |
| `seller_average_rating`  | Average review score associated with seller orders                                       |
| `seller_total_orders`    | Total number of orders associated with a seller                                          |
| `seller_total_items`     | Total number of items sold by a seller                                                   |
| `seller_review_count`    | Number of reviews associated with a seller                                               |
| `seller_completion_rate` | Percentage of seller-associated orders considered completed                              |
| `seller_on_time_rate`    | Percentage of seller-associated deliveries completed on time                             |
| `low_rating_rate`        | Percentage of seller reviews with low ratings                                            |
| `shipping_delay`         | Difference between shipping deadline and actual delivery/shipping event where applicable |
| `seller_trust_index`     | Composite seller trust index ranging from 0–100                                          |
| `trust_band`             | High Trust, Monitor, or High Risk                                                        |

---

# 13. Seller Trust Index Inputs

The **Seller Trust Index (STI)** is the primary seller-level metric used by TrustLens to summarize customer trust and seller behaviour.

The STI will combine multiple normalized seller-level indicators.

| Component             |   Weight |
| --------------------- | -------: |
| Rating Score          |      40% |
| On-Time Delivery Rate |      30% |
| Order Completion Rate |      20% |
| Review Volume Score   |      10% |
| **Total**             | **100%** |

### Component Definitions

**Rating Score**

The seller's average customer rating is normalized from the original 1–5 scale to a 0–100 scale.

**On-Time Delivery Rate**

The percentage of eligible seller-associated deliveries completed on or before the estimated delivery date.

**Order Completion Rate**

The percentage of seller-associated orders that reach the defined completed/delivered status.

**Review Volume Score**

A normalized measure representing the volume of customer feedback available for the seller.

The review volume component will be normalized to prevent sellers with very different order volumes from being unfairly compared based only on raw review counts.

### STI Formula

The final Seller Trust Index will be calculated as:

`STI = (Rating Score × 0.40) + (On-Time Delivery Rate × 0.30) + (Order Completion Rate × 0.20) + (Review Volume Score × 0.10)`

The final STI will range from **0 to 100**.

---

# 14. Trust Bands

TrustLens will classify sellers into three trust bands based on their Seller Trust Index.

| STI Range | Trust Band | Interpretation                                                      |
| --------: | ---------- | ------------------------------------------------------------------- |
|    80–100 | High Trust | Seller demonstrates consistently strong trust-related performance   |
|     60–79 | Monitor    | Seller shows acceptable performance but requires monitoring         |
|      0–59 | High Risk  | Seller demonstrates behaviours associated with lower customer trust |

The trust bands are intended for dashboard visualization and seller comparison.

---

# 15. Problem Statement Alignment

The selected Olist datasets support the major analytical requirements of the TrustLens problem statement.

| Problem Statement Requirement | Olist Data Available         | TrustLens Implementation                 |
| ----------------------------- | ---------------------------- | ---------------------------------------- |
| Seller performance analysis   | Sellers, Orders, Order Items | Seller-level KPIs                        |
| Seller behaviour analysis     | Orders, Order Items          | Completion, delivery and order behaviour |
| Return request analysis       | Not directly available       | Documented dataset limitation            |
| Customer review analysis      | Reviews                      | Ratings and review metrics               |
| Customer sentiment analysis   | Review text available        | Future sentiment analysis                |
| Delivery performance          | Orders                       | Delivery delay and on-time delivery      |
| Product/category analysis     | Products, Order Items        | Category-level seller analysis           |
| Customer geography            | Customers                    | Regional analysis                        |
| Seller geography              | Sellers                      | Seller location analysis                 |
| Customer trust measurement    | Reviews + Orders             | Seller Trust Index                       |
| Long-term seller behaviour    | Historical Olist records     | Time-based seller performance trends     |

---

# 16. Dataset Limitations

## 16.1 Return Request Data

The Olist dataset does not contain a dedicated return-request or return-status dataset.

Therefore, dedicated return-request analytics are **not included in the current MVP implementation**.

Return-related functionality may be considered as a future enhancement if an appropriate supplementary dataset becomes available.

## 16.2 Review Sentiment

The Reviews dataset contains review titles and review messages.

However, NLP-based sentiment classification is outside the current MVP scope.

The MVP will primarily use `review_score` as the customer satisfaction signal.

Review text sentiment analysis may be introduced in a future version.

## 16.3 Seller Behaviour Events

The Olist dataset does not contain a detailed seller activity/event log such as:

* Seller response time
* Seller communication history
* Seller cancellation reason
* Seller policy violations
* Seller-specific return behaviour

Therefore, TrustLens will focus on behaviours that can be reliably derived from the available historical transaction, delivery, and review data.

## 16.4 Synthetic / Derived Attributes

Where the original dataset does not directly provide a required TrustLens metric, the metric will be derived from available attributes using documented calculation rules.

No fabricated seller performance values will be introduced into the core MVP unless explicitly documented as synthetic data.

---

# 17. Data Validation Requirements

Before the implementation pipeline is developed, the following validation checks must be performed.

### File-Level Validation

* [ ] All expected Olist CSV files are available
* [ ] File names are correctly identified
* [ ] Files can be loaded successfully
* [ ] Encoding issues are identified
* [ ] Dataset row counts are recorded

### Schema Validation

* [ ] Required columns are present
* [ ] Column names match the expected schema
* [ ] Data types are identified
* [ ] Date/time columns are validated
* [ ] Join keys are present

### Data Quality Validation

* [ ] Missing values are identified
* [ ] Duplicate records are investigated
* [ ] Invalid IDs are investigated
* [ ] Invalid dates are investigated
* [ ] Delivery dates are checked for logical consistency
* [ ] Review scores are verified to be within the expected range
* [ ] Order statuses are reviewed
* [ ] Product categories are checked for missing values

### Relationship Validation

* [ ] `order_id` relationship between Orders and Order Items is validated
* [ ] `order_id` relationship between Orders and Reviews is validated
* [ ] `customer_id` relationship between Orders and Customers is validated
* [ ] `seller_id` relationship between Order Items and Sellers is validated
* [ ] `product_id` relationship between Order Items and Products is validated
* [ ] `order_id` relationship between Orders and Order Payments is validated

---

# 18. Data Inspection Status

The following information will be completed during the dataset inspection phase.

| Dataset        | File Available |       Row Count |    Column Count | Missing Values  | Duplicate Check | Status  |
| -------------- | -------------- | --------------: | --------------: | --------------- | --------------- | ------- |
| Orders         | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Order Items    | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Reviews        | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Sellers        | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Customers      | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Products       | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |
| Order Payments | Yes            | To be inspected | To be inspected | To be inspected | To be inspected | Pending |

The detailed inspection results will be documented separately during the data inspection phase.

---

# 19. TrustLens Analytical Dataset

After ingestion and preprocessing, the source datasets will be transformed into a unified analytical dataset.

The expected analytical flow is:

`Raw Olist CSV Files`

↓

`Data Validation`

↓

`Data Cleaning`

↓

`Dataset Joins`

↓

`Derived Metrics`

↓

`Seller-Level Aggregation`

↓

`Seller Trust Index Calculation`

↓

`Trust Band Classification`

↓

`Streamlit Dashboard`

The final seller-level analytical dataset is expected to contain attributes such as:

| Attribute                | Purpose                          |
| ------------------------ | -------------------------------- |
| `seller_id`              | Seller identification            |
| `seller_state`           | Seller geographic analysis       |
| `seller_city`            | Seller geographic analysis       |
| `seller_total_orders`    | Seller order activity            |
| `seller_total_items`     | Seller item volume               |
| `seller_average_rating`  | Customer satisfaction            |
| `seller_review_count`    | Review volume                    |
| `low_rating_rate`        | Negative customer feedback       |
| `seller_on_time_rate`    | Delivery performance             |
| `seller_completion_rate` | Order completion behaviour       |
| `seller_trust_index`     | Overall seller trust measurement |
| `trust_band`             | Seller risk/trust classification |

This analytical dataset will serve as a primary input to the TrustLens BI dashboard.

---

# 20. Validation Checklist

Before implementation, the following must be verified against the downloaded dataset:

* [ ] All expected CSV files are available
* [ ] Required columns are present
* [ ] Seller IDs are available
* [ ] Order IDs are available
* [ ] Product IDs are available
* [ ] Review scores are available
* [ ] Order delivery timestamps are available
* [ ] Estimated delivery dates are available
* [ ] Product categories are available
* [ ] Customer states are available
* [ ] Seller states are available
* [ ] Join keys are consistent
* [ ] Missing values are documented
* [ ] Duplicate records are investigated
* [ ] Dataset row counts are documented
* [ ] Dataset relationships are validated
* [ ] Required derived metrics can be calculated
* [ ] Seller Trust Index inputs can be calculated

---

# Conclusion

The Olist dataset provides the core attributes required for the TrustLens MVP, including seller identification, order activity, delivery performance, customer ratings, product categories, and geographical information.

The available historical transaction and review data can be transformed into seller-level behavioural metrics and combined into the Seller Trust Index.

The dataset does not directly provide dedicated return-request data or precomputed review sentiment. These limitations are documented and will be treated as future enhancements rather than introducing unsupported assumptions into the MVP.

The detailed dataset inspection will be completed before implementing the data ingestion and preprocessing pipeline.

---

## What changed in this PR?

I would make **this your second PR**, rather than creating another unrelated documentation PR.

### PR Title

```text
docs: enhance TrustLens Olist data dictionary and schema mapping
```

### Commit Message

```text
docs: enhance Olist data dictionary for TrustLens analytics
```

### PR Description — copy/paste

```markdown
## Overview

This PR enhances the TrustLens Olist dataset data dictionary and strengthens the mapping between the available Olist datasets and the TrustLens product requirements.

The update documents how the selected datasets support seller behaviour analysis, delivery performance, customer satisfaction, product/category analysis, and Seller Trust Index (STI) calculation.

## Changes Made

### 1. Expanded Dataset Documentation
- Added documentation for the Order Payments dataset.
- Clarified the purpose of each Olist dataset used by TrustLens.
- Identified core MVP datasets and supporting datasets.

### 2. Added Dataset Relationship Mapping
- Documented the relationships between Orders, Order Items, Sellers, Reviews, Customers, Products, and Order Payments.
- Defined the primary join keys used for creating the unified analytical dataset.

### 3. Improved TrustLens Attribute Mapping
- Mapped Olist attributes to TrustLens requirements.
- Added seller item volume and low-rating metrics.
- Added seller shipping behaviour as a supporting metric.

### 4. Clarified Seller Trust Index
- Standardized terminology to Seller Trust Index (STI).
- Documented the STI components and their weights.
- Added the STI calculation formula.
- Clarified how review volume should be normalized.

### 5. Added Problem Statement Alignment
- Documented how the Olist dataset supports seller performance, seller behaviour, delivery, review, category, and customer trust analysis.
- Documented dataset limitations for return requests and review sentiment.

### 6. Added Data Validation Requirements
- Added file-level, schema-level, data-quality, and relationship validation checks.
- Added validation requirements for join keys and derived metrics.

### 7. Added Data Inspection Status
- Added a structured table for recording row counts, column counts, missing values, duplicate checks, and inspection status for each dataset.

### 8. Added Analytical Dataset Definition
- Documented the expected seller-level analytical dataset that will be generated during preprocessing.
- Defined the expected flow from raw datasets to Seller Trust Index and Trust Band classification.

## Files Changed

- `docs/data_dictionary.md`

## Scope

This PR is documentation-only.

No data processing code, analytics logic, or dashboard implementation has been added.

The purpose is to establish a clear data contract and analytical mapping before implementation begins.

## Validation

The documentation has been reviewed against:

- TrustLens problem statement
- Approved PRD
- Olist dataset structure
- Seller Trust Index requirements

## Next Step

After this documentation update, the team can proceed with detailed dataset inspection and validation before implementing the ingestion and preprocessing pipeline.
```
