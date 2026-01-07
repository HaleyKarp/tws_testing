from ibapi.client import *
from ibapi.wrapper import *
import time
import threading
from services.ibapi.client import app

app.connect("127.0.0.1", 7497, clientId=1)
threading.Thread(target=app.run).start()
time.sleep(1)

for i in range(0,5):
    # print("Sending request ", i)
    print(app.nextId())
    app.reqCurrentTime()
    time.sleep(1)  # Wait for response before sending next request

app.disconnect()