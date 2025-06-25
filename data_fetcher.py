import yfinance as yf

def get_commodity_data(ticker, start_date, end_date):
    """
    Fetch historical commodity data from Yahoo Finance.

    Parameters:
    ticker (str): The ticker symbol of the commodity.
    start_date (str): The start date for fetching data in 'YYYY-MM-DD' format.
    end_date (str): The end date for fetching data in 'YYYY-MM-DD' format.
    interval (str): The frequency of the data ('1d', '1wk', '1mo').

    Returns:
    pandas.DataFrame: A DataFrame containing the historical commodity data.
    """
    try:
        commodity_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        return commodity_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    