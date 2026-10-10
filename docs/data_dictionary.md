# Data Dictionary: DataCo Smart Supply Chain Dataset

## 1. Overview

- **Source File:** `data/raw/DataCoSupplyChainDataset.csv`
- **Total Records:** 180,519 rows
- **Total Columns:** 53 columns
- **Encoding:** Latin-1 (`latin1`)
- **Dataset Granularity:** **Order Item Level** (`Order Item Id` is a unique primary key for every row)
- **Parent Entity Grain:** **Order Level** (`Order Id`, 65,752 unique orders, average ~2.75 items per order)

## 2. Table Column Specifications

| # | Column Name | Data Type | Non-Null Count | Null % | Unique Values | Sample Value | Description & Business Meaning |
|---|---|---|---|---|---|---|---|
| 1 | `Type` | object | 180,519 | 0.0 % | 4 | DEBIT | Type of transaction made |
| 2 | `Days for shipping (real)` | int64 | 180,519 | 0.0 % | 7 | 3 | Actual shipping days of the purchased product |
| 3 | `Days for shipment (scheduled)` | int64 | 180,519 | 0.0 % | 4 | 4 | Days of scheduled delivery of the purchased product |
| 4 | `Benefit per order` | float64 | 180,519 | 0.0 % | 21,998 | 91.25 | Earnings per order placed |
| 5 | `Sales per customer` | float64 | 180,519 | 0.0 % | 2,927 | 314.6400146 | Total sales per customer made per customer |
| 6 | `Delivery Status` | object | 180,519 | 0.0 % | 4 | Advance shipping | Delivery status of orders: Advance shipping , Late delivery , Shipping canceled , Shipping on time |
| 7 | `Late_delivery_risk` | int64 | 180,519 | 0.0 % | 2 | 0 | Categorical variable that indicates if sending is late (1), it is not late (0). |
| 8 | `Category Id` | int64 | 180,519 | 0.0 % | 51 | 73 | Product category code |
| 9 | `Category Name` | object | 180,519 | 0.0 % | 50 | Sporting Goods | Description of the product category |
| 10 | `Customer City` | object | 180,519 | 0.0 % | 563 | Caguas | City where the customer made the purchase |
| 11 | `Customer Country` | object | 180,519 | 0.0 % | 2 | Puerto Rico | Country where the customer made the purchase |
| 12 | `Customer Email` | object | 180,519 | 0.0 % | 1 | XXXXXXXXX | Customer's email |
| 13 | `Customer Fname` | object | 180,519 | 0.0 % | 782 | Cally | Customer name |
| 14 | `Customer Id` | int64 | 180,519 | 0.0 % | 20,652 | 20755 | Customer ID |
| 15 | `Customer Lname` | object | 180,511 | 0.0 % | 1,109 | Holloway | Customer lastname |
| 16 | `Customer Password` | object | 180,519 | 0.0 % | 1 | XXXXXXXXX | Masked customer key |
| 17 | `Customer Segment` | object | 180,519 | 0.0 % | 3 | Consumer | Types of Customers: Consumer , Corporate , Home Office |
| 18 | `Customer State` | object | 180,519 | 0.0 % | 46 | PR | State to which the store where the purchase is registered belongs |
| 19 | `Customer Street` | object | 180,519 | 0.0 % | 7,458 | 5365 Noble Nectar Island | Street to which the store where the purchase is registered belongs |
| 20 | `Customer Zipcode` | float64 | 180,516 | 0.0 % | 995 | 725.0 | Customer Zipcode |
| 21 | `Department Id` | int64 | 180,519 | 0.0 % | 11 | 2 | Department code of store |
| 22 | `Department Name` | object | 180,519 | 0.0 % | 11 | Fitness | Department name of store |
| 23 | `Latitude` | float64 | 180,519 | 0.0 % | 11,250 | 18.2514534 | Latitude corresponding to location of store |
| 24 | `Longitude` | float64 | 180,519 | 0.0 % | 4,487 | -66.03705597 | Longitude corresponding to location of store |
| 25 | `Market` | object | 180,519 | 0.0 % | 5 | Pacific Asia | Market to where the order is delivered : Africa , Europe , LATAM , Pacific Asia , USCA |
| 26 | `Order City` | object | 180,519 | 0.0 % | 3,597 | Bekasi | Destination city of the order |
| 27 | `Order Country` | object | 180,519 | 0.0 % | 164 | Indonesia | Destination country of the order |
| 28 | `Order Customer Id` | int64 | 180,519 | 0.0 % | 20,652 | 20755 | Customer order code |
| 29 | `order date (DateOrders)` | object | 180,519 | 0.0 % | 65,752 | 1/31/2018 22:56 | Date on which the order is made |
| 30 | `Order Id` | int64 | 180,519 | 0.0 % | 65,752 | 77202 | Order code |
| 31 | `Order Item Cardprod Id` | int64 | 180,519 | 0.0 % | 118 | 1360 | Product code generated through the RFID reader |
| 32 | `Order Item Discount` | float64 | 180,519 | 0.0 % | 1,017 | 13.10999966 | Order item discount value |
| 33 | `Order Item Discount Rate` | float64 | 180,519 | 0.0 % | 18 | 0.039999999 | Order item discount percentage |
| 34 | `Order Item Id` | int64 | 180,519 | 0.0 % | 180,519 | 180517 | Order item code |
| 35 | `Order Item Product Price` | float64 | 180,519 | 0.0 % | 75 | 327.75 | Price of products without discount |
| 36 | `Order Item Profit Ratio` | float64 | 180,519 | 0.0 % | 162 | 0.289999992 | Order Item Profit Ratio |
| 37 | `Order Item Quantity` | int64 | 180,519 | 0.0 % | 5 | 1 | Number of products per order |
| 38 | `Sales` | float64 | 180,519 | 0.0 % | 193 | 327.75 | Value in sales |
| 39 | `Order Item Total` | float64 | 180,519 | 0.0 % | 2,927 | 314.6400146 | Total amount per order |
| 40 | `Order Profit Per Order` | float64 | 180,519 | 0.0 % | 21,998 | 91.25 | Order Profit Per Order |
| 41 | `Order Region` | object | 180,519 | 0.0 % | 23 | Southeast Asia | Region of the world where the order is delivered :  Southeast Asia ,South Asia ,Oceania ,Eastern Asia, West Asia , West of USA , US Center , West Africa, Central Africa ,North Africa ,Western Europe ,Northern , Caribbean , South America ,East Africa ,Southern Europe , East of USA ,Canada ,Southern Africa , Central Asia ,  Europe , Central America, Eastern Europe , South of  USA |
| 42 | `Order State` | object | 180,519 | 0.0 % | 1,089 | Java Occidental | State of the region where the order is delivered |
| 43 | `Order Status` | object | 180,519 | 0.0 % | 9 | COMPLETE | Order Status : COMPLETE , PENDING , CLOSED , PENDING_PAYMENT ,CANCELED , PROCESSING ,SUSPECTED_FRAUD ,ON_HOLD ,PAYMENT_REVIEW |
| 44 | `Order Zipcode` | float64 | 24,840 | 86.24 % | 609 | 99301.0 |  |
| 45 | `Product Card Id` | int64 | 180,519 | 0.0 % | 118 | 1360 | Product code |
| 46 | `Product Category Id` | int64 | 180,519 | 0.0 % | 51 | 73 | Product category code |
| 47 | `Product Description` | float64 | 0 | 100.0 % | 0 | None | Product Description |
| 48 | `Product Image` | object | 180,519 | 0.0 % | 118 | http://images.acmesports.sports/Smart+wa | Link of visit and purchase of the product |
| 49 | `Product Name` | object | 180,519 | 0.0 % | 118 | Smart watch  | Product Name |
| 50 | `Product Price` | float64 | 180,519 | 0.0 % | 75 | 327.75 | Product Price |
| 51 | `Product Status` | int64 | 180,519 | 0.0 % | 1 | 0 | Status of the product stock :If it is 1 not available , 0 the product is available |
| 52 | `shipping date (DateOrders)` | object | 180,519 | 0.0 % | 63,701 | 2/3/2018 22:56 |  |
| 53 | `Shipping Mode` | object | 180,519 | 0.0 % | 4 | Standard Class | The following shipping modes are presented : Standard Class , First Class , Second Class , Same Day |

