# These requests require a subscription to market data API

# 232 Last Trade Date/Time * Requires subscription to market data API
########################################
#  Still results in Error. Id: 2 Code: 10089 String: Requested market data requires additional subscription for API
########################################


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

# No market data permissions
# mycontract.symbol = "ETH"
# mycontract.secType = "CRYPTO"
# mycontract.currency = "USD"
# mycontract.exchange = "PAXOS"

mycontract.symbol = 'NQ'
mycontract.secType = 'FOP'
mycontract.exchange = 'CME'
mycontract.currency = 'USD'
mycontract.strike = 20000.0

app.reqMarketDataType(3)
# 1 = Realtime, 2 = Delayed, 3 = Frozen
print("Requesting Market Data 232...")

# Generic tick types
# 232 Last Trade Date/Time * Requires subscription to market data API
########################################
#  Still results in Error. Id: 2 Code: 10089 String: Requested market data requires additional subscription for API
########################################
app.reqMktData(reqId=app.nextId(), 
                contract=mycontract, 
                genericTickList="232", 
                snapshot=False, 
                regulatorySnapshot=False, 
                mktDataOptions=[])
                
# First, qualify the contract - reqHeadTimeStamp often requires a qualified contract with conId
print("Step 1: Qualifying contract...")
app.contract_qualified = False
app.reqContractDetails(app.nextId(), mycontract)


# Wait for contract qualification
print("Waiting for contract qualification...")
timeout = 10
start_time = time.time()
while not app.contract_qualified and (time.time() - start_time) < timeout:
    time.sleep(0.1)

if not app.contract_qualified:
    print("ERROR: Contract qualification timed out or failed!")
    print("Check error messages above for details.")
else:
    print(f"Contract qualified! Using: {app.qualified_contract}")
    
    # Use the qualified contract for reqHeadTimeStamp
    reqId = app.nextId()
    print(f"\nStep 2: Requesting head timestamp with reqId: {reqId}")
    print(f"Contract: {app.qualified_contract.symbol} (conId: {app.qualified_contract.conId})")
    
    app.reqHeadTimeStamp(reqId=reqId, 
                        contract=app.qualified_contract, 
                        whatToShow="TRADES", 
                        useRTH=1, # 1 want the earliest date inside trading hours, 0 want the earliest date outside trading hours
                        formatDate=1) # 1 utc in string format or 2 epooch timestamp. 1 better for human consumption, 2 is better for programming
    
    # Wait for the async response - reqHeadTimeStamp is asynchronous
    print("Waiting for head timestamp response...")
    print("(This may take a few seconds. Check for any error messages above.)")
    time.sleep(10)  # Give more time for the callback to fire
    
    if not hasattr(app, 'head_timestamp_received') or not app.head_timestamp_received:
        print("No head timestamp received after 10 seconds.")
       

# Generic tick types
# 232 Last Trade Date/Time * Requires subscription to market data API
########################################
#  Still results in Error. Id: 2 Code: 10089 String: Requested market data requires additional subscription for API
########################################
#app.reqMktData(app.nextId(), mycontract, "232", False, False, [])

app.disconnect()