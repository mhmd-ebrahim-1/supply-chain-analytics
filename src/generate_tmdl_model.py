"""
generate_tmdl_model.py
======================
Generates the complete TMDL (Tabular Model Definition Language) semantic model
for the Supply Chain Analytics PBIP project.
"""

import os
import uuid

SEMANTIC_MODEL_DIR = os.path.abspath(r"D:\Downloads\supply-chain-analytics\powerbi\Supply_Chain_Analytics.SemanticModel")
DEF_DIR = os.path.join(SEMANTIC_MODEL_DIR, "definition")
TABLES_DIR = os.path.join(DEF_DIR, "tables")
CULTURES_DIR = os.path.join(DEF_DIR, "cultures")
DATA_DIR = os.path.abspath(r"D:\Downloads\supply-chain-analytics\data\processed").replace("\\", "/")

def ensure_dirs():
    os.makedirs(TABLES_DIR, exist_ok=True)
    os.makedirs(CULTURES_DIR, exist_ok=True)

def write_root_files():
    # .platform
    platform_content = """{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
  "metadata": {
    "type": "SemanticModel",
    "displayName": "Supply_Chain_Analytics"
  },
  "config": {
    "version": "2.0",
    "logicalId": "00000000-0000-0000-0000-000000000001"
  }
}
"""
    with open(os.path.join(SEMANTIC_MODEL_DIR, ".platform"), "w", encoding="utf-8") as f:
        f.write(platform_content)

    # definition.pbism
    pbism_content = """{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
  "version": "4.2",
  "settings": {
    "qnaEnabled": true
  }
}
"""
    with open(os.path.join(SEMANTIC_MODEL_DIR, "definition.pbism"), "w", encoding="utf-8") as f:
        f.write(pbism_content)

    # database.tmdl
    db_content = """database Supply_Chain_Analytics
\tcompatibilityLevel: 1600
"""
    with open(os.path.join(DEF_DIR, "database.tmdl"), "w", encoding="utf-8") as f:
        f.write(db_content)

    # cultures/en-US.tmdl
    with open(os.path.join(CULTURES_DIR, "en-US.tmdl"), "w", encoding="utf-8") as f:
        f.write("cultureInfo en-US\n")

    # model.tmdl
    model_content = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0
annotation PBI_QueryOrder = ["fact_order_items","dim_date","dim_product","dim_customer","dim_geography","dim_order"]
annotation PBI_ProTooling = ["DevMode"]

ref table fact_order_items
ref table dim_date
ref table dim_product
ref table dim_customer
ref table dim_geography
ref table dim_order
ref table _Measures

ref cultureInfo en-US
"""
    with open(os.path.join(DEF_DIR, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(model_content)

def write_relationships():
    rel_content = """relationship rel_fact_product
\tfromColumn: fact_order_items.product_id
\ttoColumn: dim_product.product_id

relationship rel_fact_customer
\tfromColumn: fact_order_items.customer_id
\ttoColumn: dim_customer.customer_id

relationship rel_fact_geography
\tfromColumn: fact_order_items.geography_id
\ttoColumn: dim_geography.geography_id

relationship rel_fact_order
\tfromColumn: fact_order_items.order_id
\ttoColumn: dim_order.order_id

relationship rel_fact_order_date
\tfromColumn: fact_order_items.order_date_key
\ttoColumn: dim_date.date_key

relationship rel_fact_shipping_date
\tisActive: false
\tfromColumn: fact_order_items.shipping_date_key
\ttoColumn: dim_date.date_key
"""
    with open(os.path.join(DEF_DIR, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(rel_content)

def write_measures_table():
    u = lambda: str(uuid.uuid4())
    content = f"""table _Measures
\tlineageTag: {u()}

