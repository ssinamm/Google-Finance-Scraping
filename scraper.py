from stock import Stock
from stock import Portfolio
from stock import Position
import requests as r
from bs4 import BeautifulSoup


#main url = 'https://www.google.com/finance/quote/MSFT:NASDAQ'


def get_fx_to_usd(currency):
    fx_url = f'https://www.google.com/finance/quote/{currency}-USD'
    resp = r.get(fx_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    fx_rate = soup.find('div', attrs={'data-last-price': True})
    fx = float(fx_rate['data-last-price'])
    
    return fx


def get_price_information(ticker, exchange):
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}'
    resp = r.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    price_div = soup.find('div', attrs={'data-last-price': True})
    price = float(price_div['data-last-price'])
    currency = price_div['data-currency-code']
    
    usd_price = price
    if currency != 'USD':
        fx = get_fx_to_usd(currency)
        usd_price = round(price * fx, 2)
    else:
        usd_price = price
        
    return{
        'ticker': ticker,
        'exchange': exchange,
        'price': price,
        'currency': currency,
        'usd_price': usd_price
        }
        

shop = Stock('SHOP', 'TSE')
msft = Stock('MSFT', 'NASDAQ')
googl = Stock('GOOGL', 'NASDAQ')

portfolio_ = Portfolio([Position(shop, 10), Position(msft, 2), Position(googl, 60)])

print(portfolio_.get_total_value())