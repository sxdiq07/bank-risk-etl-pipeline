# 💼 Global Bank Risk Data ETL Pipeline

This project showcases an end-to-end ETL (Extract, Transform, Load) pipeline built using Python. It focuses on collecting market capitalization data of the world’s largest banks, converting it across currencies, applying validation, and storing the final dataset in both CSV and SQL formats. The project simulates real-world financial data workflows aligned with enterprise ETL pipelines used in banking and risk analytics.

---

## 🧠 Objectives

- Extract the top 10 global banks by market capitalization (USD) from a public source
- Convert market cap to multiple currencies (GBP, EUR, INR) using live or static FX rates
- Apply data validation to ensure accuracy and consistency
- Store the final dataset in both CSV and SQLite database formats
- Log every step of the ETL process with timestamps
- Run basic SQL queries for insights

---

## ⚙️ Tools & Libraries Used

- Python 3.x
- Pandas
- BeautifulSoup (bs4)
- SQLite3
- Requests
- Logging
- NumPy

---

## 📂 Project Structure

bank-risk-etl-pipeline/
│
├── extract.py # Extracts bank data from the web
├── transform.py # Performs currency conversions
├── load.py # Saves to CSV
├── db_loader.py # Loads into SQLite DB
├── validate.py # Data validation checks
├── config.py # File paths, config variables
│
├── exchange_rate.csv # Currency rates (input file)
├── Largest_banks_data.csv # Cleaned CSV output
├── Banks.db # SQLite DB
│
├── analytics_queries/ # SQL queries for analysis
│
├── docs/
│ └── data_mapping.md # Data transformation log
│
└── README.md # Project documentation

---

## 🔁 ETL Flow Overview

```text
Web (HTML Table)
    ↓
Extract → Transform (FX Conversion) → Validate
    ↓                     ↓
   CSV                SQLite DB

-- 1. Top 5 banks by Market Cap in USD
SELECT Name, MC_USD_Billion FROM Largest_banks ORDER BY MC_USD_Billion DESC LIMIT 5;

-- 2. Average Market Cap in GBP
SELECT AVG(MC_GBP_Billion) FROM Largest_banks;

-- 3. Total number of banks in dataset
SELECT COUNT(*) FROM Largest_banks;
## 📋 Logging

All ETL and validation steps are logged with timestamps using Python's logging module.

Logged events include:
- ETL pipeline start and end
- Data extraction and transformation status
- File save (CSV/DB) confirmation
- Validation outcomes (nulls, negatives, duplicates)

📄 Log file: `etl_log.txt`
