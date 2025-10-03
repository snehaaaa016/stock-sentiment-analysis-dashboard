import yfinance as yf

def get_stock_data(ticker="TSLA"):
    data = yf.download(ticker, period="5d", interval="1h")
    return data

if __name__ == "__main__":
    df = get_stock_data("TSLA")
    print(df.head())
