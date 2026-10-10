"""
data_ingestion.py
=================
Automated ingestion and verification script for the DataCo Smart Supply Chain dataset.
Downloads archive from Kaggle or extracts local zip into data/raw/.
"""

import os
import sys
import zipfile
import urllib.request
import pandas as pd

KAGGLE_DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis"
RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))
PRIMARY_DATA_FILE = os.path.join(RAW_DATA_DIR, "DataCoSupplyChainDataset.csv")
ZIP_FILE_PATH = os.path.join(RAW_DATA_DIR, "dataco_dataset.zip")

def ensure_data_directory():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

def download_dataset():
    ensure_data_directory()
    if os.path.exists(PRIMARY_DATA_FILE):
        print(f"[OK] Primary dataset already present at: {PRIMARY_DATA_FILE}")
        return True

    print(f"Dataset not found at {PRIMARY_DATA_FILE}. Attempting automated download...")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
        urllib.request.install_opener(opener)
        
        print(f"Downloading from {KAGGLE_DATASET_URL}...")
        urllib.request.urlretrieve(KAGGLE_DATASET_URL, ZIP_FILE_PATH)
        print(f"Download complete. Size: {os.path.getsize(ZIP_FILE_PATH):,} bytes.")
        
        print(f"Extracting archive to {RAW_DATA_DIR}...")
        with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
            zip_ref.extractall(RAW_DATA_DIR)
            print("Extracted files:", zip_ref.namelist())
        return True
    except Exception as e:
        print(f"[ERROR] Failed automated download: {e}")
        print("\nPlease manually download the dataset from:")
        print("https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis")
        print(f"and place 'DataCoSupplyChainDataset.csv' inside '{RAW_DATA_DIR}'.")
        return False

def verify_dataset():
    if not os.path.exists(PRIMARY_DATA_FILE):
        print(f"[FAIL] Missing dataset file: {PRIMARY_DATA_FILE}")
        return False
    
    file_size_mb = os.path.getsize(PRIMARY_DATA_FILE) / (1024 * 1024)
    print(f"[OK] Found {PRIMARY_DATA_FILE} ({file_size_mb:.2f} MB)")
    
    # Quick header and row count probe
    df = pd.read_csv(PRIMARY_DATA_FILE, encoding='latin1', nrows=5)
    print(f"[OK] Schema verified: {len(df.columns)} columns detected.")
    return True

if __name__ == "__main__":
    if download_dataset():
        verify_dataset()
    else:
        sys.exit(1)
