'''
    Description:
    Test strategy with three currencies - ethereum (ETH), euro (EUR) and binance usd (BUSD). The program checks
every fifth second the current prices for the three currency pairs (ETH/EUR, ETH/BUSD and EUR/BUSD) and calculates
whether they are suitable for trading according to the current quantities of currencies. The ratio is calculated
based on the previous available quantity of the respective currency.
'''

from test_strategy_carrusel.asset import Asset
from test_strategy_carrusel.methods import Methods


from binance.client import Client
import time

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)
method = Methods

eur = Asset(200, 'EUR')
eth = Asset(0.128466, 'ETH', True)
busd = Asset(203.94,'BUSD', True)

objects = [eth, eur, busd]
profit_percentage = 1.0015
transactions_count = 0
message = 'Processing...'
method.print_method(message)
while True:
    if eth.on_charge:
        for obj in objects:
            if obj.name != 'ETH' and not obj.on_charge:
                price = float(client.get_symbol_ticker(symbol = f'ETH{obj.name}')['price'])
                if method.check_for_profit(eth.real_quantity, obj.real_quantity, price, profit_percentage, 'mltp'):
                    transactions_count +=1
                    method.execution(eth, obj,'multiply', objects, transactions_count)

    if eur.on_charge:
        for obj in objects:
            if obj.name != 'EUR' and not obj.on_charge:
                if obj.name == 'ETH':
                    price = float(client.get_symbol_ticker(symbol=f'{obj.name}EUR')['price'])
                    operation = 'division'
                else:
                    price = float(client.get_symbol_ticker(symbol=f'EUR{obj.name}')['price'])
                    operation = 'multiply'
                if method.check_for_profit(eur.real_quantity, obj.real_quantity, price, profit_percentage, operation):
                    transactions_count +=1
                    method.execution(eur, obj,operation, objects, transactions_count)
    if busd.on_charge:
        for obj in objects:
            if obj.name != 'BUSD' and not obj.on_charge:
                price = float(client.get_symbol_ticker(symbol = f'{obj.name}BUSD')['price'])
                if method.check_for_profit(busd.real_quantity, obj.real_quantity, price,
                                           profit_percentage, operation='division'):
                    transactions_count += 1
                    method.execution(busd, obj, 'division', objects, transactions_count)
    time.sleep(5)


