import pandas as pd
import numpy as np
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime
from transform import transform  # <- NEW: Import the updated function

def extract(url, table_attribs):
    df = pd.DataFrame(columns=table_attribs)

    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    tables = data.find_all('tbody')[0]
    rows = tables.find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            ancher_data = col[1].find_all('a')[1]
            if ancher_data is not None:
                data_dict = {
                    'Name': ancher_data.contents[0],
                    'MC_USD_Billion': col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)

    USD_list = list(df['MC_USD_Billion'])
    USD_list = [float(''.join(x.split('\n'))) for x in USD_list]
    df['MC_USD_Billion'] = USD_list

    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path, index=False)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statements, sql_connection):
    for query in query_statements:
        print(query)
        print(pd.read_sql(query, sql_connection), '\n')

def log_progress(msg):
    timeformat = '%Y-%m-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timeformat)

    with open('code_log.txt', 'a') as f:
        f.write(timestamp + ' : ' + msg + '\n')

# =============================
# Pipeline Execution Starts Here
# =============================

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'

table_attribs = ['Name', 'MC_USD_Billion']
db_name = 'Banks.db'
table_name = 'Largest_banks'
conn = sqlite3.connect(db_name)

query_statements = [
    'SELECT * FROM Largest_banks',
    'SELECT AVG(MC_GBP_Billion) FROM Largest_banks',
    'SELECT Name FROM Largest_banks LIMIT 5'
]

logfile = 'code_log.txt'
output_csv_path = 'Largest_banks_data.csv'

log_progress('Preliminaries complete. Initiating ETL process.')

df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating transformation process.')

df = transform(df)
log_progress('Data transformation complete. Initiating loading process.')

load_to_csv(df, output_csv_path)
log_progress('Data saved to CSV file.')

log_progress('SQL connection initiated.')

load_to_db(df, conn, table_name)
log_progress('Data loaded to database as table. Running the query.')

run_query(query_statements, conn)
conn.close()
log_progress('Process complete.')
