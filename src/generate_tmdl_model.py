"""
generate_tmdl_model.py
======================
Generates the complete TMDL (Tabular Model Definition Language) semantic model
for the Supply Chain Analytics PBIP project matching the exact specification.
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

def u():
    return str(uuid.uuid4())

def write_root_files():
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

    db_content = """database Supply_Chain_Analytics
\tcompatibilityLevel: 1600
"""
    with open(os.path.join(DEF_DIR, "database.tmdl"), "w", encoding="utf-8") as f:
        f.write(db_content)

    with open(os.path.join(CULTURES_DIR, "en-US.tmdl"), "w", encoding="utf-8") as f:
        f.write("cultureInfo en-US\n")

    model_content = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 0
annotation PBI_QueryOrder = ["fact_order_items","dim_date","dim_product","dim_customer","dim_geography","dim_order","dim_shipping"]
annotation PBI_ProTooling = ["DevMode"]

ref table fact_order_items
ref table dim_date
ref table dim_product
ref table dim_customer
ref table dim_geography
ref table dim_order
ref table dim_shipping
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
\tfromColumn: fact_order_items.geo_id
\ttoColumn: dim_geography.geo_id

relationship rel_fact_shipping
\tfromColumn: fact_order_items.shipping_id
\ttoColumn: dim_shipping.shipping_id

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
    lines = [
        "table _Measures",
        f"\tlineageTag: {u()}",
        "",
        "\tmeasure 'Total Sales' =",
        "\t\t\tSUM ( fact_order_items[sales] )",
        "\t\tformatString: $#,##0.00",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Total Profit' =",
        "\t\t\tSUM ( fact_order_items[benefit_per_order] )",
        "\t\tformatString: $#,##0.00",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Profit Margin %' =",
        "\t\t\tDIVIDE ( [Total Profit], [Total Sales], 0 )",
        "\t\tformatString: 0.0%",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Total Orders' =",
        "\t\t\tDISTINCTCOUNT ( fact_order_items[order_id] )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 2. Volume KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Total Quantity' =",
        "\t\t\tSUM ( fact_order_items[order_item_quantity] )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 2. Volume KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'AOV' =",
        "\t\t\tDIVIDE ( [Total Sales], [Total Orders], 0 )",
        "\t\tformatString: $#,##0.00",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Total Discount' =",
        "\t\t\tSUM ( fact_order_items[order_item_discount] )",
        "\t\tformatString: $#,##0.00",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Avg Discount Rate %' =",
        "\t\t\tAVERAGE ( fact_order_items[order_item_discount_rate] )",
        "\t\tformatString: 0.0%",
        "\t\tdisplayFolder: 1. Financial KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Avg Real Shipping Days' =",
        "\t\t\tAVERAGE ( fact_order_items[days_for_shipping_real] )",
        "\t\tformatString: 0.00",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Avg Scheduled Shipping Days' =",
        "\t\t\tAVERAGE ( fact_order_items[days_for_shipment_scheduled] )",
        "\t\tformatString: 0.00",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Shipping Delay Variance' =",
        "\t\t\t[Avg Real Shipping Days] - [Avg Scheduled Shipping Days]",
        "\t\tformatString: +0.00;-0.00;0.00",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Late Delivery Orders' =",
        "\t\t\tCALCULATE ( [Total Orders], fact_order_items[late_delivery_risk] = 1 )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Late Delivery Rate %' =",
        "\t\t\tDIVIDE ( [Late Delivery Orders], [Total Orders], 0 )",
        "\t\tformatString: 0.0%",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'On-Time Delivery Rate %' =",
        "\t\t\tDIVIDE (",
        '\t\t\t    CALCULATE ( [Total Orders], dim_shipping[delivery_status] IN { "Shipping on time", "Advance shipping" } ),',
        "\t\t\t    [Total Orders],",
        "\t\t\t    0",
        "\t\t\t)",
        "\t\tformatString: 0.0%",
        "\t\tdisplayFolder: 3. Delivery KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Active Customers' =",
        "\t\t\tDISTINCTCOUNT ( fact_order_items[customer_id] )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 4. Customer KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Active Products' =",
        "\t\t\tDISTINCTCOUNT ( fact_order_items[product_id] )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 5. Product KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Suspected Fraud Orders' =",
        '\t\t\tCALCULATE ( [Total Orders], dim_order[order_status] = "SUSPECTED_FRAUD" )',
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 4. Customer KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Sales per Customer' =",
        "\t\t\tDIVIDE ( [Total Sales], [Active Customers], 0 )",
        "\t\tformatString: $#,##0.00",
        "\t\tdisplayFolder: 4. Customer KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tmeasure 'Countries Reached' =",
        "\t\t\tDISTINCTCOUNT ( dim_geography[order_country] )",
        "\t\tformatString: #,##0",
        "\t\tdisplayFolder: 4. Customer KPIs",
        f"\t\tlineageTag: {u()}",
        "",
        "\tcolumn Dummy",
        "\t\tdataType: int64",
        "\t\tisHidden",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: Dummy",
        "",
        "\tpartition _Measures = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        '\t\t\t\t    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i45WMlSKjQUA", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Dummy = _t]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Dummy", Int64.Type}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_date():
    lines = [
        "table dim_date",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn date_key",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: date_key",
        "",
        "\tcolumn full_date",
        "\t\tdataType: dateTime",
        "\t\tformatString: yyyy-mm-dd",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: full_date",
        "",
        "\tcolumn year",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: year",
        "",
        "\tcolumn quarter",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: quarter",
        "",
        "\tcolumn month",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: month",
        "",
        "\tcolumn month_name",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: month_name",
        "\t\tsortByColumn: month",
        "",
        "\tcolumn week",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: week",
        "",
        "\tcolumn day_of_week",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: day_of_week",
        "",
        "\tcolumn day_name",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: day_name",
        "",
        "\tcolumn is_weekend",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: is_weekend",
        "",
        "\tpartition dim_date = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_date.csv"),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date_key", Int64.Type}, {"full_date", type date}, {"year", Int64.Type}, {"quarter", Int64.Type}, {"month", Int64.Type}, {"month_name", type text}, {"week", Int64.Type}, {"day_of_week", Int64.Type}, {"day_name", type text}, {"is_weekend", Int64.Type}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_date.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_shipping():
    lines = [
        "table dim_shipping",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn shipping_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: shipping_id",
        "",
        "\tcolumn shipping_mode",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: shipping_mode",
        "",
        "\tcolumn delivery_status",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: delivery_status",
        "",
        "\tpartition dim_shipping = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_shipping.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"shipping_id", Int64.Type}, {"shipping_mode", type text}, {"delivery_status", type text}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_shipping.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_geography():
    lines = [
        "table dim_geography",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn geo_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: geo_id",
        "",
        "\tcolumn market",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: market",
        "",
        "\tcolumn order_region",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_region",
        "",
        "\tcolumn order_country",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_country",
        "",
        "\tcolumn order_state",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_state",
        "",
        "\tcolumn order_city",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_city",
        "",
        "\tcolumn latitude",
        "\t\tdataType: double",
        "\t\tformatString: 0.000000",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: latitude",
        "",
        "\tcolumn longitude",
        "\t\tdataType: double",
        "\t\tformatString: 0.000000",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: longitude",
        "",
        "\tpartition dim_geography = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_geography.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"geo_id", Int64.Type}, {"market", type text}, {"order_region", type text}, {"order_country", type text}, {"order_state", type text}, {"order_city", type text}, {"latitude", type number}, {"longitude", type number}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_geography.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_customer():
    lines = [
        "table dim_customer",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn customer_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_id",
        "",
        "\tcolumn customer_fname",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_fname",
        "",
        "\tcolumn customer_lname",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_lname",
        "",
        "\tcolumn customer_segment",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_segment",
        "",
        "\tcolumn customer_city",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_city",
        "",
        "\tcolumn customer_state",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_state",
        "",
        "\tcolumn customer_country",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_country",
        "",
        "\tcolumn customer_street",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_street",
        "",
        "\tcolumn customer_zipcode",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_zipcode",
        "",
        "\tpartition dim_customer = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_customer.csv"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_id", Int64.Type}, {"customer_fname", type text}, {"customer_lname", type text}, {"customer_segment", type text}, {"customer_city", type text}, {"customer_state", type text}, {"customer_country", type text}, {"customer_street", type text}, {"customer_zipcode", type text}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_customer.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_order():
    lines = [
        "table dim_order",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn order_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_id",
        "",
        "\tcolumn order_status",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_status",
        "",
        "\tcolumn payment_type",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: payment_type",
        "",
        "\tpartition dim_order = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_order.csv"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_id", Int64.Type}, {"order_status", type text}, {"payment_type", type text}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_order.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_dim_product():
    lines = [
        "table dim_product",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn product_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: product_id",
        "",
        "\tcolumn product_name",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: product_name",
        "",
        "\tcolumn product_price",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: product_price",
        "",
        "\tcolumn category_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: category_id",
        "",
        "\tcolumn category_name",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: category_name",
        "",
        "\tcolumn department_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: department_id",
        "",
        "\tcolumn department_name",
        "\t\tdataType: string",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: department_name",
        "",
        "\tpartition dim_product = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/dim_product.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"product_id", Int64.Type}, {"product_name", type text}, {"product_price", type number}, {"category_id", Int64.Type}, {"category_name", type text}, {"department_id", Int64.Type}, {"department_name", type text}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "dim_product.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def write_fact_order_items():
    lines = [
        "table fact_order_items",
        f"\tlineageTag: {u()}",
        "",
        "\tcolumn order_item_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_item_id",
        "",
        "\tcolumn order_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_id",
        "",
        "\tcolumn order_date_key",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: order_date_key",
        "",
        "\tcolumn shipping_date_key",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: shipping_date_key",
        "",
        "\tcolumn customer_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: customer_id",
        "",
        "\tcolumn product_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: product_id",
        "",
        "\tcolumn geo_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: geo_id",
        "",
        "\tcolumn shipping_id",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: none",
        "\t\tsourceColumn: shipping_id",
        "",
        "\tcolumn order_item_quantity",
        "\t\tdataType: int64",
        "\t\tformatString: #,##0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: order_item_quantity",
        "",
        "\tcolumn sales",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: sales",
        "",
        "\tcolumn order_item_discount",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: order_item_discount",
        "",
        "\tcolumn order_item_discount_rate",
        "\t\tdataType: double",
        "\t\tformatString: 0.00%",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: order_item_discount_rate",
        "",
        "\tcolumn order_item_product_price",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: order_item_product_price",
        "",
        "\tcolumn order_item_profit_ratio",
        "\t\tdataType: double",
        "\t\tformatString: 0.00%",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: order_item_profit_ratio",
        "",
        "\tcolumn order_profit_per_order",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: order_profit_per_order",
        "",
        "\tcolumn benefit_per_order",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: benefit_per_order",
        "",
        "\tcolumn sales_per_customer",
        "\t\tdataType: double",
        "\t\tformatString: $#,##0.00",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: sales_per_customer",
        "",
        "\tcolumn days_for_shipping_real",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: days_for_shipping_real",
        "",
        "\tcolumn days_for_shipment_scheduled",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: average",
        "\t\tsourceColumn: days_for_shipment_scheduled",
        "",
        "\tcolumn late_delivery_risk",
        "\t\tdataType: int64",
        "\t\tformatString: 0",
        f"\t\tlineageTag: {u()}",
        "\t\tsummarizeBy: sum",
        "\t\tsourceColumn: late_delivery_risk",
        "",
        "\tpartition fact_order_items = m",
        "\t\tmode: import",
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{DATA_DIR}/fact_order_items.csv"),[Delimiter=",", Columns=20, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        '\t\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
        '\t\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"order_item_id", Int64.Type}, {"order_id", Int64.Type}, {"order_date_key", Int64.Type}, {"shipping_date_key", Int64.Type}, {"customer_id", Int64.Type}, {"product_id", Int64.Type}, {"geo_id", Int64.Type}, {"shipping_id", Int64.Type}, {"order_item_quantity", Int64.Type}, {"sales", type number}, {"order_item_discount", type number}, {"order_item_discount_rate", type number}, {"order_item_product_price", type number}, {"order_item_profit_ratio", type number}, {"order_profit_per_order", type number}, {"benefit_per_order", type number}, {"sales_per_customer", type number}, {"days_for_shipping_real", Int64.Type}, {"days_for_shipment_scheduled", Int64.Type}, {"late_delivery_risk", Int64.Type}})',
        "\t\t\t\tin",
        '\t\t\t\t    #"Changed Type"',
        "",
        "\tannotation PBI_ResultType = Table",
        ""
    ]
    with open(os.path.join(TABLES_DIR, "fact_order_items.tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    ensure_dirs()
    write_root_files()
    write_relationships()
    write_measures_table()
    write_dim_date()
    write_dim_shipping()
    write_dim_geography()
    write_dim_customer()
    write_dim_order()
    write_dim_product()
    write_fact_order_items()
    print("Semantic Model TMDL files generated successfully!")

if __name__ == "__main__":
    main()
