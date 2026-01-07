from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.contract import ComboLeg
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
mycontract.symbol = "AAPL"
mycontract.secType = "STK" # Indicates a combo order
mycontract.currency = "USD"
mycontract.exchange = "SMART"

# Stop loss order

parent = Order()
parent.orderId = app.nextId()
parent.action = "BUY"
parent.orderType = "LMT"
parent.lmtPrice = 150.00
parent.totalQuantity = 10
parent.transmit = False
parent.eTradeOnly = False
parent.firmQuoteOnly = False
parent.account = "DUP075701"

profit_taker = Order()
profit_taker.orderId = parent.orderId + 1
profit_taker.parentId = parent.orderId
profit_taker.action = "SELL"
profit_taker.orderType = "LMT"
profit_taker.lmtPrice = 155
profit_taker.totalQuantity = 10
profit_taker.transmit = False
profit_taker.eTradeOnly = False
profit_taker.firmQuoteOnly = False
profit_taker.account = "DUP075701"

stop_loss = Order()
stop_loss.orderId = parent.orderId + 2
stop_loss.parentId = parent.orderId
stop_loss.orderType = "STP"
stop_loss.auxPrice = 140
stop_loss.action = "SELL"
stop_loss.totalQuantity = 10
stop_loss.transmit = True
stop_loss.eTradeOnly = False
stop_loss.firmQuoteOnly = False
stop_loss.account = "DUP075701"


app.placeOrder(orderId=parent.orderId, 
                contract=mycontract, 
                order=parent)
app.placeOrder(orderId=profit_taker.orderId,
                contract=mycontract,
                order=profit_taker)
app.placeOrder(orderId=stop_loss.orderId,
                contract=mycontract,
                order=stop_loss)

time.sleep(3)
app.disconnect()