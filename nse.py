import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
import json

import yfinance as yf
dat = yf.Ticker("MSFT")
dat = yf.Ticker("MSFT")
dat.info
dat.calendar
dat.analyst_price_targets
dat.quarterly_income_stmt
dat.history(period='1mo')
dat.option_chain(dat.options[0]).calls
print (dat.info)


# Suppose 'data' is your yfinance dictionary
data = dat.info  # your long dict

def pretty_print_company(data):
    print("\n=== Company Info ===")
    print(f"Name       : {data.get('longName')}")
    print(f"Ticker     : {data.get('symbol')}")
    print(f"Website    : {data.get('website')}")
    print(f"Industry   : {data.get('industry')}")
    print(f"Sector     : {data.get('sector')}")
    print(f"Headquarters: {data.get('address1')}, {data.get('city')}, {data.get('state')} {data.get('zip')}, {data.get('country')}")
    print(f"Phone      : {data.get('phone')}\n")
    
    print("=== Key Metrics ===")
    print(f"Current Price         : {data.get('currentPrice')}")
    print(f"Previous Close        : {data.get('previousClose')}")
    print(f"Market Cap            : {data.get('marketCap'):,}")
    print(f"Beta                  : {data.get('beta')}")
    print(f"52 Week Range         : {data.get('fiftyTwoWeekLow')} - {data.get('fiftyTwoWeekHigh')}")
    print(f"Dividend Rate         : {data.get('dividendRate')}")
    print(f"Dividend Yield        : {data.get('dividendYield')}")
    print(f"P/E Ratio (Trailing)  : {data.get('trailingPE')}")
    print(f"P/E Ratio (Forward)   : {data.get('forwardPE')}\n")

    print("=== Executive Team ===")
    for officer in data.get("companyOfficers", []):
        print(f"- {officer.get('name')} | {officer.get('title')} | Total Pay: ${officer.get('totalPay'):,}")

    print("\n=== Business Summary ===")
    summary = data.get("longBusinessSummary", "")
    for line in summary.split(". "):
        print(f"- {line.strip()}.")
    
# Pretty print
pretty_print_company(data)