\tmeasure 'Total Gross Sales' =
\t\t\tSUM ( fact_order_items[gross_sales] )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Net Sales' =
\t\t\tSUM ( fact_order_items[net_sales] )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Profit' =
\t\t\tSUM ( fact_order_items[profit] )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Profit Margin %' =
\t\t\tDIVIDE ( [Total Profit], [Total Net Sales], BLANK() )
\t\tformatString: 0.00%
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Discount Amount' =
\t\t\tSUM ( fact_order_items[order_item_discount] )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Average Discount Rate %' =
\t\t\tAVERAGE ( fact_order_items[order_item_discount_rate] )
\t\tformatString: 0.00%
\t\tdisplayFolder: 1. Financial KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Orders' =
\t\t\tDISTINCTCOUNT ( fact_order_items[order_id] )
\t\tformatString: #,##0
\t\tdisplayFolder: 2. Volume KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Order Items' =
\t\t\tCOUNTROWS ( fact_order_items )
\t\tformatString: #,##0
\t\tdisplayFolder: 2. Volume KPIs
\t\tlineageTag: {u()}

\tmeasure 'Average Order Value' =
\t\t\tDIVIDE ( [Total Net Sales], [Total Orders], BLANK() )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 2. Volume KPIs
\t\tlineageTag: {u()}

\tmeasure 'Items Per Order' =
\t\t\tDIVIDE ( [Total Order Items], [Total Orders], BLANK() )
\t\tformatString: 0.00
\t\tdisplayFolder: 2. Volume KPIs
\t\tlineageTag: {u()}

\tmeasure 'Total Eligible Shipments' =
\t\t\tCALCULATE ( COUNTROWS ( fact_order_items ), fact_order_items[is_eligible_shipment] = 1 )
\t\tformatString: #,##0
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Late Delivery Items Count' =
\t\t\tCALCULATE ( COUNTROWS ( fact_order_items ), fact_order_items[is_late_delivery] = 1, fact_order_items[is_eligible_shipment] = 1 )
\t\tformatString: #,##0
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Late Delivery Rate %' =
\t\t\tDIVIDE ( [Late Delivery Items Count], [Total Eligible Shipments], BLANK() )
\t\tformatString: 0.00%
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'On-Time Delivery Rate %' =
\t\t\t1 - [Late Delivery Rate %]
\t\tformatString: 0.00%
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Late Orders Count' =
\t\t\tCALCULATE ( DISTINCTCOUNT ( fact_order_items[order_id] ), fact_order_items[is_late_delivery] = 1, fact_order_items[is_eligible_shipment] = 1 )
\t\tformatString: #,##0
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Late Order Rate %' =
\t\t\tDIVIDE ( [Late Orders Count], [Total Orders], BLANK() )
\t\tformatString: 0.00%
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Average Actual Shipping Days' =
\t\t\tAVERAGE ( fact_order_items[shipping_days_real] )
\t\tformatString: 0.00
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Average Scheduled Shipping Days' =
\t\t\tAVERAGE ( fact_order_items[shipping_days_scheduled] )
\t\tformatString: 0.00
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Average Delay Days (Late Only)' =
\t\t\tCALCULATE ( AVERAGE ( fact_order_items[delay_days] ), fact_order_items[is_late_delivery] = 1, fact_order_items[is_eligible_shipment] = 1 )
\t\tformatString: 0.00
\t\tdisplayFolder: 3. Delivery KPIs
\t\tlineageTag: {u()}

\tmeasure 'Sales Previous Month' =
\t\t\tCALCULATE ( [Total Net Sales], PREVIOUSMONTH ( dim_date[full_date] ) )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 4. Time Intelligence
\t\tlineageTag: {u()}

\tmeasure 'MoM Net Sales Growth %' =
\t\t\tVAR PrevSales = [Sales Previous Month]
\t\t\tRETURN DIVIDE ( [Total Net Sales] - PrevSales, PrevSales, BLANK() )
\t\tformatString: 0.00%
\t\tdisplayFolder: 4. Time Intelligence
\t\tlineageTag: {u()}

\tmeasure 'Profit Previous Month' =
\t\t\tCALCULATE ( [Total Profit], PREVIOUSMONTH ( dim_date[full_date] ) )
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 4. Time Intelligence
\t\tlineageTag: {u()}

