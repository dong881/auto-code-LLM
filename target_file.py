import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.alphavantage.co/query'
params = {
    'function': 'GLOBAL_QUOTE',
    'symbol': 'TSLA',
    'apikey': 'YOUR_API_KEY'  # Replace with your own API key
}
response = requests.get(url, params=params)
soup = BeautifulSoup(response.text, 'html.parser')
print(json.loads(soup.text)['Global Quote']['05. price'])