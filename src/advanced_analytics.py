"""
advanced_analytics.py
=====================
Implements Advanced Analytics modules:
1. Product ABC Classification by Revenue & Profit Contribution
2. Pareto 80/20 Concentration (Regions, Categories, Late Shipments)
3. Delivery Risk Predictive Modeling (Leakage-free, Temporal Train/Test Split)
4. Demand Forecasting (Monthly Time Series, Naive Baseline Benchmark, RMSE/MAE/MAPE)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, precision_recall_fscore_support
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

CLEAN_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "supply_chain_clean.csv"))
FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports", "figures"))
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_abc_pareto_analysis(df):
    print("--- 1. Running ABC & Pareto Analysis ---")
    
    # Product ABC
    prod_stats = df.groupby(['product_id', 'product_name', 'category_name']).agg(
        total_revenue=('net_sales', 'sum'),
        total_profit=('profit', 'sum'),
        total_units=('order_item_quantity', 'sum')
    ).reset_index()

    prod_stats = prod_stats.sort_values(by='total_revenue', ascending=False)
    prod_stats['cum_revenue'] = prod_stats['total_revenue'].cumsum()
    total_rev = prod_stats['total_revenue'].sum()
    prod_stats['cum_rev_pct'] = (prod_stats['cum_revenue'] / total_rev) * 100

    def get_abc(p):
        if p <= 70.0:
            return 'A (Top 70%)'
        elif p <= 90.0:
            return 'B (Next 20%)'
        else:
            return 'C (Bottom 10%)'

    prod_stats['abc_class'] = prod_stats['cum_rev_pct'].apply(get_abc)
    abc_summary = prod_stats.groupby('abc_class').agg(
        product_count=('product_id', 'count'),
        total_sales=('total_revenue', 'sum'),
        total_profit=('total_profit', 'sum')
    ).reset_index()
    abc_summary['sales_share_pct'] = (abc_summary['total_sales'] / total_rev) * 100
    abc_summary['profit_share_pct'] = (abc_summary['total_profit'] / prod_stats['total_profit'].sum()) * 100

    print("\nProduct ABC Summary:")
    print(abc_summary.to_string(index=False))

    # Regional Late Pareto
    eligible = df[df['is_eligible_shipment'] == 1].copy()
    region_late = eligible.groupby('order_region')['is_late_delivery'].agg(['count', 'sum']).reset_index()
    region_late.columns = ['order_region', 'total_shipments', 'late_shipments']
    region_late = region_late.sort_values(by='late_shipments', ascending=False)
    region_late['cum_late'] = region_late['late_shipments'].cumsum()
    total_lates = region_late['late_shipments'].sum()
    region_late['cum_late_pct'] = (region_late['cum_late'] / total_lates) * 100

    top_80_regions = region_late[region_late['cum_late_pct'] <= 85.0]
    print(f"\nRegional Late Pareto: {len(top_80_regions)} of {len(region_late)} regions account for ~85% of all late shipments.")

    return prod_stats, abc_summary

def run_delivery_risk_model(df):
    print("\n--- 2. Running Delivery Risk Predictive Modeling ---")
    # Only eligible shipments
    df_model = df[df['is_eligible_shipment'] == 1].copy()

    # Temporal split: Train on 2015-2016, Test on 2017
    # Note: Jan 2018 is held out or included in test
    train_mask = df_model['order_date'] < '2017-01-01'
    test_mask = (df_model['order_date'] >= '2017-01-01') & (df_model['order_date'] < '2018-01-01')

    # Leakage Prevention: Only strictly pre-transit order features
    feature_cols_cat = ['shipping_mode', 'market', 'order_region', 'category_name', 'customer_segment']
    feature_cols_num = ['shipping_days_scheduled', 'order_item_quantity', 'net_sales', 'order_item_product_price']

    X = df_model[feature_cols_cat + feature_cols_num]
    y = df_model['is_late_delivery']

    X_train = X[train_mask]
    y_train = y[train_mask]
    X_test = X[test_mask]
    y_test = y[test_mask]

    print(f"Train sample: {len(X_train):,} items (2015-2016) | Late rate: {y_train.mean():.2%}")
    print(f"Test sample:  {len(X_test):,} items (2017)      | Late rate: {y_test.mean():.2%}")

    # Baseline: Majority Class Predictor
    majority_class = y_train.mode()[0]
    y_pred_baseline = np.full_like(y_test, majority_class)
    baseline_acc = (y_test == y_pred_baseline).mean()
    print(f"Baseline (Majority Class {majority_class}) Accuracy: {baseline_acc:.4f}")

    # Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), feature_cols_cat),
            ('num', 'passthrough', feature_cols_num)
        ]
    )

    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    # Train Logistic Regression
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X_train_trans, y_train)

    y_pred = clf.predict(X_test_trans)
    y_proba = clf.predict_proba(X_test_trans)[:, 1]

    auc = roc_auc_score(y_test, y_proba)
    acc = (y_test == y_pred).mean()
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')

    print("\nDelivery Risk Logistic Regression Results (Test Set 2017):")
    print(f"Accuracy:  {acc:.4f} (vs Baseline: {baseline_acc:.4f})")
    print(f"ROC-AUC:   {auc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")

    # Export Feature Importances / Coefficients
    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(feature_cols_cat)
    all_feature_names = list(cat_feature_names) + feature_cols_num
    coefs = pd.DataFrame({
        'feature': all_feature_names,
        'coefficient': clf.coef_[0]
    }).sort_values(by='coefficient', key=abs, ascending=False)
    
    print("\nTop Predictors of Late Delivery:")
    print(coefs.head(8).to_string(index=False))

    return coefs, {'roc_auc': auc, 'accuracy': acc, 'baseline_accuracy': baseline_acc, 'f1': f1}

def run_demand_forecasting(df):
    print("\n--- 3. Running Demand Forecasting Time-Series Analysis ---")
    # Monthly aggregation
    monthly = df.groupby(df['order_date'].dt.to_period('M')).agg(
        order_count=('order_id', 'nunique'),
        net_sales=('net_sales', 'sum')
    ).reset_index()
    monthly['order_date'] = monthly['order_date'].dt.to_timestamp()
    monthly = monthly.sort_values(by='order_date').reset_index(drop=True)

    # Separate training (2015-2016, 24 months) and test (2017, 12 months)
    train_df = monthly[monthly['order_date'] < '2017-01-01'].copy()
    test_df = monthly[(monthly['order_date'] >= '2017-01-01') & (monthly['order_date'] < '2018-01-01')].copy()

    # Naive Baseline: Previous Month Value
    test_df['naive_forecast'] = [train_df['order_count'].iloc[-1]] + list(test_df['order_count'].iloc[:-1])

    # Moving Average (3-month window) Forecast
    rolling_val = train_df['order_count'].rolling(3).mean().iloc[-1]
    ma_forecasts = []
    hist = list(train_df['order_count'])
    for actual in test_df['order_count']:
        pred = np.mean(hist[-3:])
        ma_forecasts.append(pred)
        hist.append(actual)
    test_df['ma3_forecast'] = ma_forecasts

    # Error Metrics
    def calc_metrics(actual, pred):
        mae = np.mean(np.abs(actual - pred))
        rmse = np.sqrt(np.mean((actual - pred)**2))
        mape = np.mean(np.abs((actual - pred) / actual)) * 100
        return mae, rmse, mape

    naive_mae, naive_rmse, naive_mape = calc_metrics(test_df['order_count'], test_df['naive_forecast'])
    ma_mae, ma_rmse, ma_mape = calc_metrics(test_df['order_count'], test_df['ma3_forecast'])

    print(f"Forecasting Evaluation (Test Year 2017 - Monthly Order Volume):")
    print(f"Naive Baseline Forecast:     MAE={naive_mae:.1f} | RMSE={naive_rmse:.1f} | MAPE={naive_mape:.2f}%")
    print(f"3-Month Moving Avg Forecast: MAE={ma_mae:.1f} | RMSE={ma_rmse:.1f} | MAPE={ma_mape:.2f}%")

    # Plot Forecasting Chart
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(train_df['order_date'], train_df['order_count'], label='Historical Training (2015-2016)', color='#1f77b4', marker='o')
    ax.plot(test_df['order_date'], test_df['order_count'], label='Actual Test (2017)', color='black', marker='o', linewidth=2)
    ax.plot(test_df['order_date'], test_df['ma3_forecast'], label=f'Moving Avg Forecast (MAPE {ma_mape:.1f}%)', color='#2ca02c', linestyle='--', marker='s')
    ax.plot(test_df['order_date'], test_df['naive_forecast'], label=f'Naive Baseline (MAPE {naive_mape:.1f}%)', color='#ff7f0e', linestyle=':', marker='^')

    ax.axvline(pd.to_datetime('2017-01-01'), color='gray', linestyle='--', label='Train/Test Split')
    ax.set_title('Monthly Demand Forecasting: Actual vs Forecasted Orders (2017 Test Set)', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Monthly Order Volume', fontsize=11)
    ax.set_xlabel('Order Month', fontsize=11)
    ax.legend(loc='lower left')

    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, '07_demand_forecast_evaluation.png')
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")

    return test_df

if __name__ == "__main__":
    df = pd.read_csv(CLEAN_DATA_PATH, parse_dates=['order_date', 'shipping_date'])
    run_abc_pareto_analysis(df)
    run_delivery_risk_model(df)
    run_demand_forecasting(df)
    print("\nAdvanced analytics suite completed successfully.")
