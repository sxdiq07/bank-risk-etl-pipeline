# 📄 Data Mapping – Global Bank Risk ETL Pipeline

This document outlines how raw data fields are transformed and mapped into cleaned, structured output for reporting and analysis.

---

## 🗃️ Source: Wikipedia (Archived)  
**URL:** https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks

---

## 📈 Exchange Rates Source  
**File:** `exchange_rate.csv`  
Rates are based on static sample data (can be replaced with dynamic API-based FX rates).

---

## 🔁 Mapping Table

| Raw Column (Source) | Final Column (Output) | Data Type | Transformation Description                   |
|---------------------|------------------------|-----------|-----------------------------------------------|
| `Name`              | `Name`                 | String    | No change – directly taken from source        |
| `MC_USD_Billion`    | `MC_USD_Billion`       | Float     | Extracted as string → cleaned → converted     |
| —                   | `MC_GBP_Billion`       | Float     | USD × FX rate for GBP                         |
| —                   | `MC_EUR_Billion`       | Float     | USD × FX rate for EUR                         |
| —                   | `MC_INR_Billion`       | Float     | USD × FX rate for INR                         |

---

## ✅ Notes

- **Currency Conversion Logic:**  
  FX rates are loaded from `exchange_rate.csv` and applied using `pandas` operations in `transform.py`

- **Missing or malformed values** are logged and handled in `validate.py`

- **Final outputs** are saved to:
  - `Largest_banks_data.csv` (CSV)
  - `Banks.db` (SQLite database table `Largest_banks`)

---

## 📌 Data Flow Summary

```text
Wikipedia HTML Table → Extract → Clean → Convert (Multi-Currency)
         ↓                                 ↓
    Pandas DataFrame            →       Validation Checks
         ↓                                 ↓
        CSV                            SQLite DB
