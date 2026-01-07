# Notes

## Terminology

### Contract

A **Contract** in the TWS API is a specification that uniquely identifies a financial instrument you want to trade or query. Think of it as a "recipe" or "address" that tells the system exactly which instrument you're referring to.

#### Conceptual Understanding

In trading, you can't just say "I want to buy Apple" - you need to specify:
- **What type** of instrument (stock, option, future, etc.)
- **Which exchange** it trades on
- **What currency** it's denominated in
- **Additional details** for complex instruments (expiration dates, strike prices, etc.)

A Contract object is like filling out a form with all these details to uniquely identify the instrument.

#### Why Request Contract Details?

When you call `reqContractDetails()`, you're asking TWS: *"Hey, I think I want this instrument (based on the contract spec I provided) - can you confirm it exists, give me all its details, and tell me if my specification is correct or needs adjustment?"*

The response (`contractDetails`) contains:
- **Validation**: Confirms the contract exists and is tradeable
- **Complete Information**: Fills in missing details (like contract ID, trading class, etc.)
- **Market Data**: Provides additional metadata about the instrument
- **Corrections**: May suggest corrections if your specification was slightly off

#### Examples from Your Code

**Stock Contract:**
```python
mycontract = Contract()
mycontract.symbol = "AAPL"           # What: Apple stock
mycontract.secType = "STK"           # Type: Stock
mycontract.currency = "USD"          # Currency: US Dollars
mycontract.exchange = "SMART"        # Where: Smart routing (finds best exchange)
mycontract.primaryExchange = "NASDAQ" # Primary: NASDAQ exchange
```
This says: "I want Apple stock, traded in USD, routed through SMART to NASDAQ"

**Future Contract:**
```python
futurecontract = Contract()
futurecontract.symbol = "ES"         # What: E-mini S&P 500
futurecontract.secType = "FUT"       # Type: Future
futurecontract.currency = "USD"
futurecontract.exchange = "CME"      # Where: Chicago Mercantile Exchange
futurecontract.lastTradeDateOrContractMonth = 203012  # When: December 2030
```
This says: "I want the E-mini S&P 500 future expiring in December 2030"

**Option Contract:**
```python
optioncontract = Contract()
optioncontract.symbol = "SPX"        # What: S&P 500 Index
optioncontract.secType = "OPT"       # Type: Option
optioncontract.currency = "USD"
optioncontract.exchange = "SMART"
optioncontract.right = "PUT"         # Direction: Put option (right to sell)
optioncontract.tradingClass = "SPXW" # Class: Weekly SPX options
optioncontract.lastTradeDateOrContractMonth = 202612  # Expiration: Dec 2026
optioncontract.strike = 7840         # Strike price: 7840
```
This says: "I want a SPX PUT option, strike 7840, expiring December 2026, weekly series"

#### Key Takeaway

A Contract is **not** the actual trade or position - it's just the **specification** of what instrument you're interested in. You use it to:
1. Request market data
2. Place orders
3. Query details about the instrument
4. Validate that your instrument specification is correct

---

### Combo Order (BAG)

A **Combo Order** (also called a "BAG" order) is a single order that executes multiple legs simultaneously. All legs must execute together - if one leg can't be filled, the entire order is rejected.

#### Conceptual Understanding

Think of a combo order like a package deal: "I want to buy X AND sell Y at the same time, or nothing at all." Common use cases:
- **Pairs Trading**: Buy one stock and sell another simultaneously
- **Spread Trading**: Buy and sell related instruments (e.g., different expirations)
- **Hedging**: Enter multiple positions that offset each other

#### How It Works

1. **Contract Setup**: Use `secType = "BAG"` and define each leg as a `ComboLeg`
2. **Leg Definition**: Each leg specifies:
   - `conId`: Contract ID of the instrument
   - `ratio`: How many units of this leg per combo (usually 1)
   - `action`: BUY or SELL for this leg
   - `exchange`: Where to execute this leg

3. **Order Details**: The order itself has:
   - `action`: Overall direction (BUY or SELL the combo)
   - `orderType`: Price type (LMT, MKT, etc.)
   - `smartComboRoutingParams`: Special parameters (like `NonGuaranteed`)

#### Example from Your Code (`l8_combo_order.py`)

