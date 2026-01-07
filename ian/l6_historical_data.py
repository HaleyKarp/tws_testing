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
mycontract.symbol = "SMR"
mycontract.secType = "STK"
mycontract.currency = "USD"
mycontract.exchange = "SMART"

app.reqHistoricalData(reqId=app.nextId(), 
                        contract=mycontract, 
                        endDateTime="20240523 16:00:00 US/Eastern",
                        durationStr="1 D",
                        barSizeSetting="1 hour",
                        whatToShow="TRADES",
                        useRTH=1,
                        formatDate=1,
                        keepUpToDate=False,
                        chartOptions=[])