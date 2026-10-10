"""
run_sql_analytics.py
====================
Loads the star schema into an embedded DuckDB analytical database,
executes all SQL scripts (sql/01 through 06), validates execution, and prints sample results.
"""

import os
import duckdb
import re

SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sql"))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

def init_database():
    print("Initializing analytical DuckDB database...")
    con = duckdb.connect(database=':memory:')

    tables = [
        ('fact_order_items', 'fact_order_items.csv'),
        ('dim_date', 'dim_date.csv'),
        ('dim_product', 'dim_product.csv'),
        ('dim_customer', 'dim_customer.csv'),
        ('dim_geography', 'dim_geography.csv'),
        ('dim_shipping', 'dim_shipping.csv'),
        ('dim_order', 'dim_order.csv')
    ]

    for tbl_name, csv_file in tables:
        path = os.path.join(PROCESSED_DIR, csv_file).replace('\\', '/')
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing star schema table file: {path}")
        print(f"Loading {tbl_name} from {csv_file}...")
        con.execute(f"CREATE TABLE {tbl_name} AS SELECT * FROM read_csv_auto('{path}');")
        row_count = con.execute(f"SELECT COUNT(*) FROM {tbl_name}").fetchone()[0]
        print(f"  [OK] Table '{tbl_name}' loaded with {row_count:,} records.")

    return con

def parse_sql_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split on semicolon, keeping non-empty queries
    raw_statements = text.split(';')
    queries = []
    for s in raw_statements:
        clean_s = s.strip()
        # Remove comments to check if meaningful SQL remains
        no_comments = re.sub(r'--.*', '', clean_s).strip()
        if no_comments:
            queries.append(clean_s)
    return queries

def run_all_sql(con):
    sql_files = sorted([f for f in os.listdir(SQL_DIR) if f.endswith('.sql')])
    print(f"\nDiscovered {len(sql_files)} SQL analytics scripts in {SQL_DIR}.")

    for sql_file in sql_files:
        filepath = os.path.join(SQL_DIR, sql_file)
        print(f"\n=======================================================")
        print(f"EXECUTING: {sql_file}")
        print(f"=======================================================")
        queries = parse_sql_file(filepath)
        print(f"Found {len(queries)} distinct SQL statements.")

        for i, q in enumerate(queries, 1):
            print(f"\n--- Running Query {i} in {sql_file} ---")
            try:
                res = con.execute(q).df()
                print(f"Status: SUCCESS | Rows returned: {len(res):,}")
                print(res.head(5).to_string(index=False))
            except Exception as e:
                print(f"[ERROR] Failed query {i}: {e}")
                raise e

if __name__ == "__main__":
    db_con = init_database()
    run_all_sql(db_con)
    print("\n[ALL SQL ANALYTICS EXECUTED AND VALIDATED SUCCESSFULLY]")
