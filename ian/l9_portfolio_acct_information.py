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

app.reqAccountUpdates(subscribe=True, acctCode="DUP075701")
time.sleep(1)
app.disconnect()