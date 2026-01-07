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
mycontract.symbol = "AAPL,TSLA"
mycontract.secType = "BAG" # Indicates a combo order
mycontract.currency = "USD"
mycontract.exchange = "SMART"

# TSLA leg
leg1 = ComboLeg()
leg1.conId = 76792991
leg1.ratio = 1
leg1.action = "BUY"
leg1.exchange = "SMART"

# AAPL leg
leg2 = ComboLeg()
leg2.conId = 265598
leg2.ratio = 1
leg2.action = "SELL"
leg2.exchange = "SMART"

mycontract.comboLegs = [leg1, leg2]

myorder = Order()
myorder.orderId = app.nextId()
myorder.action = "BUY"
myorder.orderType = "LMT"
myorder.lmtPrice = 100.00
myorder.totalQuantity = 10
myorder.tif = "GTC"
# NonGuaranteed must be passed via smartComboRoutingParams and value must be string "1"
myorder.smartComboRoutingParams = [TagValue("NonGuaranteed", "1")]
myorder.eTradeOnly = False
myorder.firmQuoteOnly = False
myorder.account = "DUP075701"

app.placeOrder(orderId=myorder.orderId, 
                contract=mycontract, 
                order=myorder)

time.sleep(3)
app.disconnect()