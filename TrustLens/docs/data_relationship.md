# TrustLens — Olist Dataset Relationships & Data Quality Analysis

## 1. Purpose

This document describes the relationships between the Olist datasets used by TrustLens and identifies the data-quality checks required before implementing the data pipeline.

The objective is to establish a reliable data model for seller-level analytics and Seller Trust Index calculation.

---

# 2. Dataset Relationships

The primary relationships used by TrustLens are:

Orders
↓
Order Items
↓
Sellers

Orders
↓
Reviews

Order Items
↓
Products

Orders
↓
Customers

---

# 3. Relationship Mapping

| Parent Dataset | Parent Key | Child Dataset | Child Key | Relationship Purpose |
|---|---|---|---|---|
| Orders | order_id | Order Items | order_id | Connect orders with sellers/products |
| Orders | order_id | Reviews | order_id | Connect orders with customer reviews |
| Order Items | seller_id | Sellers | seller_id | Connect orders with sellers |
| Order Items | product_id | Products | product_id | Connect orders with product categories |
| Orders | customer_id | Customers | customer_id | Connect orders with customers |

---

# 4. TrustLens Analytical Join

The main analytical relationship is:

Orders
+
Order Items
+
Reviews
+
Sellers
+
Products
+
Customers

This allows TrustLens to connect:

Seller
→ Orders
→ Delivery
→ Reviews
→ Products
→ Customer Geography

The resulting analytical dataset will support seller-level performance analysis.

---

# 5. Key Join Keys

| Join Key | Datasets | Purpose |
|---|---|---|
| order_id | Orders, Order Items, Reviews | Order-level integration |
| seller_id | Order Items, Sellers | Seller-level analysis |
| product_id | Order Items, Products | Product category analysis |
| customer_id | Orders, Customers | Customer geography |

---

# 6. Expected Cardinality

| Relationship | Expected Relationship |
|---|---|
| Orders → Order Items | One-to-many |
| Orders → Reviews | One-to-one or one-to-many depending on dataset records |
| Sellers → Order Items | One-to-many |
| Products → Order Items | One-to-many |
| Customers → Orders | One-to-many |

The actual cardinality will be validated against the downloaded dataset during implementation.

---

# 7. Data Quality Checks

The following checks must be performed before transformation.

## 7.1 Missing Values

Check for missing values in:

- order_id
- seller_id
- product_id
- customer_id
- order_status
- delivery timestamps
- estimated delivery date
- review_score

Missing values must be documented and handled according to their analytical importance.

---

## 7.2 Duplicate Records

Check for duplicate:

- order records
- order item records
- review records
- seller records
- customer records
- product records

Duplicates must be investigated before aggregation.

---

## 7.3 Invalid Dates

Validate:

- purchase timestamps
- approval timestamps
- carrier delivery dates
- customer delivery dates
- estimated delivery dates
- review dates

Date fields must be converted to a consistent datetime format.

---

## 7.4 Invalid Review Scores

Review scores should be checked against the expected 1–5 range.

Values outside the valid range must be identified and handled.

---

## 7.5 Join Integrity

Validate that:

- Order Items reference valid Orders
- Order Items reference valid Sellers
- Order Items reference valid Products
- Reviews reference valid Orders
- Orders reference valid Customers

Unmatched records must be identified and documented.

---

# 8. Delivery Metric Validation

TrustLens depends on delivery performance metrics.

The following fields must be validated:

- order_purchase_timestamp
- order_delivered_customer_date
- order_estimated_delivery_date

These fields will be used to derive:

### Delivery Days

text
Delivery Days =
Delivered Customer Date - Purchase Date
`

### Delivery Delay

text
Delivery Delay Days =
Delivered Customer Date - Estimated Delivery Date


### On-Time Delivery

text
On-Time Delivery =
1 if actual delivery date <= estimated delivery date
0 otherwise


The exact handling of missing delivery dates will be defined during preprocessing.

---

# 9. Seller-Level Aggregation

The analytical data must eventually support seller-level aggregation.

Expected seller-level metrics include:

| Metric                | Source               |
| --------------------- | -------------------- |
| Total Orders          | Orders + Order Items |
| Average Rating        | Reviews              |
| Review Count          | Reviews              |
| Completion Rate       | Order Status         |
| On-Time Rate          | Delivery dates       |
| Average Delivery Days | Delivery dates       |
| Seller Trust Index    | Derived metrics      |
| Trust Band            | Seller Trust Index   |

---

# 10. Dataset Limitations

The Olist dataset does not contain a dedicated return-request or return-status dataset.

Therefore:

* Return-request analytics are excluded from the current MVP.
* Return-related analysis may be considered in future scope.

Review text is available, but:

* NLP sentiment analysis is not part of the current MVP.
* Review scores will be used for the MVP customer satisfaction analysis.

---

# 11. Data Inspection Checklist

* [ ] Verify all expected datasets are available
* [ ] Verify row counts
* [ ] Verify column names
* [ ] Verify data types
* [ ] Check missing values
* [ ] Check duplicate records
* [ ] Check invalid dates
* [ ] Check review score range
* [ ] Check join-key availability
* [ ] Check unmatched foreign keys
* [ ] Check order status values
* [ ] Check delivery-date consistency
* [ ] Confirm seller-level aggregation is possible

---

# 12. Readiness Criteria

The dataset will be considered ready for implementation when:

1. Required datasets are available.
2. Required join keys are present.
3. Required TrustLens attributes are available.
4. Data-quality issues have been identified.
5. Missing-value handling strategies are documented.
6. Join relationships are validated.
7. Delivery metrics can be derived.
8. Seller-level aggregation is feasible.

---

# Conclusion

The Olist dataset provides the relational structure required to connect sellers, orders, products, customers, deliveries, and reviews.

This relationship and validation analysis provides the foundation for implementing the TrustLens ingestion and preprocessing pipeline after PRD approval.
---