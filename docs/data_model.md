# Analytical Data Model Specification: Supply Chain Star Schema

## 1. Schema Overview

The operational supply chain transaction data is structured into a 3NF Star Schema optimized for high-performance Power BI reporting (TMDL/PBIR) and SQL analytics.

```mermaid
erDiagram
    dim_date ||--o{ fact_order_items : "order_date_key (1:N, Active)"
    dim_date ||--o{ fact_order_items : "shipping_date_key (1:N, Inactive)"
    dim_customer ||--o{ fact_order_items : "customer_id (1:N, Active)"
    dim_geography ||--o{ fact_order_items : "geo_id (1:N, Active)"
    dim_order ||--o{ fact_order_items : "order_id (1:N, Active)"
    dim_product ||--o{ fact_order_items : "product_id (1:N, Active)"
    dim_shipping ||--o{ fact_order_items : "shipping_id (1:N, Active)"

    fact_order_items {
        int order_item_id PK
        int order_id FK
        int order_date_key FK
        int shipping_date_key FK
        int customer_id FK
        int product_id FK
        int geo_id FK
        int shipping_id FK
        int order_item_quantity
        decimal sales
        decimal order_item_discount
        decimal order_item_discount_rate
        decimal order_item_product_price
        decimal order_item_profit_ratio
        decimal order_profit_per_order
        decimal benefit_per_order
        decimal sales_per_customer
        int days_for_shipping_real
        int days_for_shipment_scheduled
        int late_delivery_risk
    }

    dim_date {
        int date_key PK
        date full_date
        int year
        int quarter
        int month
        string month_name
        string year_month
        int week
        int day_of_week
        string day_name
        int is_weekend
    }

    dim_customer {
        int customer_id PK
        string customer_fname
        string customer_lname
        string customer_segment
        string customer_city
        string customer_state
        string customer_country
        string customer_street
        string customer_zipcode
    }

    dim_geography {
        int geo_id PK
        string market
        string order_region
        string order_country
        string order_state
        string order_city
        double latitude
        double longitude
    }

    dim_order {
        int order_id PK
        string order_status
        string payment_type
    }

    dim_product {
        int product_id PK
        string product_name
        decimal product_price
        int category_id
        string category_name
        int department_id
        string department_name
    }

    dim_shipping {
        int shipping_id PK
        string shipping_mode
        string delivery_status
    }
```

---

## 2. Table Specifications & Cardinalities

| Table Name | Type | Grain | Row Count | Primary Key | Description |
|---|---|---|---|---|---|
| **`fact_order_items`** | Fact | Line item per order | 180,519 | `order_item_id` | Core transaction metrics (sales, profit, quantity, shipping days, delivery risk). |
| **`dim_date`** | Dimension | Calendar day | 1,133 | `date_key` | Calendar dimensions covering 2015-01-01 to 2018-02-06. |
| **`dim_customer`** | Dimension | Customer account | 20,652 | `customer_id` | Customer profile, segment, and billing address. |
| **`dim_geography`** | Dimension | Fulfillment routing | 3,772 | `geo_id` | Market, regional destination, coordinates. |
| **`dim_order`** | Dimension | Order header | 65,752 | `order_id` | Order status and payment mechanism. |
| **`dim_product`** | Dimension | Catalog SKU | 118 | `product_id` | Product catalog with category and department hierarchy. |
| **`dim_shipping`** | Dimension | Shipping profile | 16 | `shipping_id` | Shipping mode and final delivery status combinations. |

---

## 3. Relationships & Referential Integrity

- All relationships follow `1:*` cardinality with **Single** cross-filter direction pointing from Dimension to Fact.
- Full referential integrity verified: **0 orphaned foreign keys** across all 180,519 fact records.
