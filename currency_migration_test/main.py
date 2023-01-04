'''
    Description:
    This test crypto bot takes the current price of ten currency pairs every second and decides whether it is
appropriate to make a transaction. At any given time, the entire trading amount is located in one of the
currencies, and if the price of the pairs in which this currency participates is appropriate,
the crypto bot makes transaction. 'Appropriate' means that the new amount should be greater than the previous
available amount of the respective currency. For example, if there was $100 in a previous transaction, the current
currency's dollar equivalent must be greater than $100.

'''

from asset import Asset

from general_methods import GeneralMethods
from binance.client import Client
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)
asset_pairs_list = ['TRX/XRP', 'TRX/ETH', 'TRX/BTC', 'TRX/BUSD', 'XRP/ETH',
                    'XRP/BTC', 'XRP/BUSD', 'ETH/BTC', 'ETH/BUSD', 'BTC/BUSD']
access = GeneralMethods

transaction_count = 0
profit_percentage = 1.003
profit_step = 0.00005


def take_all_prices(prices_list):
    global prices_dict
    for pairs in prices_list:
        joined_pair = ''.join(pairs.split('/'))
        prices_dict[pairs] = float(client.get_symbol_ticker(symbol=joined_pair)['price'])
    return prices_dict


prices_dict = take_all_prices(asset_pairs_list)
print(prices_dict)
busd = Asset(300, 'BUSD')
xrp = Asset(access.multiply(busd.quantity, 1 / prices_dict["XRP/BUSD"]), 'XRP')
eth = Asset(access.multiply(busd.quantity, 1 / prices_dict['ETH/BUSD']), 'ETH')
btc = Asset(access.multiply(busd.quantity, 1 / prices_dict['BTC/BUSD']), 'BTC')
trx = Asset(access.multiply(busd.quantity, 1 / prices_dict['TRX/BUSD']), 'TRX')
obj_list = [trx, xrp, eth, btc, busd]
asset_on_charge = busd.name
print('Processing...')
for obj in obj_list:
    print(f'Starting {obj.name}: {obj.quantity}')
print(access.next_prices(asset_on_charge, {'TRX': trx.quantity, 'XRP': xrp.quantity, 'ETH': eth.quantity,
                                           'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                         profit_percentage))
start = time.time()
while True:
    prices_dict = take_all_prices(asset_pairs_list)

    previous_asset = asset_on_charge
    asset_on_charge, price = access.check_for_profit(asset_on_charge, prices_dict, obj_list, profit_percentage)
    end = time.time()
    if asset_on_charge != previous_asset:
        transaction_count += 1
        start = time.time()
        print(access.execution_report(previous_asset, asset_on_charge, price, transaction_count))
        print(f'Current active asset: {asset_on_charge}')
        for obj in obj_list:
            print(f'{obj.name}: {obj.quantity} Profit: {(obj.quantity / obj.init_qty - 1) * 100:.2f}%')
        print(access.next_prices(asset_on_charge, {'TRX': trx.quantity, 'XRP': xrp.quantity, 'ETH': eth.quantity,
                                                   'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                                 profit_percentage))

    end = time.time()
    if end - start >= 20:

        print('--------ADDING QUANTITY---------')

        for obj in obj_list:
            if obj.name == asset_on_charge:
                print(f'Old quantity {asset_on_charge}: {obj.quantity}')
                if asset_on_charge != 'BUSD':
                    obj.quantity += 10 / float(client.get_symbol_ticker(symbol=f'{asset_on_charge}BUSD')['price'])
                else:
                    obj.quantity += 10
                print(f'New quantity {asset_on_charge}: {obj.quantity}')
        print(access.next_prices(asset_on_charge, {'TRX': trx.quantity, 'XRP': xrp.quantity, 'ETH': eth.quantity,
                                                   'BTC': btc.quantity, 'BUSD': busd.quantity}, asset_pairs_list,
                                 profit_percentage))

        start = time.time()

    time.sleep(1)