\tmeasure 'MoM Profit Growth %' =
\t\t\tVAR PrevProfit = [Profit Previous Month]
\t\t\tRETURN DIVIDE ( [Total Profit] - PrevProfit, PrevProfit, BLANK() )
\t\tformatString: 0.00%
\t\tdisplayFolder: 4. Time Intelligence
\t\tlineageTag: {u()}

\tcolumn MeasuresTablePlaceholder
\t\tdataType: int64
\t\thidden
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: MeasuresTablePlaceholder

\tpartition _Measures = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasuresTablePlaceholder = _t]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{"MeasuresTablePlaceholder", Int64.Type}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_fact_table():
    u = lambda: str(uuid.uuid4())
    content = f"""table fact_order_items
\tlineageTag: {u()}

\tcolumn order_item_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_item_id

\tcolumn order_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_id

\tcolumn customer_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_id

\tcolumn product_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: product_id

\tcolumn geography_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: geography_id

\tcolumn order_date_key
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_date_key

\tcolumn shipping_date_key
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: shipping_date_key

\tcolumn shipping_mode
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: shipping_mode

\tcolumn delivery_status
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: delivery_status

\tcolumn order_item_quantity
\t\tdataType: int64
\t\tformatString: #,##0
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: order_item_quantity

\tcolumn order_item_product_price
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: order_item_product_price

\tcolumn order_item_discount
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: order_item_discount

\tcolumn order_item_discount_rate
\t\tdataType: double
\t\tformatString: 0.00%
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: order_item_discount_rate

\tcolumn gross_sales
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: gross_sales

\tcolumn net_sales
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: net_sales

\tcolumn profit
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: profit

\tcolumn profit_margin
\t\tdataType: double
\t\tformatString: 0.00%
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: profit_margin

\tcolumn shipping_days_real
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: shipping_days_real

\tcolumn shipping_days_scheduled
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: shipping_days_scheduled

\tcolumn delay_days
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: delay_days

\tcolumn is_delayed
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: is_delayed

\tcolumn is_late_delivery
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: is_late_delivery

\tcolumn is_eligible_shipment
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: sum
\t\tsourceColumn: is_eligible_shipment

\tcolumn discount_tier
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: discount_tier

\tpartition fact_order_items = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/fact_order_items.csv"' + """),[Delimiter=",", Columns=24, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_item_id", Int64.Type}, {"order_id", Int64.Type}, {"customer_id", Int64.Type}, {"product_id", Int64.Type}, {"geography_id", Int64.Type}, {"order_date_key", Int64.Type}, {"shipping_date_key", Int64.Type}, {"shipping_mode", type text}, {"delivery_status", type text}, {"order_item_quantity", Int64.Type}, {"order_item_product_price", type number}, {"order_item_discount", type number}, {"order_item_discount_rate", type number}, {"gross_sales", type number}, {"net_sales", type number}, {"profit", type number}, {"profit_margin", type number}, {"shipping_days_real", Int64.Type}, {"shipping_days_scheduled", Int64.Type}, {"delay_days", Int64.Type}, {"is_delayed", Int64.Type}, {"is_late_delivery", Int64.Type}, {"is_eligible_shipment", Int64.Type}, {"discount_tier", type text}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "fact_order_items.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_dim_date():
    u = lambda: str(uuid.uuid4())
    content = f"""table dim_date
\tlineageTag: {u()}

\tcolumn date_key
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: date_key

\tcolumn full_date
\t\tdataType: dateTime
\t\tformatString: yyyy-mm-dd
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: full_date

\tcolumn year
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: year

\tcolumn quarter
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: quarter

\tcolumn month
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: month

\tcolumn month_name
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: month_name

\tcolumn year_month
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: year_month

\tcolumn day_of_month
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: day_of_month

\tcolumn day_of_week
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: day_of_week

\tcolumn is_weekend
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: is_weekend

\tpartition dim_date = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/dim_date.csv"' + """),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date_key", Int64.Type}, {"full_date", type date}, {"year", Int64.Type}, {"quarter", Int64.Type}, {"month", Int64.Type}, {"month_name", type text}, {"year_month", type text}, {"day_of_month", Int64.Type}, {"day_of_week", type text}, {"is_weekend", Int64.Type}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "dim_date.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_dim_product():
    u = lambda: str(uuid.uuid4())
    content = f"""table dim_product
\tlineageTag: {u()}

\tcolumn product_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: product_id

\tcolumn product_name
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: product_name

\tcolumn product_price
\t\tdataType: double
\t\tformatString: $#,##0.00
\t\tlineageTag: {u()}
\t\tsummarizeBy: average
\t\tsourceColumn: product_price

\tcolumn category_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: category_id

\tcolumn category_name
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: category_name

\tcolumn department_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: department_id

\tcolumn department_name
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: department_name

\tcolumn abc_revenue_class
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: abc_revenue_class

\tpartition dim_product = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/dim_product.csv"' + """),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"product_id", Int64.Type}, {"product_name", type text}, {"product_price", type number}, {"category_id", Int64.Type}, {"category_name", type text}, {"department_id", Int64.Type}, {"department_name", type text}, {"abc_revenue_class", type text}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "dim_product.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_dim_customer():
    u = lambda: str(uuid.uuid4())
    content = f"""table dim_customer
\tlineageTag: {u()}

\tcolumn customer_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_id

\tcolumn customer_fname
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_fname

\tcolumn customer_lname
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_lname

\tcolumn customer_segment
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_segment

\tcolumn customer_city
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_city

\tcolumn customer_state
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_state

\tcolumn customer_country
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_country

\tcolumn customer_street
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_street

\tcolumn customer_zipcode
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_zipcode

\tcolumn customer_full_name
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: customer_full_name

\tpartition dim_customer = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/dim_customer.csv"' + """),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_id", Int64.Type}, {"customer_fname", type text}, {"customer_lname", type text}, {"customer_segment", type text}, {"customer_city", type text}, {"customer_state", type text}, {"customer_country", type text}, {"customer_street", type text}, {"customer_zipcode", type text}, {"customer_full_name", type text}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "dim_customer.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_dim_geography():
    u = lambda: str(uuid.uuid4())
    content = f"""table dim_geography
\tlineageTag: {u()}

\tcolumn geography_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: geography_id

\tcolumn order_region
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_region

\tcolumn order_country
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_country

\tcolumn order_state
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_state

\tcolumn order_city
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_city

\tcolumn market
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: market

\tpartition dim_geography = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/dim_geography.csv"' + """),[Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_region", type text}, {"order_country", type text}, {"order_state", type text}, {"order_city", type text}, {"market", type text}, {"geography_id", Int64.Type}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "dim_geography.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def write_dim_order():
    u = lambda: str(uuid.uuid4())
    content = f"""table dim_order
\tlineageTag: {u()}

\tcolumn order_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_id

\tcolumn payment_type
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: payment_type

\tcolumn order_status
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_status

\tcolumn market
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: market

\tcolumn order_region
\t\tdataType: string
\t\tlineageTag: {u()}
\t\tsummarizeBy: none
\t\tsourceColumn: order_region

\tpartition dim_order = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Csv.Document(File.Contents(""" + f'"{DATA_DIR}/dim_order.csv"' + """),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_id", Int64.Type}, {"payment_type", type text}, {"order_status", type text}, {"market", type text}, {"order_region", type text}})
\t\t\t\tin
\t\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(TABLES_DIR, "dim_order.tmdl"), "w", encoding="utf-8") as f:
        f.write(content)

def build_all():
    print(f"Building complete TMDL semantic model in {SEMANTIC_MODEL_DIR}...")
    ensure_dirs()
    write_root_files()
    write_relationships()
    write_measures_table()
    write_fact_table()
    write_dim_date()
    write_dim_product()
    write_dim_customer()
    write_dim_geography()
    write_dim_order()
    print("[SUCCESS] All TMDL model files generated successfully.")

if __name__ == "__main__":
    build_all()
