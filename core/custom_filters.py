from django import template
import cryptocompare
import threading

register = template.Library()

def fetch_price_async(value, callback):
    try:
        price_data = cryptocompare.get_price(value, currency='USD')
        if value in price_data and 'USD' in price_data[value]:
            callback(price_data[value]['USD'])
    except Exception as e:
        # Handle any exceptions here, e.g., log the error.
        callback(None)
def fetch_24hr_percent_async(value, callback):
    try:
        historical_data = cryptocompare.get_historical_price_day(value, currency='USD', limit=2)
        if len(historical_data) >= 2:
            # Calculate the percentage change
            close_price_now = historical_data[0]['close']
            close_price_24hr_ago = historical_data[1]['close']
            percent_change_24hr = ((close_price_now - close_price_24hr_ago) / close_price_24hr_ago) * 100
            callback(percent_change_24hr)
    except Exception as e:
        # Handle any exceptions here, e.g., log the error.
        callback(None)

@register.filter
def fetch_price(value):
    result = [None]

    def callback(data):
        result[0] = data

    # Create a thread to fetch the price asynchronously
    thread = threading.Thread(target=fetch_price_async, args=(value, callback))
    thread.start()
    thread.join()  # Wait for the thread to finish (you can use a timeout if needed)

    return result[0]

@register.filter
def fetch_24hr_percent(value):
    result = [None]

    def callback(data):
        result[0] = data

    # Create a thread to fetch the 24-hour percentage change asynchronously
    thread = threading.Thread(target=fetch_24hr_percent_async, args=(value, callback))
    thread.start()
    thread.join()  # Wait for the thread to finish (you can use a timeout if needed)

    return result[0]