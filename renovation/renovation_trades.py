import time
from collections import deque

from binance.client import Client

api_key = 'c9itieFnQstNwuNEVZzqDJcYD6KqeFnZ6hdypdLWovRrSLRDb9DDjyq5ap3LtmFv'
api_secret = 'k3CHbLo2UdaacdjObSMglzljAjo1tGkvqNdQCp1W0GPkU1tE3U2smZIqLX1YGH3F'

# client = Client(api_key, api_secret)

waiting_btc = deque()
waiting_busd = deque()
gap = 0.0003


def get_deque_sum(deque):
    return sum([member[1] for member in deque])

def populate_deque(price, btc_deque, busd_deque):
    for degree in range(1, 7):
        btc_deque.append([price * ((1 + gap) ** degree), 0.0008])
        busd_deque.append([price * (1 - gap) ** degree, 16])


def make_transaction(price, btc_deque, busd_deque, trade_asset):
    if trade_asset == 'BTC':
        btc_first_member = btc_deque.popleft()
        busd_last_member = busd_deque.pop()
        busd_deque.appendleft([price * (1 - gap), btc_first_member[1] * price])
        btc_deque.append([btc_deque[-1][0] * (1 + gap), busd_last_member[1] / price])

    else:
        print(busd_deque)
        busd_first_member = busd_deque.popleft()
        btc_last_member  = btc_deque.pop()
        btc_deque.appendleft([price*(1+gap),busd_first_member[1] / price])
        busd_deque.append([busd_deque[-1][0] * (1-gap), btc_last_member[1] * price])
        print(busd_deque)

def check_for_trade(price, btc_deque, busd_deque):
    btc_price = btc_deque[0][0]
    busd_price = busd_deque[0][0]
    if price >= btc_price:
        make_transaction(price, btc_deque, busd_deque, 'BTC')
    elif price <= busd_price:
        make_transaction(price, btc_deque, busd_deque, 'BUSD')
    # print(btc_price)
    # print(busd_price)


populate_deque(20000, waiting_btc, waiting_busd)
print(get_deque_sum(waiting_btc))
print(get_deque_sum(waiting_busd))
# print(waiting_btc)
# print()
# print(waiting_busd)

# make_transaction(20000, waiting_btc, waiting_busd)

# check_for_trade(19993, waiting_btc, waiting_busd)
# while True:
#     price = float(input('Price: '))