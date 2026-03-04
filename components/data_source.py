import yfinance as yf

class StockDataSource:
    def fetch(self, symbol, start_date, end_date):
        raise NotImplementedError
    

class YahooFinanceSource(StockDataSource):
    def fetch(self, symbol, start_date, end_date):
        # yfinance logic here
        pass
