'''
    Description:
    Trading strategy by opening multiple positions - buy and sell - and close the position if the price
reaches a preset constant profit percentage.
'''


import time
from collections import deque

from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)


class PrintInfo:

    @staticmethod
    def execution_print(asset, curr_trade_qty, new_qty):
        first = ''
        second = ''
        next_profit_price = 0
        print()
        print(f'-------EXECUTION--------')
        print()
        print(f'Transaction count: {transaction_count}')
        if asset == 'BTC':
            first = 'BTC'
            second = 'BUSD'
            curr_trade_qty = f'{curr_trade_qty:.8f}'
            new_qty = f'{new_qty:.2f}'
            next_profit_price = btc.btc_waiting_profits_stack[-1][-1]
        elif asset == 'BUSD':
            first = 'BUSD'
            second = 'BTC'
            curr_trade_qty = f'{curr_trade_qty:.2f}'
            new_qty = f'{new_qty:.8f}'
            next_profit_price = busd.busd_waiting_profits_deque[0][-1]
        return f'{curr_trade_qty}  {first} -> {new_qty} {second} on price {curr_price:.2f}\n' \
               f'Next price for partial profit: {next_profit_price:.2f}'

    @staticmethod
    def get_overall_quantities():
        btc.btc_overall = buffer.calculate_overall('BTC', curr_price)
        busd.busd_overall = buffer.calculate_overall('BUSD', curr_price)
        return f'Overall quantity BTC: {btc.btc_overall:.8f}\nOverall quantity BTC: {init_btc_overall_qty:.8f}\n' \
               f'Overall quantity BUSD: {busd.busd_overall:.2f}\nStart quantity BUSD: {init_busd_overall_qty:.2f}'

    @staticmethod
    def print_profits(trades_count, asset):
        return f'Overall profit BTC: {(btc.btc_overall / btc.base_overall - 1) * 100:.2f}%\n' \
               f'Overall profit BUSD: {(busd.busd_overall / busd.base_overall - 1) * 100:.2f}%\n' \
               f'Transaction count: {asset}: {trades_count}\n' \
               f'Next up price: {btc.next_price:.2f}\n' \
               f'Next down price: {busd.next_price:.2f}'

    @staticmethod
    def profit_execution(asset, waiting_qty, profit_qty):
        next_price = 0
        temp_asset = ''
        if asset == 'BTC':
            waiting_qty = f'{waiting_qty:.2f}'
            profit_qty = f'{profit_qty:.8f}'
            temp_asset = 'BUSD'
            if btc.btc_waiting_profits_stack:
                next_price = btc.btc_waiting_profits_stack[-1][-1]
        elif asset == 'BUSD':
            waiting_qty = f'{waiting_qty:.8f}'
            profit_qty = f'{profit_qty:.2f}'
            temp_asset = 'BTC'
            if busd.busd_waiting_profits_deque:
                next_price = busd.busd_waiting_profits_deque[0][-1]
        return f'\n-------PARTIAL PROFIT--------\n\n{waiting_qty} {temp_asset} -> {profit_qty} {asset} on price: ' \
               f'{curr_price:.2f}\n' \
               f'Next price for partial profit: {next_price:.2f}'