```python
# Contract with BAG secType
mycontract = Contract()
mycontract.symbol = "AAPL,TSLA"  # Comma-separated symbols
mycontract.secType = "BAG"        # BAG = combo order
mycontract.currency = "USD"
mycontract.exchange = "SMART"

# Leg 1: BUY TSLA
leg1 = ComboLeg()
leg1.conId = 76792991  # TSLA contract ID
leg1.ratio = 1
leg1.action = "BUY"
leg1.exchange = "SMART"

# Leg 2: SELL AAPL
leg2 = ComboLeg()
leg2.conId = 265598    # AAPL contract ID
leg2.ratio = 1
leg2.action = "SELL"
leg2.exchange = "SMART"

mycontract.comboLegs = [leg1, leg2]

# Order: BUY the combo at $100 limit
myorder = Order()
myorder.action = "BUY"           # Buy the combo (which means BUY TSLA, SELL AAPL)
myorder.orderType = "LMT"
myorder.lmtPrice = 100.00        # Net price for the combo
myorder.totalQuantity = 10        # 10 combos
myorder.smartComboRoutingParams = [TagValue("NonGuaranteed", "1")]
```

**What this does**: Places an order to simultaneously BUY 10 shares of TSLA and SELL 10 shares of AAPL, with a net limit price of $100. The `NonGuaranteed` flag is required for certain order types (REL+MKT, LMT+MKT, REL+LMT) and must be set as a string `"1"`.

#### Key Points

- All legs execute together or not at all (all-or-nothing)
- The `action` on the order is the overall direction of the combo
- Each leg has its own `action` (BUY/SELL) independent of the order action
- `NonGuaranteed` must be set via `smartComboRoutingParams` as a TagValue with string `"1"`

---

### Bracket Order

A **Bracket Order** is a set of three related orders: a parent order and two child orders (profit taker and stop loss). The parent executes first, then the children are automatically activated.

#### Conceptual Understanding

Think of it like a safety net: "Buy this stock, but automatically set a profit target and a stop loss to protect me." The bracket order ensures you have exit strategies in place before entering the position.

**Structure:**
1. **Parent Order**: The initial entry order (e.g., BUY AAPL)
2. **Profit Taker**: A limit order to take profits (e.g., SELL at higher price)
3. **Stop Loss**: A stop order to limit losses (e.g., SELL at lower price)

#### How It Works

1. **Order Linking**: Child orders reference the parent via `parentId`
2. **Transmit Flag**: Controls when orders are sent to the exchange:
   - `transmit=False`: Order is held locally until parent executes
   - `transmit=True`: Order is sent immediately (use on the last order)
3. **Order IDs**: Sequential IDs link the orders together

#### Example from Your Code (`l8_bracket_order.py`)

```python
# Parent: BUY AAPL at $150 limit
parent = Order()
parent.orderId = app.nextId()        # e.g., ID = 2
parent.action = "BUY"
parent.orderType = "LMT"
parent.lmtPrice = 150.00
parent.totalQuantity = 10
parent.transmit = False              # Don't send yet, wait for children

# Profit Taker: SELL at $140 (taking a loss - this seems backwards!)
profit_taker = Order()
profit_taker.orderId = parent.orderId + 1  # ID = 3
profit_taker.parentId = parent.orderId    # Link to parent (ID = 2)
profit_taker.action = "SELL"
profit_taker.orderType = "LMT"
profit_taker.lmtPrice = 140               # Sell at $140 (below entry)
profit_taker.totalQuantity = 10
profit_taker.transmit = False              # Don't send yet

# Stop Loss: SELL at $155 stop
stop_loss = Order()
stop_loss.orderId = parent.orderId + 2     # ID = 4
stop_loss.parentId = parent.orderId        # Link to parent (ID = 2)
stop_loss.orderType = "STP"                # Stop order
stop_loss.auxPrice = 155                   # Trigger at $155
stop_loss.action = "SELL"
stop_loss.totalQuantity = 10
stop_loss.transmit = True                  # Send this last (activates all)

# Place all three orders
app.placeOrder(parent.orderId, contract, parent)
app.placeOrder(profit_taker.orderId, contract, profit_taker)
app.placeOrder(stop_loss.orderId, contract, stop_loss)
```

**What this does**: 
1. Places a bracket order to BUY 10 shares of AAPL at $150 limit
2. If filled, automatically activates:
   - Profit taker: SELL at $140 (limit order)
   - Stop loss: SELL at $155 (stop order triggers if price rises to $155)

**Note**: In this example, the profit taker is set below the entry price ($140 < $150), which would be a loss. Typically you'd set it above entry for profit. The stop loss at $155 protects against the price rising too high (if you're short) or falling too low (if you're long).

#### Key Points

- **Parent-Child Relationship**: Child orders have `parentId` matching parent's `orderId`
- **Sequential IDs**: Order IDs should be sequential (parent, parent+1, parent+2)
- **Transmit Flag**: Only the last order should have `transmit=True` to activate the bracket
- **Automatic Activation**: Once parent fills, children are automatically submitted
- **Order Types**: 
  - Parent/Profit Taker: Usually `LMT` (limit orders)
  - Stop Loss: `STP` (stop order) with `auxPrice` as trigger price