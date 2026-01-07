from ibapi.client import *
from ibapi.wrapper import *
import time
import threading
from services.ibapi.client import app

app.connect("127.0.0.1", 7497, clientId=1)
threading.Thread(target=app.run).start()
time.sleep(1)

# Wait for nextValidId before using nextId/order placement
if not app.next_valid_event.wait(timeout=5):
    raise RuntimeError("Timed out waiting for nextValidId from TWS")

# Stock contract
mycontract = Contract()
mycontract.symbol = "SMR"
mycontract.secType = "STK"
mycontract.currency = "USD"
mycontract.exchange = "SMART"


app.reqContractDetails(reqId=app.nextId(), 
                        contract=mycontract)

myorder = Order()
myorder.orderId = app.nextId()
myorder.action = "BUY"
myorder.totalQuantity = 10
myorder.orderType = "MKT"
# Need to specify account and eTradeOnly, example in video did not have these.
myorder.account = "DUP075701"
# Avoid unsupported attributes (see error 10268)
myorder.eTradeOnly = False
myorder.firmQuoteOnly = False


app.placeOrder(orderId=myorder.orderId, 
                contract=mycontract, 
                order=myorder)

# allow callbacks (openOrder/orderStatus) to arrive before disconnecting
time.sleep(3)
app.disconnect()