class General:
    def __init__(self):
        self.price_list = []

    @staticmethod
    def create_ground_price(price):
        return price

    @staticmethod
    def create_new_price(asset, price):
        if asset == 'BTC':
            return price * price_percentage
        else:
            return price / price_percentage

    @staticmethod
    def check_curr_price(curr_price):
        if curr_price >= btc.next_price:
            return True, 'BTC'
        elif curr_price <= busd.next_price:
            return True, 'BUSD'
        return False,

    @staticmethod
    def execution_order(asset, curr_price):
        trades_count = 0
        if asset == 'BTC':
            curr_trade_qty = btc.quantity * btc.qty_factor()
            new_qty = curr_trade_qty * curr_price
            btc.quantity -= curr_trade_qty
            busd.quantity += curr_trade_qty * curr_price
            btc.next_price = buffer.create_new_price('BTC', curr_price)
            btc.btc_waiting_profits_stack.append((new_qty, curr_price / profit_percentage))
            btc.btc_trades_count += 1
            trades_count = btc.btc_trades_count
            print(print_buffer.execution_print('BTC', curr_trade_qty, new_qty))

        elif asset == 'BUSD':
            curr_trade_qty = busd.quantity * busd.qty_factor()
            new_qty = curr_trade_qty / curr_price
            busd.quantity -= curr_trade_qty
            btc.quantity += curr_trade_qty / curr_price
            busd.next_price = buffer.create_new_price('BUSD', curr_price)
            busd.busd_waiting_profits_deque.appendleft((new_qty, curr_price * profit_percentage))
            busd.busd_trades_count += 1
            trades_count = busd.busd_trades_count
            print(print_buffer.execution_print('BUSD', curr_trade_qty, new_qty))

        print(print_buffer.get_overall_quantities())
        print(print_buffer.print_profits(trades_count, asset))

    @staticmethod
    def check_for_profit(asset):
        trades_count = 0
        is_profit = False
        if asset == 'BTC':
            waiting_qty, waiting_price = btc.btc_waiting_profits_stack[-1]
            if curr_price <= waiting_price:
                is_profit = True
                profit_qty = waiting_qty / curr_price
                btc.quantity += profit_qty
                busd.quantity -= waiting_qty
                btc.btc_waiting_profits_stack.pop()
                btc.next_price = buffer.create_new_price('BTC', curr_price)
                btc.btc_trades_count -= 1
                trades_count = btc.btc_trades_count
                print(print_buffer.profit_execution('BTC', waiting_qty, profit_qty))

        elif asset == 'BUSD':
            waiting_qty, waiting_price = busd.busd_waiting_profits_deque[0]
            if curr_price >= waiting_price:
                is_profit = True
                profit_qty = waiting_qty * curr_price
                busd.quantity += profit_qty
                btc.quantity -= waiting_qty
                busd.busd_waiting_profits_deque.popleft()
                busd.next_price = buffer.create_new_price('BUSD', curr_price)
                busd.busd_trades_count -= 1
                trades_count = busd.busd_trades_count
                print(print_buffer.profit_execution('BUSD', waiting_qty, profit_qty))
        if is_profit:
            print(print_buffer.get_overall_quantities())
            print(print_buffer.print_profits(trades_count, asset))

    @staticmethod
    def calculate_overall(asset, price):
        if asset == 'BTC':
            return btc.quantity + busd.quantity / price
        elif asset == 'BUSD':
            return busd.quantity + btc.quantity * price

    @staticmethod
    def check_for_total_profit():
        global ground_price
        curr_total_btc = buffer.calculate_overall('BTC', curr_price)
        curr_total_busd = buffer.calculate_overall('BUSD', curr_price)
        if (curr_total_btc / btc.base_overall - 1) * 100 >= 0.02 and (
                curr_total_busd / busd.base_overall - 1) * 100 >= 0.02:
            ground_price = buffer.create_ground_price(curr_price)
            btc.btc_waiting_profits_stack = []
            busd.busd_waiting_profits_deque = deque([])
            btc.btc_trades_count = 0
            busd.busd_trades_count = 0
            btc.quantity = btc.base_overall / 2
            busd.quantity = btc.quantity * ground_price
            btc.next_price = buffer.create_new_price('BTC', ground_price)
            busd.next_price = buffer.create_new_price('BUSD', ground_price)
            print(f'\n-------TOTAL PROFIT-------\nNew base price: {ground_price:.2f}\nTotal profit BTC:'
                  f' {(btc.base_overall / init_btc_overall_qty - 1) * 100}%\nNew active quantity BTC: {btc.quantity})\n'
                  f'New active quantity BUSD: {busd.quantity}\nNext up price: {btc.next_price}\n'
                  f'Next down price: {busd.next_price}\nProfit BTC: '
                  f'{(curr_total_btc / btc.base_overall - 1) * 100:.2f}%\n'
                  f'Profit BUSD: {(curr_total_busd / busd.base_overall - 1) * 100:.2f}%')
            btc.base_overall = curr_total_btc
            busd.base_overall = curr_total_busd


class Bitcoin:
    def __init__(self, quantity, next_price):
        self.next_price = next_price
        self.quantity = quantity
        self.btc_trades_count = 0
        self.btc_waiting_profits_stack = []
        self.btc_overall = 0
        self.base_overall = 0

    def qty_factor(self):
        return 1 / (number_trades - self.btc_trades_count)


class Busd:
    def __init__(self, quantity, next_price):
        self.next_price = next_price
        self.quantity = quantity
        self.busd_trades_count = 0
        self.busd_waiting_profits_deque = deque([])
        self.busd_overall = 0
        self.base_overall = 0

    def qty_factor(self):
        return 1 / (number_trades - self.busd_trades_count)


number_trades = 6
price_percentage = 1.001
profit_percentage = 1.0005
transaction_count = 0

buffer = General()
print_buffer = PrintInfo()
ground_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])

initial_btc = 0.02651
initial_busd = 844

btc = Bitcoin(initial_btc, buffer.create_new_price('BTC', ground_price))
busd = Busd(initial_busd, buffer.create_new_price('BUSD', ground_price))

init_btc_overall_qty = buffer.calculate_overall('BTC', ground_price)
init_busd_overall_qty = buffer.calculate_overall('BUSD', ground_price)

btc.quantity = init_btc_overall_qty / 2
busd.quantity = init_busd_overall_qty / 2

btc.base_overall = init_btc_overall_qty
busd.base_overall = init_busd_overall_qty

print('Processing...')
print(f'Next up price: {btc.next_price}')
print(f'Next down price: {busd.next_price}')
print(f'Start quantity BTC: {init_btc_overall_qty}')
print(f'Start quantity BUSD: {init_busd_overall_qty}')

while True:
    curr_price = float(client.get_symbol_ticker(symbol='BTCBUSD')['price'])
    is_ready_to_execute = buffer.check_curr_price(curr_price)
    if is_ready_to_execute[0]:
        transaction_count += 1
        if is_ready_to_execute[1] == 'BTC':
            buffer.execution_order('BTC', curr_price)
        elif is_ready_to_execute[1] == 'BUSD':
            buffer.execution_order('BUSD', curr_price)
    if curr_price > ground_price:
        if btc.btc_waiting_profits_stack:
            buffer.check_for_profit('BTC')
    elif curr_price < ground_price:
        if busd.busd_waiting_profits_deque:
            buffer.check_for_profit('BUSD')
    buffer.check_for_total_profit()
    time.sleep(1)
