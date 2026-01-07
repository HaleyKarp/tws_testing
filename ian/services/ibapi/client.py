from ibapi.client import *
from ibapi.wrapper import *
import time
import threading
from ibapi.ticktype import TickTypeEnum

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.qualified_contract = None
        self.contract_qualified = False
        self.head_timestamp_received = False
        # set when TWS sends the first valid order id
        self.next_valid_event = threading.Event()

    def nextValidId(self, orderId: int):
        print("Next valid id: ", orderId)
        self.orderId = orderId
        self.next_valid_event.set()

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def currentTime(self, time):
        print(time)

    def error(self, reqId, errorCode, errorString, advancedOrderReject=None):
        print(f"Error. Id: {reqId} Code: {errorCode} String: {errorString} Advanced order reject: {advancedOrderReject}")

    def contractDetails(self, reqId, contractDetails):
        attrs = vars(contractDetails)
        # print("\n".join(f"{name}: {value}" for name, value in attrs.items()))
        print(f"Contract details: {contractDetails.contract}")
        # Store the qualified contract
        self.qualified_contract = contractDetails.contract
        self.contract_qualified = True

    def contractDetailsEnd(self, reqId):
        print(f"Contract details end: {reqId}")
        # Don't auto-disconnect - let the calling code decide
        # self.disconnect()

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"ReqId: {reqId} TickType: {TickTypeEnum.toString(tickType)} Price: {price} Attrib: {attrib}")

    def tickSize(self, reqId, tickType, size):
        print(f"ReqId: {reqId} TickType: {TickTypeEnum.toString(tickType)} Size: {size}")

    def headTimeStamp(self, reqId, headTimestamp):
        print(f"ReqId: {reqId} HeadTimestamp: {headTimestamp}")
        self.head_timestamp_received = True
        self.cancelHeadTimeStamp(reqId)

    def historicalData(self, reqId, bar):
        print(f"ReqId: {reqId} Bar: {bar}")

    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical data end:ReqId: {reqId} Start: {start} End: {end}")
        self.cancelHistoricalData(reqId)

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"Open order: {orderId} {contract} {order} {orderState}")

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"Order status: {orderId} {status} {filled} {remaining} {avgFillPrice} {permId} {parentId} {lastFillPrice} {clientId} {whyHeld} {mktCapPrice}")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"Exec details: {reqId} {contract} {execution}")

app = TestApp()