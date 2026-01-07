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