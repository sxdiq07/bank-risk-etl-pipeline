import numpy as np
import requests

def get_live_exchange_rates():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data['rates']
        return {
            'GBP': rates['GBP'],
            'EUR': rates['EUR'],
            'INR': rates['INR']
        }
    else:
        raise Exception("Failed to fetch exchange rates")

def transform(df):
    rates = get_live_exchange_rates()

    df['MC_GBP_Billion'] = [np.round(x * rates['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * rates['INR'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * rates['EUR'], 2) for x in df['MC_USD_Billion']]

    return df
