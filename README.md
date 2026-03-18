# Soil Health Mapping — Pan India

An end-to-end ML pipeline for predicting soil nutrient levels (N, P, K, OC)
across India using Soil Health Card (SHC) data, satellite imagery, and
Agro-Ecological Zone (AEZ)-stratified Random Forest models.

---

## Pipeline Overview

| Step | File | Description |
|------|------|-------------|
| 1 | `1_data_download.py` | Download raw SHC data from portal |
| 2 | `2_segregate_data_by_state.py` | Split raw data by state |
| 3 | `3_data_preprocessing.ipynb` | Clean and normalise data |
| 4 | `4_satellite_datapipeline.ipynb` | Fetch satellite features via GEE |
| 5 | `5_process_satellite_to_aez.ipynb` | Aggregate satellite data to AEZ level |
| 6 | `6_lulc_filter.ipynb` | LULC-based agricultural land filtering |
| 7 | `7_NIRv_pH.ipynb` | NIRv and pH feature engineering |
| 8 | `8_balanced_RF_model.ipynb` | Train AEZ-wise balanced RF regressors |
| 9 | `9_rf_to_csv.ipynb` | Export RF tree structures to CSV |
| 10 | `10_predict_export_generate.ipynb` | Final prediction and map generation |

---

## Setup
```bash
conda create -n soil python=3.12
conda activate soil
pip install -r requirements.txt
```

---

## Data & Pre-trained Models

Large files (`shc_data/`, `rfr_joblib/`, `rfr_csv/`) are not tracked in this repo.

📥 **Download from Google Drive:** [Data](https://drive.google.com/file/d/1RU_stGcUCIZv2ty1cofOmqldeKSbg7GA/view?usp=sharing)


The archive contains:
- `shc_data/` — Raw and normalised Soil Health Card data (2023–24)
- `rfr_joblib/` — Trained Random Forest models per AEZ per nutrient
- `rfr_csv/` — Exported RF tree structures (10 trees, depth 16)

Alternatively, run Steps 1–7 sequentially to regenerate everything from scratch.

---

## AEZs Covered

AEZ 2 through 19 (18 zones), predicting **N, P, K, OC** per zone.

---

## Configuration

All paths and parameters are centralised in `config.yaml`.

---