## 3. Entity Classification and Granularity Breakdown

The 53 columns represent attributes of multiple business domains combined into a single flat denormalized table:

1. **Order Entity (Order Grain):** `Order Id`, `order date (DateOrders)`, `Order Status`, `Market`, `Order Region`, `Order Country`, `Order State`, `Order City`, `Order Zipcode`, `Order Customer Id`, `Type` (payment type: DEBIT, TRANSFER, PAYMENT, CASH).
2. **Order Item Entity (Fact Grain):** `Order Item Id`, `Order Item Cardprod Id`, `Order Item Product Price`, `Order Item Quantity`, `Order Item Discount`, `Order Item Discount Rate`, `Order Item Total` (net revenue), `Sales` (gross revenue), `Order Profit Per Order` (profit contribution per line item), `Order Item Profit Ratio`.
3. **Customer Entity:** `Customer Id`, `Customer Fname`, `Customer Lname`, `Customer Segment` (Consumer, Corporate, Home Office), `Customer City`, `Customer State`, `Customer Country`, `Customer Street`, `Customer Zipcode`.
4. **Product & Catalog Entity:** `Product Card Id`, `Product Category Id`, `Category Id`, `Category Name`, `Department Id`, `Department Name`, `Product Name`, `Product Price`, `Product Status`, `Product Description` (100% null), `Product Image`.
5. **Shipping & Delivery Entity:** `Shipping Mode` (Standard Class, Second Class, First Class, Same Day), `shipping date (DateOrders)`, `Days for shipping (real)`, `Days for shipment (scheduled)`, `Delivery Status` (Late delivery, Advance shipping, Shipping on time, Shipping canceled), `Late_delivery_risk` (binary flag: 1 if late, 0 otherwise).
6. **Store / Origin Geography:** `Latitude`, `Longitude`, `Customer State`, `Customer City` (representing store transaction origins).

## 4. Key Relationships and Integrity Constraints

- **Primary Fact Key:** `Order Item Id` (180,519 unique values, 0 nulls, 0 duplicates).
- **Parent Foreign Key:** `Order Id` (65,752 unique orders).
- **Customer Foreign Key:** `Customer Id` / `Order Customer Id` (20,652 unique customers).
- **Product Foreign Key:** `Product Card Id` / `Order Item Cardprod Id` (118 unique catalog products).
- **Category Foreign Key:** `Category Id` / `Product Category Id` (51 unique categories).
- **Department Foreign Key:** `Department Id` (11 unique departments).
