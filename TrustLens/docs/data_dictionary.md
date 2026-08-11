# TrustLens — Olist Dataset Data Dictionary

## 1. Purpose

This document describes the datasets used by TrustLens and identifies the attributes relevant to seller behaviour, delivery performance, customer satisfaction, product categories, and Seller Trust Index (STI) calculation.

The primary dataset selected for TrustLens is the Brazilian E-Commerce Public Dataset by Olist.

This document is part of the Day 6 Data Inspection phase and is intended to validate dataset availability before implementation of the data pipeline.

---

## 2. Dataset Overview

TrustLens uses the following Olist datasets:

| Dataset | Purpose in TrustLens |
|---|---|
| Orders | Order lifecycle and delivery analysis |
| Order Items | Seller-product-order relationship |
| Reviews | Customer rating and review analysis |
| Sellers | Seller identification and location |
| Customers | Customer location analysis |
| Products | Product category analysis |

---

## 3. Orders Dataset

### Purpose

The Orders dataset provides information about the order lifecycle and delivery timeline.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| order_id | Unique identifier of an order | Order identification and joins |
| customer_id | Customer associated with the order | Customer linkage |
| order_status | Current order status | Completion analysis |
| order_purchase_timestamp | Time when order was placed | Time-based analysis |
| order_approved_at | Order approval timestamp | Order lifecycle analysis |
| order_delivered_carrier_date | Date handed to carrier | Delivery analysis |
| order_delivered_customer_date | Date delivered to customer | Delivery duration |
| order_estimated_delivery_date | Estimated delivery date | Delivery delay calculation |

---

## 4. Order Items Dataset

### Purpose

The Order Items dataset connects orders with sellers and products.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| order_id | Unique order identifier | Join with Orders |
| order_item_id | Item sequence within order | Item identification |
| product_id | Product identifier | Join with Products |
| seller_id | Seller identifier | Seller-level analysis |
| shipping_limit_date | Seller shipping deadline | Shipping analysis |
| price | Item price | Order/item analysis |
| freight_value | Freight cost | Supporting analysis |

---

## 5. Reviews Dataset

### Purpose

The Reviews dataset provides customer feedback associated with orders.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| review_id | Review identifier | Review identification |
| order_id | Associated order | Join with Orders |
| review_score | Customer rating from 1–5 | Customer satisfaction and STI |
| review_comment_title | Review title | Future sentiment analysis |
| review_comment_message | Review text | Future sentiment analysis |
| review_creation_date | Review creation date | Review trend analysis |
| review_answer_timestamp | Review response timestamp | Supporting analysis |

---

## 6. Sellers Dataset

### Purpose

The Sellers dataset provides seller identity and geographical information.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| seller_id | Unique seller identifier | Seller identification |
| seller_zip_code_prefix | Seller ZIP code prefix | Geographic analysis |
| seller_city | Seller city | Geographic analysis |
| seller_state | Seller state | Geographic analysis |

---

## 7. Customers Dataset

### Purpose

The Customers dataset provides customer identity and geographical information.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| customer_id | Unique customer identifier | Customer linkage |
| customer_unique_id | Unique customer identity | Customer analysis |
| customer_zip_code_prefix | Customer ZIP code prefix | Geographic analysis |
| customer_city | Customer city | Geographic analysis |
| customer_state | Customer state | Customer location filtering |

---

## 8. Products Dataset

### Purpose

The Products dataset provides product-level information required for category analysis.

### Important Attributes

| Attribute | Description | TrustLens Usage |
|---|---|---|
| product_id | Unique product identifier | Product linkage |
| product_category_name | Product category | Category-level analysis |
| product_name_lenght | Product name length | Supporting attribute |
| product_description_lenght | Product description length | Supporting attribute |
| product_photos_qty | Number of product photos | Supporting attribute |
| product_weight_g | Product weight | Supporting attribute |
| product_length_cm | Product length | Supporting attribute |
| product_height_cm | Product height | Supporting attribute |
| product_width_cm | Product width | Supporting attribute |

---

# 9. TrustLens Attribute Mapping

The following mapping connects the available Olist attributes with the TrustLens product requirements.

| TrustLens Requirement | Source Attribute(s) | Derived Metric |
|---|---|---|
| Seller identification | seller_id | seller_id |
| Seller order volume | seller_id, order_id | seller_total_orders |
| Delivery performance | purchase and delivery timestamps | delivery_days |
| Delivery delay | delivered date, estimated date | delivery_delay_days |
| On-time delivery | delivered date, estimated date | on_time_delivery |
| Customer satisfaction | review_score | seller_average_rating |
| Review volume | review_id, seller_id | seller_review_count |
| Order completion | order_status | seller_completion_rate |
| Seller trust | Rating, delivery, completion, review volume | seller_trust_index |
| Trust classification | seller_trust_index | trust_band |
| Category performance | product_category_name | category-level metrics |
| Customer geography | customer_state | customer state filtering |
| Seller geography | seller_state | seller location analysis |

---

# 10. Derived Attributes

TrustLens will create the following derived attributes during the data processing phase.

| Derived Attribute | Description |
|---|---|
| order_month | Month extracted from order purchase timestamp |
| delivery_days | Number of days between purchase and delivery |
| delivery_delay_days | Difference between actual and estimated delivery |
| on_time_delivery | Indicates whether delivery occurred on or before estimated date |
| seller_average_rating | Average review score associated with seller orders |
| seller_total_orders | Total number of orders associated with seller |
| seller_review_count | Number of reviews associated with seller |
| seller_completion_rate | Percentage of seller orders considered completed |
| seller_on_time_rate | Percentage of deliveries completed on time |
| seller_trust_index | Composite seller trust score from 0–100 |
| trust_band | High Trust, Monitor, or High Risk |

---

# 11. Seller Trust Index Inputs

The Seller Trust Index will use normalized seller-level metrics.

| Component | Weight |
|---|---:|
| Rating Score | 40% |
| On-Time Delivery Rate | 30% |
| Order Completion Rate | 20% |
| Review Volume Score | 10% |
| Total | 100% |

Rating Score will be normalized from the original 1–5 review scale to a 0–100 scale.

The final Seller Trust Index will range from 0–100.

---

# 12. Trust Bands

| STI Range | Trust Band |
|---:|---|
| 80–100 | High Trust |
| 60–79 | Monitor |
| 0–59 | High Risk |

---

# 13. Dataset Limitations

The Olist dataset does not contain a dedicated return-request or return-status dataset.

Therefore, dedicated return-request analytics are not included in the current MVP implementation.

Similarly, review text is available, but NLP-based sentiment classification is outside the current MVP scope.

These capabilities may be considered as future enhancements.

---

# 14. Validation Checklist

Before implementation, the following must be verified against the downloaded dataset:

- [ ] All expected CSV files are available
- [ ] Required columns are present
- [ ] Seller IDs are available
- [ ] Order IDs are available
- [ ] Product IDs are available
- [ ] Review scores are available
- [ ] Order delivery timestamps are available
- [ ] Estimated delivery dates are available
- [ ] Product categories are available
- [ ] Customer states are available
- [ ] Seller states are available
- [ ] Join keys are consistent
- [ ] Missing values are documented
- [ ] Duplicate records are investigated

---

## Conclusion

The Olist dataset provides the core attributes required for the TrustLens MVP, including seller identification, order activity, delivery performance, customer ratings, product categories, and geographical information.

The dataset inspection will be completed before implementing the data ingestion and preprocessing pipeline.