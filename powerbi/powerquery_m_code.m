// =============================================================================
// Power Query M Code: Supply Chain Star Schema Data Ingestion
// =============================================================================

// Parameter: Base Data Directory (Update this path to your local repository)
// let DataPath = "D:\Downloads\supply-chain-analytics\data\processed\"

// -----------------------------------------------------------------------------
// Table 1: DimDate
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\dim_date.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"date_key", Int64.Type},
        {"full_date", type date},
        {"year", Int64.Type},
        {"quarter", Int64.Type},
        {"month", Int64.Type},
        {"month_name", type text},
        {"year_month", type text},
        {"day_of_month", Int64.Type},
        {"day_of_week", type text},
        {"is_weekend", Int64.Type}
    })
in
    ChangeTypes

// -----------------------------------------------------------------------------
// Table 2: DimProduct
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\dim_product.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"product_id", Int64.Type},
        {"product_name", type text},
        {"product_price", type number},
        {"category_id", Int64.Type},
        {"category_name", type text},
        {"department_id", Int64.Type},
        {"department_name", type text},
        {"abc_revenue_class", type text}
    })
in
    ChangeTypes

// -----------------------------------------------------------------------------
// Table 3: DimCustomer
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\dim_customer.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"customer_id", Int64.Type},
        {"customer_fname", type text},
        {"customer_lname", type text},
        {"customer_segment", type text},
        {"customer_city", type text},
        {"customer_state", type text},
        {"customer_country", type text},
        {"customer_street", type text},
        {"customer_zipcode", type text},
        {"customer_full_name", type text}
    })
in
    ChangeTypes

// -----------------------------------------------------------------------------
// Table 4: DimGeography
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\dim_geography.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"order_region", type text},
        {"order_country", type text},
        {"order_state", type text},
        {"order_city", type text},
        {"market", type text},
        {"geography_id", Int64.Type}
    })
in
    ChangeTypes

// -----------------------------------------------------------------------------
// Table 5: DimOrder
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\dim_order.csv"), [Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"order_id", Int64.Type},
        {"payment_type", type text},
        {"order_status", type text},
        {"market", type text},
        {"order_region", type text}
    })
in
    ChangeTypes

// -----------------------------------------------------------------------------
// Table 6: FactOrderItems
// -----------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("D:\Downloads\supply-chain-analytics\data\processed\fact_order_items.csv"), [Delimiter=",", Columns=24, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{
        {"order_item_id", Int64.Type},
        {"order_id", Int64.Type},
        {"customer_id", Int64.Type},
        {"product_id", Int64.Type},
        {"geography_id", Int64.Type},
        {"order_date_key", Int64.Type},
        {"shipping_date_key", Int64.Type},
        {"shipping_mode", type text},
        {"delivery_status", type text},
        {"order_item_quantity", Int64.Type},
        {"order_item_product_price", type number},
        {"order_item_discount", type number},
        {"order_item_discount_rate", type number},
        {"gross_sales", type number},
        {"net_sales", type number},
        {"profit", type number},
        {"profit_margin", type number},
        {"shipping_days_real", Int64.Type},
        {"shipping_days_scheduled", Int64.Type},
        {"delay_days", Int64.Type},
        {"is_delayed", Int64.Type},
        {"is_late_delivery", Int64.Type},
        {"is_eligible_shipment", Int64.Type},
        {"discount_tier", type text}
    })
in
    ChangeTypes
