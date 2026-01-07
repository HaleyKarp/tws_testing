from ibapi.client import *
from ibapi.wrapper import *
import time
import threading
from services.ibapi.client import app

app.connect("127.0.0.1", 7497, clientId=1)
threading.Thread(target=app.run).start()
time.sleep(1)

# Stock
mycontract = Contract()
mycontract.symbol = "AAPL"
mycontract.secType = "STK"
mycontract.currency = "USD"
mycontract.exchange = "SMART"
mycontract.primaryExchange = "NASDAQ"

# Future
futurecontract = Contract()
futurecontract.symbol = "ES"
futurecontract.secType = "FUT"
futurecontract.currency = "USD"
futurecontract.exchange = "CME"
futurecontract.lastTradeDateOrContractMonth = 203012

# Option
optioncontract = Contract()
optioncontract.symbol = "SPX"
optioncontract.secType = "OPT"
optioncontract.currency = "USD"
optioncontract.exchange = "SMART"
optioncontract.right = "PUT"
optioncontract.tradingClass = "SPXW"
optioncontract.lastTradeDateOrContractMonth = 202612
optioncontract.strike = 7840
# futurecontract.lastTradeDateOrContractMonth = 203012

# app.reqContractDetails(app.nextId(), mycontract)
# app.reqContractDetails(app.nextId(), futurecontract)
app.reqContractDetails(app.nextId(), optioncontract)