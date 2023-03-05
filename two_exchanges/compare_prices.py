'''
    Description:
Trading strategy on two exchanges - Binance and Kraken. The prices of a currency pair
are compared - in this case BTC/USD - and if the difference between them is greater than
a specific value - the variable profit_percentage - the corresponding orders are executed.
'''

import time

import krakenex
import requests
from pykrakenapi import KrakenAPI

api = krakenex.API()
k = KrakenAPI(api)

# defining public key/request url
binance_key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
kraken_key = 'https://api.kraken.com/0/public/Ticker?price?pair=BTCUSDT'


class Asset:
    trade_count = 0

    def __init__(self, name, quantity, init_quantity=None):
        self.name = name
        self.quantity = quantity
        self.init_quantity = init_quantity

    @staticmethod
    def calculate_profit_percentage(qty1, qty2):
        return float(f'{((qty1 / qty2) - 1) * 100:.2f}')

    @staticmethod
    def make_exchange(binance_asset, kraken_asset, binance_price, kraken_price):
        if binance_asset.name == 'BTC':
            binance_asset.name = 'USDT'
            binance_trade_quantity = binance_asset.quantity
            binance_trade_name = 'BTC'
            binance_asset.quantity *= binance_price

            kraken_asset.name = 'BTC'
            kraken_trade_name = 'USDT'
            kraken_trade_quantity = kraken_asset.quantity
            kraken_asset.quantity /= kraken_price

        else:
            binance_asset.name = 'BTC'
            binance_trade_quantity = binance_asset.quantity
            binance_trade_name = 'USDT'
            binance_asset.quantity /= binance_price

            kraken_asset.name = 'USDT'
            kraken_trade_quantity = kraken_asset.quantity
            kraken_trade_name = 'BTC'
            kraken_asset.quantity *= kraken_price
        Asset.print_trade_info(
            binance_trade_quantity,
            kraken_trade_quantity,
            binance_trade_name,
            kraken_trade_name,
            binance_price,
            kraken_price,
            binance_asset,
            kraken_asset
        )

        Asset.print_profits(binance_asset, kraken_asset)

    @classmethod
    def print_trade_info(cls, binance_trade_quantity, kraken_trade_quantity, binance_trade_name, kraken_trade_name,
                         binance_price, kraken_price, binance_asset, kraken_asset):
        cls.trade_count += 1
        info = f'{("/" * 40)}\nTRADE!!!!!!!\n' \
               f'Number trade: {cls.trade_count}\n' \
               f'Binance {binance_trade_quantity} {binance_trade_name} -> {binance_asset.quantity} on price: ' \
               f'{binance_price}\n' \
               f'Kraken {kraken_trade_quantity} {kraken_trade_name} -> {kraken_asset.quantity} on price: ' \
               f'{kraken_price}'
        print(info)

    @staticmethod
    def print_profits(binance_asset, kraken_asset):
        if binance_asset.name == 'BTC':
            btc_qty = binance_asset.quantity
            usdt_qty = kraken_asset.quantity
            btc_profit = binance_asset.calculate_profit_percentage(binance_asset.quantity, binance_asset.init_quantity)
            usdt_profit = kraken_asset.calculate_profit_percentage(kraken_asset.quantity, kraken_asset.init_quantity)
        else:
            usdt_qty = binance_asset.quantity
            btc_qty = kraken_asset.quantity
            usdt_profit = binance_asset.calculate_profit_percentage(binance_asset.quantity, kraken_asset.init_quantity)
            btc_profit = kraken_asset.calculate_profit_percentage(kraken_asset.quantity, binance_asset.init_quantity)

        info = f'{("*" * 40)}\nProfits:\n' \
               f'BTC: {btc_profit}%\nUSDT: {usdt_profit}%\nAvg: {(btc_profit + usdt_profit) / 2}%\n' \
               f'BTC quantity: {btc_qty}\n' \
               f'USDT quantity: {usdt_qty}\n'
        print(info)


kraken_price = \
    float(requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0])
data_b = requests.get(binance_key)
data_b = data_b.json()

binance_price = float(data_b['price'])

binance_asset = Asset('BTC', 0.009961)
kraken_asset = Asset('USDT', 255.44)
binance_asset.init_quantity = 0.01
kraken_asset.init_quantity = 223.248

btc_init = binance_asset.quantity + kraken_asset.quantity / kraken_price
usdt_init = kraken_asset.quantity + binance_asset.quantity * binance_price

profit_percentage = 0.03
start = time.time()
print(f'Start program\nBTC init: {btc_init}\nUSDT init: {usdt_init}')

while True:
    try:
        kraken_price = \
            float(
                requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0])
        data_b = requests.get(binance_key)
        data_b = data_b.json()
    except:
        print('Fail to get prices')
        time.sleep(2)
        continue
    binance_price = float(data_b['price'])

    diff_price_ratio = Asset.calculate_profit_percentage(binance_price, kraken_price) \
        if binance_asset.name == 'BTC' else Asset.calculate_profit_percentage(kraken_price, binance_price)
    if diff_price_ratio >= profit_percentage:
        Asset.make_exchange(binance_asset, kraken_asset, binance_price, kraken_price)

    time.sleep(0.3)
