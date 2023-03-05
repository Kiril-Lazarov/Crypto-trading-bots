
import pickle

import time


import krakenex
import requests
from pykrakenapi import KrakenAPI
api = krakenex.API()
k = KrakenAPI(api)
# defining key/request url
binance_key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
kraken_key = 'https://api.kraken.com/0/public/Ticker?price?pair=BTCUSDT'
# requesting data from url

class Asset:
    trade_count = 0
    def __init__(self, name, quantity, init_quantity=None):
        self.name = name
        self.quantity = quantity
        self.init_quantity = init_quantity

    @staticmethod
    def calculate_profit_percentage(qty1,qty2):
        return float(f'{((qty1/qty2)-1)*100:.2f}')

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
                         binance_price, kraken_price, binance_asset,kraken_asset):
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


        info = f'{("*"*40)}\nProfits:\n' \
               f'BTC: {btc_profit}%\nUSDT: {usdt_profit}%\nAvg: {(btc_profit + usdt_profit)/2}%\n' \
               f'BTC quantity: {btc_qty}\n' \
               f'USDT quantity: {usdt_qty}\n'
        print(info)



kraken_price = \
    float(requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0])
data_b = requests.get(binance_key)
data_b = data_b.json()

binance_price = float(data_b['price'])

binance_asset = Asset('BTC', 0.009972)
kraken_asset = Asset('USDT', 232.68)
binance_asset.init_quantity = 0.01
kraken_asset.init_quantity = 223.248

btc_init = binance_asset.quantity + kraken_asset.quantity / kraken_price
usdt_init = kraken_asset.quantity + binance_asset.quantity * binance_price

diff_list = []
max_diffs = []
min_diffs = []
profit_percentage = 0.03
start = time.time()
print(f'Start program\nBTC init: {btc_init}\nUSDT init: {usdt_init}')

while True:
    # end = time.time()
    try:
        kraken_price = \
        float(requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()['result']['XXBTZUSD']['c'][0])
        # print(current_price)
        data_b = requests.get(binance_key)
        data_b = data_b.json()
    except:
        print('Fail to get prices')
        time.sleep(2)
        continue
    binance_price = float(data_b['price'])
    # binance_price = float(input('Binance price: '))
    # kraken_price = float(input('Kraken price: '))
    diff_price_ratio = Asset.calculate_profit_percentage(binance_price,kraken_price) \
    if binance_asset.name == 'BTC' else Asset.calculate_profit_percentage(kraken_price, binance_price)
    if diff_price_ratio >= profit_percentage:
        Asset.make_exchange(binance_asset, kraken_asset, binance_price, kraken_price)
    # print(f'Binance: {data_b} Kraken: {current_price}')
    # print(f'Relation: {(binance_price/current_price -1)*100:.2f}%')
    # diff_list.append(float(f'{(binance_price/kraken_price -1)*100:.2f}'))
    # if len(diff_list) >= 10:
    #     max_diffs.append((max(diff_list)))
    #     min_diffs.append(min(diff_list))
    #     diff_list.clear()
    # if end - start >=10:
    #     pickle_in = open('data_list.txt', 'wb')
    #     pickle.dump([max_diffs, min_diffs], pickle_in)
    #     pickle_in.close()
    #     start = time.time()
    time.sleep(0.3)

# pickle_out = open('data_list.txt', 'rb')
# lists = pickle.load(pickle_out)
# print(lists[0], lists[1])
# pickle_out.close()
