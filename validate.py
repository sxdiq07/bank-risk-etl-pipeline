import pandas as pd
import logging

# Setup logging
logging.basicConfig(
    filename='validation_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File to validate
csv_path = 'Largest_banks_data.csv'

try:
    # Load the cleaned data
    df = pd.read_csv(csv_path)

    logging.info("Validation started.")
    print("\n✅ Validation started...\n")

    # 1. Check for missing values
    null_counts = df.isnull().sum()
    print("🔍 Null values in each column:\n", null_counts, "\n")
    logging.info(f"Null values:\n{null_counts.to_string()}")

    # 2. Check for negative values in market caps
    negative_values = df[df['MC_USD_Billion'] < 0]
    print("❗ Negative Market Cap entries:\n", negative_values[['Name', 'MC_USD_Billion']], "\n")
    logging.info(f"Negative values:\n{negative_values.to_string()}")

    # 3. Check for duplicate bank names
    duplicates = df[df.duplicated(subset='Name')]
    print("❗ Duplicate Bank Names:\n", duplicates[['Name']], "\n")
    logging.info(f"Duplicate names:\n{duplicates.to_string()}")

    # 4. Validate currency conversion (optional check: converted columns > 0)
    conversion_columns = ['MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
    for col in conversion_columns:
        invalid_conversion = df[df[col] <= 0]
        if not invalid_conversion.empty:
            print(f"⚠️ Invalid values in {col}:\n", invalid_conversion[['Name', col]], "\n")
            logging.warning(f"Invalid values in {col}:\n{invalid_conversion.to_string()}")

    print("✅ Data validation completed. Check 'validation_log.txt' for full log.")
    logging.info("Validation completed successfully.")

except FileNotFoundError:
    print(f"❌ File '{csv_path}' not found. Make sure the ETL has been run.")
    logging.error(f"File not found: {csv_path}")
