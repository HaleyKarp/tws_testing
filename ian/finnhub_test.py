# Finnhub API Test

# load in the python dotenv library
from dotenv import load_dotenv
load_dotenv()
import os
# load in the finnhub library
import finnhub

# get the API key from the environment variable
api_key = os.getenv("FINNHUB_API_KEY")

# create a finnhub client
client = finnhub.Client(api_key=api_key)

# get the stock price for AAPL
stock_price = client.quote("AAPL")

SMR = client.symbol_lookup("Nuscale Power")
print(SMR)
print(stock_price)