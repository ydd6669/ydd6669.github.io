import yfinance as yf
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data

def calculate_rsi(data, window=14):
    close_prices = data['Close']
    daily_price_changes = close_prices.diff(1)

    gain = daily_price_changes.where(daily_price_changes > 0, 0)
    loss = -daily_price_changes.where(daily_price_changes < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def plot_combined_chart(data, short_window, long_window, stock_symbol):
    # Ensure that the index is a DatetimeIndex
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')

    # Calculate short and long moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()

    # Create a subplot with two axes (two rows, one column)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [1, 3]})

    # Plot candlestick chart with moving averages on the first axis
    apd = mpf.make_addplot(data['Short_MA'], color='blue', ax=ax1)
    apd2 = mpf.make_addplot(data['Long_MA'], color='red', ax=ax1)
    mpf.plot(data, type='candle', ax=ax1, addplot=[apd, apd2], volume=False, show_nontrading=True)
    ax1.set_title(f'{stock_symbol} Candlestick Chart with Moving Averages', pad=20)  # Adjust title spacing

    # Calculate RSI
    rsi_values = calculate_rsi(data)

    # Plot RSI on the second axis
    ax2.plot(rsi_values, label='RSI', color='orange')
    ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    ax2.set_title('Relative Strength Index (RSI)', pad=20)  # Adjust title spacing
    ax2.legend()

    ax3 = ax2.twinx()
    ax3.plot(data['Close'], label='Close Price', color='blue')  # Add Stock Price line
    ax3.set_ylabel('Stock Price')  # Add y-axis label for Stock Price
    ax3.legend()

    plt.tight_layout()  # Adjust overall layout
    plt.show()

if __name__ == "__main__":
    stock_symbol = input("Enter the stock symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    short_window = int(input("Enter the short moving average window: "))
    long_window = int(input("Enter the long moving average window: "))

    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    plot_combined_chart(stock_data, short_window, long_window, stock_symbol)